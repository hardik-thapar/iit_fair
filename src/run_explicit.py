"""Positive control (Reviewer 2, draft review): identity stated EXPLICITLY instead of via names.

No name or hometown: the "Name:" line becomes an applicant ID and the "Hometown:" line is replaced
by a self-declared background line; only one field of that line changes per variant.
English, template T1 only: 150 profiles x 9 variants = 1,350 prompts per model.
Passes: decision (first-token P(Yes)) and a reason-first explanation for EVERY prompt.

Usage: python -m src.run_explicit --model qwen3-4b
Outputs: results/raw/<model>/explicit_decision.jsonl, explicit_explain.jsonl
"""
import argparse
import json
import time

from src.config import ROOT, model_cfg, raw_dir
from src.llm import Cache, Model
from src.make_benchmark import T, fill_app, load_names

REF = {"Gender": "Male", "Religion": "Hindu", "Caste category": "General", "Home region": "North India"}
SWAP = {"ref": {}, "gender_female": {"Gender": "Female"}, "religion_muslim": {"Religion": "Muslim"},
        "religion_sikh": {"Religion": "Sikh"}, "religion_christian": {"Religion": "Christian"},
        "caste_obc": {"Caste category": "OBC"}, "caste_sc": {"Caste category": "SC"},
        "region_south": {"Home region": "South India"}, "region_northeast": {"Home region": "Northeast India"}}


def build():
    profiles = [json.loads(l) for l in open(ROOT / "data/benchmark/profiles.jsonl", encoding="utf-8")]
    pools = load_names()
    ref_cell = [c for c in pools if c.startswith("ref")][0]
    items = []
    for p in profiles:
        row = pools[ref_cell][p["name_pos"]]
        name, town = row["full_name_en"], row["hometown"]
        w = T["wrappers"][p["scenario"]]["T1"]["en"]
        for var, change in SWAP.items():
            fields = dict(REF, **change)
            decl = "Self-declared background: " + "; ".join(f"{k}: {v}" for k, v in fields.items())
            app = (fill_app(p, "en", name, town).replace(f"Hometown: {town}", decl)
                   .replace(f"Name: {name}", f"Applicant ID: {p['profile_id']}"))
            assert decl in app and name not in app
            base = f"{w['intro']}\n\n{app}\n\n{w['question']}"
            items.append({"id": f"{p['profile_id']}|{var}|T1|en|explicit", "profile_id": p["profile_id"],
                          "variant": var, "tier": p["tier"], "scenario": p["scenario"],
                          "messages": [{"role": "user", "content": f"{base} {w['answer']}"}],
                          "explain_messages": [{"role": "user", "content": f"{base} {T['explain_instruction']['en']}"}]})
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    a = ap.parse_args()
    t0 = time.time()
    items = build()
    m = Model(model_cfg(a.model))
    out = raw_dir(a.model)
    m.run(Cache(out / "explicit_decision.jsonl"), "explicit_decision",
          [{"id": i["id"], "messages": i["messages"]} for i in items], max_tokens=4)
    m.run(Cache(out / "explicit_explain.jsonl"), "explicit_explain",
          [{"id": i["id"], "messages": i["explain_messages"]} for i in items], max_tokens=384, logprobs=None)
    print(f"DONE explicit {a.model} in {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
