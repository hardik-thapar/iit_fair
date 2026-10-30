"""Run all passes for one model: decision, manipulation check, self-prediction, explanation.

Usage (inside the vLLM container): python -m src.run_model --model qwen3-4b [--pilot]
Outputs: results/raw/<model>/{decision,manip,selfpred,explain}.jsonl (cached by prompt hash).
"""
import argparse
import json
import random
import time

from src.config import ROOT, model_cfg, raw_dir
from src.llm import Cache, Model

BENCH = ROOT / "data" / "benchmark"
T = json.loads((ROOT / "configs" / "templates.json").read_text())
LETTERS = {l: {l} | {l.lower()} for l in "ABCDEFGH"}


def load(path, pilot):
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    return [r for r in rows if r.get("pilot", True)] if pilot else rows


def p_yes(row):
    m = row.get("first_token_mass") or {}
    tot = m.get("yes", 0) + m.get("no", 0)
    return m.get("yes", 0) / tot if tot > 0 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--pilot", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    cfg = model_cfg(a.model)
    out = raw_dir(a.model)
    m = Model(cfg)
    print(f"loaded {a.model} in {time.time() - t0:.0f}s", flush=True)

    # 1. decision pass
    dec = load(BENCH / "decision.jsonl", a.pilot)
    dcache = Cache(out / "decision.jsonl")
    m.run(dcache, "decision", dec, max_tokens=4)
    by_id = {r["id"]: r for r in dcache.rows.values()}

    # 2. manipulation check (names only; same for pilot and full)
    man = load(BENCH / "manip.jsonl", False)
    m.run(Cache(out / "manip.jsonl"), "manip", man, max_tokens=2,
          options={l: LETTERS[l] for l in "ABCDEFGH"})

    # 3. self-prediction: turn 1 = reference prompt, assistant = model's own reference answer
    ref_of = {}
    for d in dec:
        if d["variant"].startswith("ref"):
            ref_of[(d["profile_id"], d["template"], d["lang"])] = d
    sp_items = []
    for d in dec:
        if d["variant"].startswith("ref"):
            continue
        ref = ref_of[(d["profile_id"], d["template"], d["lang"])]
        pr = p_yes(by_id.get(ref["id"], {}))
        if pr is None:
            continue
        own = "Yes" if pr >= 0.5 else "No"
        kind = "control" if d["variant"].startswith("control") else d["variant"]
        phrase = T["selfpred"]["phrases"].get(kind, T["selfpred"]["phrases"]["control"])[d["lang"]]
        for cond in ["N", "A"]:
            q = T["selfpred"][cond][d["lang"]].format(cf_full_name=d["full_name"], cf_hometown=d["hometown"],
                                                       cf_attribute_phrase=phrase)
            sp_items.append({"id": f"{d['id']}|{cond}", "messages": ref["messages"] + [
                {"role": "assistant", "content": own}, {"role": "user", "content": q}]})
    m.run(Cache(out / "selfpred.jsonl"), "selfpred", sp_items, max_tokens=4)

    # 4. explanation pass (reason first): every flipped pair + seeded 25% sample of unflipped pairs
    rng = random.Random(20261030)
    chosen = set()
    for d in dec:
        if d["variant"].startswith("ref"):
            continue
        ref = ref_of[(d["profile_id"], d["template"], d["lang"])]
        pr, pv = p_yes(by_id.get(ref["id"], {})), p_yes(by_id.get(d["id"], {}))
        if pr is None or pv is None:
            continue
        flipped = (pr >= 0.5) != (pv >= 0.5)
        if flipped or rng.random() < 0.25:
            chosen.add(d["id"])
            chosen.add(ref["id"])
    ex_items = [{"id": d["id"], "messages": d["explain_messages"]} for d in dec if d["id"] in chosen]
    m.run(Cache(out / "explain.jsonl"), "explain", ex_items, max_tokens=256, logprobs=None)

    print(f"DONE {a.model} in {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
