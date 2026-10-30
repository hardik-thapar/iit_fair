"""Thin wrapper around vLLM with an on-disk cache.

Every request is keyed by sha256(model, revision, pass, messages, sampling settings).
Results are appended to results/raw/<model_slug>/<pass>.jsonl; a key that is already
there is never sent to the model again.
"""
import hashlib
import json
import math
import os
from pathlib import Path

YES = {"yes", "हाँ", "हां"}
NO = {"no", "नहीं", "नही"}


def slug(model_name):
    return model_name.replace("/", "__")


def key_for(model, revision, pass_name, messages, settings):
    blob = json.dumps([model, revision, pass_name, messages, settings], ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class Cache:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.rows = {}
        if self.path.exists():
            with open(self.path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        r = json.loads(line)
                        self.rows[r["key"]] = r

    def has(self, key):
        return key in self.rows

    def add_many(self, rows):
        with open(self.path, "a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                self.rows[r["key"]] = r
            f.flush()
            os.fsync(f.fileno())


def first_token_probs(logprobs_at_pos0, options=None):
    """Sum probability mass of the first generated token over surface variants.

    options: dict label -> set of normalised strings. Default is Yes/No.
    Returns (probs per label, total mass on all labels).
    """
    options = options or {"yes": YES, "no": NO}
    mass = {k: 0.0 for k in options}
    for lp in logprobs_at_pos0.values():
        tok = (lp.decoded_token or "").strip().strip(".:,!\"'").lower()
        for label, forms in options.items():
            if tok in forms:
                mass[label] += math.exp(lp.logprob)
    return mass, sum(mass.values())


class Model:
    def __init__(self, cfg):
        from vllm import LLM  # imported here so the rest of the code runs without vLLM

        self.cfg = cfg
        kwargs = dict(model=cfg["hf_id"], revision=cfg.get("revision"), seed=cfg.get("seed", 20261030),
                      max_model_len=cfg.get("max_model_len", 4096), gpu_memory_utilization=0.88,
                      trust_remote_code=False, max_logprobs=40)
        kwargs.update(cfg.get("vllm_kwargs", {}))
        self.llm = LLM(**kwargs)
        self.chat_kwargs = cfg.get("chat_template_kwargs", {})

    def run(self, cache, pass_name, items, max_tokens, logprobs=20, options=None, batch=512):
        """items: list of dicts with 'id' and 'messages'. Returns nothing; writes to cache."""
        from vllm import SamplingParams

        settings = {"max_tokens": max_tokens, "temperature": 0.0, "logprobs": logprobs,
                    "chat_template_kwargs": self.chat_kwargs}
        todo = []
        for it in items:
            k = key_for(self.cfg["hf_id"], self.cfg.get("revision"), pass_name, it["messages"], settings)
            if not cache.has(k):
                todo.append((k, it))
        print(f"[{pass_name}] {len(items)} items, {len(items) - len(todo)} cached, {len(todo)} to run", flush=True)
        sp = SamplingParams(max_tokens=max_tokens, temperature=0.0, logprobs=logprobs, seed=20261030)
        for start in range(0, len(todo), batch):
            chunk = todo[start:start + batch]
            outs = self.llm.chat([it["messages"] for _, it in chunk], sp, use_tqdm=False,
                                 chat_template_kwargs=self.chat_kwargs or None)
            rows = []
            for (k, it), out in zip(chunk, outs):
                o = out.outputs[0]
                row = {"key": k, "id": it["id"], "pass": pass_name, "model": self.cfg["hf_id"],
                       "revision": self.cfg.get("revision"), "text": o.text,
                       "n_prompt_tokens": len(out.prompt_token_ids), "n_gen_tokens": len(o.token_ids),
                       "finish_reason": o.finish_reason}
                if o.logprobs:
                    mass, total = first_token_probs(o.logprobs[0], options)
                    row["first_token_mass"] = mass
                    row["first_token_total"] = total
                    top = sorted(o.logprobs[0].values(), key=lambda x: -x.logprob)[:5]
                    row["top5"] = [[t.decoded_token, round(t.logprob, 4)] for t in top]
                rows.append(row)
            cache.add_many(rows)
            print(f"[{pass_name}] {min(start + batch, len(todo))}/{len(todo)}", flush=True)
