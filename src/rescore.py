"""Full-candidate scoring (spec §6.3 fallback) and longer explanations.

Why: in Hindi prompts several models start their answer with "हाँ"/"नहीं", which byte-level
tokenizers split into pieces, so first-token Yes/No mass misses it. Here we score each full
answer string with prompt logprobs and normalise:
    P(Yes) = sum p(yes forms) / sum p(yes forms + no forms)
Forms: Yes, No, हाँ, हां, नहीं, each with and without a leading space (deduplicated by tokens).
Also re-runs explanations that hit the 256-token limit with max_tokens=768.

Usage: python -m src.rescore --model qwen3-4b
Outputs: results/raw/<model>/{decision_scored,selfpred_scored,explain_long}.jsonl
"""
import argparse
import json
import math
import os
import time

from src.config import ROOT, model_cfg, raw_dir
from src.llm import Cache, Model, key_for

FORMS = {"yes": ["Yes", "हाँ", "हां"], "no": ["No", "नहीं"]}


def score_pass(m, tok, items, cache, pass_name):
    from vllm import SamplingParams
    from vllm.inputs import TokensPrompt

    settings = {"candidates": FORMS, "method": "prompt_logprobs_v1", "chat_template_kwargs": m.chat_kwargs}
    todo = []
    for it in items:
        k = key_for(m.cfg["hf_id"], m.cfg.get("revision"), pass_name, it["messages"], settings)
        if not cache.has(k):
            todo.append((k, it))
    print(f"[{pass_name}] {len(items)} items, {len(todo)} to score", flush=True)
    sp = SamplingParams(max_tokens=1, temperature=0.0, prompt_logprobs=0)
    B = 256
    for s in range(0, len(todo), B):
        chunk = todo[s:s + B]
        reqs, index = [], []
        for ci, (k, it) in enumerate(chunk):
            prompt = tok.apply_chat_template(it["messages"], tokenize=False, add_generation_prompt=True,
                                             **m.chat_kwargs)
            pids = tok(prompt, add_special_tokens=False)["input_ids"]
            seen = set()
            for label, forms in FORMS.items():
                for f in forms:
                    for surface in (f, " " + f):
                        cids = tok(surface, add_special_tokens=False)["input_ids"]
                        if not cids or tuple(cids) in seen:
                            continue
                        seen.add(tuple(cids))
                        reqs.append(TokensPrompt(prompt_token_ids=pids + cids))
                        index.append((ci, label, surface, len(pids), len(cids)))
        outs = m.llm.generate(reqs, sp, use_tqdm=False)
        acc = [{"yes": 0.0, "no": 0.0, "forms": {}} for _ in chunk]
        for (ci, label, surface, plen, clen), o in zip(index, outs):
            lp = 0.0
            for pos in range(plen, plen + clen):
                d = o.prompt_logprobs[pos]
                tid = o.prompt_token_ids[pos]
                lp += d[tid].logprob
            p = math.exp(lp)
            acc[ci][label] += p
            acc[ci]["forms"][surface] = round(lp, 4)
        rows = []
        for (k, it), a in zip(chunk, acc):
            tot = a["yes"] + a["no"]
            rows.append({"key": k, "id": it["id"], "pass": pass_name, "model": m.cfg["hf_id"],
                         "p_yes": a["yes"] / tot if tot > 0 else None, "mass": tot, "forms": a["forms"]})
        cache.add_many(rows)
        print(f"[{pass_name}] {min(s + B, len(todo))}/{len(todo)}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    a = ap.parse_args()
    t0 = time.time()
    cfg = model_cfg(a.model)
    cfg.setdefault("vllm_kwargs", {})["enable_prefix_caching"] = True
    out = raw_dir(a.model)
    m = Model(cfg)
    tok = m.llm.get_tokenizer()

    dec = [json.loads(l) for l in open(ROOT / "data/benchmark/decision.jsonl", encoding="utf-8")]
    # Only rows where the first-token readout caught < 90% of the probability need full scoring;
    # elsewhere both readouts agree to within the missing mass (< 0.1).
    first = {r["id"]: (r.get("first_token_total") or 0) for r in Cache(out / "decision.jsonl").rows.values()}
    need = [{"id": d["id"], "messages": d["messages"]} for d in dec if first.get(d["id"], 0) < 0.9]
    score_pass(m, tok, need, Cache(out / "decision_scored.jsonl"), "decision_scored")
    if os.environ.get("SKIP_SELFPRED_SCORING", "1") == "1":
        sp_skip = True
    else:
        sp_skip = False

    # self-prediction prompts: rebuild exactly as run_model did, from its cached rows' ids
    import src.run_model as rm  # reuse prompt construction
    T = rm.T
    raw_dec = {r["id"]: r for r in Cache(out / "decision.jsonl").rows.values()}
    ref_of = {(d["profile_id"], d["template"], d["lang"]): d for d in dec if d["variant"].startswith("ref")}
    sp_items = []
    for d in dec:
        if d["variant"].startswith("ref"):
            continue
        ref = ref_of[(d["profile_id"], d["template"], d["lang"])]
        pr = rm.p_yes(raw_dec.get(ref["id"], {}))
        if pr is None:
            continue
        own = "Yes" if pr >= 0.5 else "No"  # same assistant turn as the original self-prediction pass
        kind = "control" if d["variant"].startswith("control") else d["variant"]
        phrase = T["selfpred"]["phrases"].get(kind, T["selfpred"]["phrases"]["control"])[d["lang"]]
        for cond in ["N", "A"]:
            q = T["selfpred"][cond][d["lang"]].format(cf_full_name=d["full_name"], cf_hometown=d["hometown"],
                                                       cf_attribute_phrase=phrase)
            sp_items.append({"id": f"{d['id']}|{cond}", "messages": ref["messages"] + [
                {"role": "assistant", "content": own}, {"role": "user", "content": q}]})
    if not sp_skip:
        score_pass(m, tok, sp_items, Cache(out / "selfpred_scored.jsonl"), "selfpred_scored")

    # explanations that hit the length limit: regenerate with a larger limit
    ex = Cache(out / "explain.jsonl").rows.values()
    msgs = {d["id"]: d["explain_messages"] for d in dec}
    long_items = [{"id": r["id"], "messages": msgs[r["id"]]} for r in ex if r["finish_reason"] == "length"]
    m.run(Cache(out / "explain_long.jsonl"), "explain", long_items, max_tokens=768, logprobs=None)
    print(f"DONE rescore {a.model} in {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
