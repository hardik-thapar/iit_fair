"""Quick health check of one model's raw outputs (pure Python, no GPU).

Usage: python3 -m src.pilot_check qwen3-4b
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
name = sys.argv[1]
raw = ROOT / "results" / "raw" / name
bench = {json.loads(l)["id"]: json.loads(l) for l in open(ROOT / "data/benchmark/decision.jsonl", encoding="utf-8")}


def rows(f):
    p = raw / f
    return [json.loads(l) for l in open(p, encoding="utf-8")] if p.exists() else []


dec = rows("decision.jsonl")
P, low_mass, agree, n = {}, 0, 0, 0
for r in dec:
    m = r.get("first_token_mass", {})
    tot = m.get("yes", 0) + m.get("no", 0)
    if tot < 0.9:
        low_mass += 1
    if tot > 0:
        P[r["id"]] = m["yes"] / tot
        txt = r["text"].strip().lower()
        if txt.startswith("yes") or txt.startswith("no"):
            n += 1
            agree += (P[r["id"]] >= 0.5) == txt.startswith("yes")
print(f"decision rows {len(dec)}; Yes+No mass<0.9: {low_mass} ({low_mass / max(1, len(dec)):.1%}); "
      f"text parsable {n}; argmax-vs-text agreement {agree / max(1, n):.1%}")
flips, dps = defaultdict(list), defaultdict(list)
refp = []
for i, p in P.items():
    b = bench[i]
    if b["variant"].startswith("ref"):
        refp.append((b["tier"], p))
        continue
    rid = f"{b['profile_id']}|{[c for c in [i.split('|')[1]] if 0] or ''}"
    ref_id = "|".join([b["profile_id"], next(v for v in [x.split('|')[1] for x in P if x.startswith(b['profile_id'] + '|')] if v.startswith('ref')), b["template"], b["lang"]])
    if ref_id in P:
        flips[b["variant"]].append((P[ref_id] >= 0.5) != (p >= 0.5))
        dps[b["variant"]].append(p - P[ref_id])
for tier in ["strong", "borderline", "weak"]:
    v = [p for t, p in refp if t == tier]
    if v:
        print(f"ref P(Yes) {tier}: mean {sum(v) / len(v):.2f} (n={len(v)})")
for k in sorted(flips):
    f, d = flips[k], dps[k]
    print(f"{k:40s} flip {sum(f) / len(f):.1%}  meanΔP {sum(d) / len(d):+.3f}  mean|ΔP| {sum(map(abs, d)) / len(d):.3f}  n={len(f)}")
ex = rows("explain.jsonl")
ok = sum(bool(re.search(r"Decision:\s*\**\s*(Yes|No)", r["text"])) for r in ex)
print(f"explanations {len(ex)}; with parsable 'Decision:' {ok}; truncated {sum(r['finish_reason'] == 'length' for r in ex)}")
sp = rows("selfpred.jsonl")
spm = sum((r.get("first_token_total") or 0) >= 0.9 for r in sp)
print(f"selfpred {len(sp)}; Yes+No mass>=0.9: {spm}")
ma = rows("manip.jsonl")
print(f"manip {len(ma)}; letter mass>=0.9: {sum((r.get('first_token_total') or 0) >= 0.9 for r in ma)}")
if ex:
    print("--- sample explanation:\n" + ex[0]["text"][:600])
