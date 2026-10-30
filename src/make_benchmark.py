"""Build the benchmark: profiles, name-position assignment and all prompts.

Usage: python -m src.make_benchmark            (writes data/benchmark/*.jsonl)
Follows design/spec.md §2 (profiles), §2.5 (name rotation), §3 (variants), §7 (passes).
Everything is seeded; re-running gives byte-identical files.
"""
import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "benchmark"
T = json.loads((ROOT / "configs" / "templates.json").read_text())
SEED = 20261030
SCENARIOS = ["S1", "S2", "S3"]
TEMPLATES = ["T1", "T2"]
LANGS = ["en", "hi"]
N_PER_SCENARIO = 50
ATTRS = {"S1": ["college", "cgpa", "coding", "projects", "internship"],
         "S2": ["income", "foir", "cibil", "tenure", "multiple"],
         "S3": ["c10", "c12", "apt", "fam_income", "extras"]}
BANDS = {  # (strong, mid, weak) ranges from spec §2.2
    "cgpa": [(8.5, 9.5), (7.0, 8.0), (5.8, 6.6)], "coding": [(85, 98), (55, 75), (15, 40)],
    "income": [(75000, 120000), (35000, 50000), (18000, 26000)], "foir": [(0.0, 0.10), (0.30, 0.40), (0.50, 0.60)],
    "cibil": [(770, 830), (690, 730), (600, 650)], "multiple": [(1, 2), (4, 6), (9, 12)],
    "c10": [(93, 98), (82, 88), (68, 75)], "c12": [(92, 98), (80, 86), (65, 72)], "apt": [(90, 99), (60, 75), (20, 45)],
    "fam_income": [(1.5, 3.0), (4.5, 6.0), (7.0, 7.9)],
}
LEVEL = {"strong": 0, "mid": 1, "weak": 2}
POINTS = {"strong": 2, "mid": 1, "weak": 0}


def ordinal(n):
    n = int(n)
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def inr(n):
    """Indian digit grouping: 120000 -> 1,20,000."""
    s = str(int(round(n)))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts) + "," + tail


def tier_plan(rng):
    """Return a list of 50 band-level dicts per spec §2.3: 25 borderline, 13 strong, 12 weak."""
    plans = []
    for tier, n in [("strong", 13), ("weak", 12)]:
        for _ in range(n):
            lv = {i: tier for i in range(5)}
            if rng.random() < 0.5:
                lv[int(rng.integers(5))] = "mid"
            plans.append(("strong" if tier == "strong" else "weak", "-", lv))
    for i in range(25):
        if i < 13:  # mixed: k strong, k weak, rest mid
            k = int(rng.choice([1, 2]))
            idx = rng.permutation(5)
            lv = {int(j): "mid" for j in idx}
            for j in idx[:k]:
                lv[int(j)] = "strong"
            for j in idx[k:2 * k]:
                lv[int(j)] = "weak"
            plans.append(("borderline", "mixed", lv))
        else:
            plans.append(("borderline", "uniform", {j: "mid" for j in range(5)}))
    order = rng.permutation(len(plans))
    return [plans[i] for i in order]


def draw(rng, attr, level):
    lo, hi = BANDS[attr][LEVEL[level]]
    return float(rng.uniform(lo, hi))


def make_profile(rng, scen, pid, tier, sub, lv):
    names = ATTRS[scen]
    L = {names[i]: lv[i] for i in range(5)}
    v = {"profile_id": pid, "scenario": scen, "tier": tier, "subtier": sub, "levels": L,
         "band_score": sum(POINTS[x] for x in L.values())}
    if scen == "S1":
        v["age"] = int(rng.integers(21, 24))
        c = L["college"]
        v["college_key"] = (("top50" if rng.random() < 0.5 else "51_100") if c == "strong"
                            else "101_200" if c == "mid" else "unranked")
        v["cgpa"] = round(draw(rng, "cgpa", L["cgpa"]), 2)
        v["coding_percentile"] = int(round(draw(rng, "coding", L["coding"])))
        np_ = {"strong": 3, "mid": 2, "weak": 0}[L["projects"]]
        v["project_idx"] = sorted(int(i) for i in rng.choice(6, size=np_, replace=False)) if np_ else []
        it = L["internship"]
        v["intern_level"] = it
        v["intern_months"] = int(rng.integers(4, 7)) if it == "strong" else int(rng.integers(1, 3)) if it == "mid" else 0
    elif scen == "S2":
        v["age"] = int(rng.integers(26, 39))
        income = round(draw(rng, "income", L["income"]) / 1000) * 1000
        v["income"] = income
        v["emi"] = int(round(income * draw(rng, "foir", L["foir"]) / 100) * 100)
        v["cibil"] = int(round(draw(rng, "cibil", L["cibil"])))
        t = L["tenure"]
        if t == "weak":
            v["tenure_unit"], v["tenure_n"] = "months", int(rng.integers(3, 9))
        else:
            v["tenure_unit"], v["tenure_n"] = "years", int(rng.integers(4, 9)) if t == "strong" else int(rng.integers(1, 3))
        v["amount"] = int(round(income * draw(rng, "multiple", L["multiple"]) / 10000) * 10000)
        v["job_idx"] = int(rng.integers(4))
        v["purpose_idx"] = int(rng.integers(3))
    else:
        v["age"] = int(rng.integers(17, 19))
        v["c10"] = round(draw(rng, "c10", L["c10"]), 1)
        v["c12"] = round(draw(rng, "c12", L["c12"]), 1)
        v["apt_percentile"] = int(round(draw(rng, "apt", L["apt"])))
        v["fam_income"] = round(draw(rng, "fam_income", L["fam_income"]), 1)
        v["course_idx"] = int(rng.integers(4))
        e = L["extras"]
        if e == "strong":
            v["extras_idx"] = sorted(int(i) for i in rng.choice(5, size=2, replace=False))
            v["extras_state"] = True
        elif e == "mid":
            v["extras_idx"] = sorted(int(i) for i in rng.choice(5, size=int(rng.integers(1, 3)), replace=False))
            v["extras_state"] = False
        else:
            v["extras_idx"], v["extras_state"] = [], False
    return v


def fill_app(p, lang, full_name, hometown):
    P = T["pools"]
    s = p["scenario"]
    f = {"full_name": full_name, "hometown": hometown, "age": p["age"]}
    if s == "S1":
        f["college_band"] = P["college"][p["college_key"]][lang]
        f["cgpa"] = f"{p['cgpa']:.2f}"
        f["coding_percentile"] = p["coding_percentile"]
        f["coding_percentile_ord"] = ordinal(p["coding_percentile"])
        f["projects"] = ("; ".join(P["projects"][lang][i] for i in p["project_idx"]) if p["project_idx"]
                         else P["project_weak"][lang])
        lvl, n = p["intern_level"], p["intern_months"]
        key = "mid1" if (lvl == "mid" and n == 1) else lvl
        f["internships"] = P["internship"][key][lang].replace("{n}", str(n))
    elif s == "S2":
        f["job_title"] = P["job_title"][lang][p["job_idx"]]
        unit = "tenure_years" if p["tenure_unit"] == "years" else "tenure_months"
        n = p["tenure_n"]
        txt = P[unit][lang].replace("{n}", str(n))
        if lang == "en" and n == 1:
            txt = txt.replace("years", "year").replace("months", "month")
        if lang == "hi" and n == 1 and unit == "tenure_months":
            txt = "1 महीना"
        f["tenure_text"] = txt
        f["income"], f["emi"], f["amount"] = inr(p["income"]), inr(p["emi"]), inr(p["amount"])
        f["cibil"] = p["cibil"]
        f["purpose"] = P["purpose"][lang][p["purpose_idx"]]
    else:
        f["c10"], f["c12"] = f"{p['c10']:.1f}", f"{p['c12']:.1f}"
        f["apt_percentile"], f["apt_percentile_ord"] = p["apt_percentile"], ordinal(p["apt_percentile"])
        f["fam_income"] = f"{p['fam_income']:.1f}"
        f["course"] = P["course"][lang][p["course_idx"]]
        items = ([P["extras_state"][lang][0]] if p["extras_state"] else []) + [P["extras_other"][lang][i] for i in p["extras_idx"]]
        f["extras"] = "; ".join(items) if items else P["none"][lang]
    return T["app"][s][lang].format(**f)


def decision_prompt(p, tmpl, lang, full_name, hometown, explain=False):
    w = T["wrappers"][p["scenario"]][tmpl][lang]
    answer = T["explain_instruction"][lang] if explain else w["answer"]
    return f"{w['intro']}\n\n{fill_app(p, lang, full_name, hometown)}\n\n{w['question']} {answer}"


def load_names():
    rows = list(csv.DictReader(open(ROOT / "design" / "name_pools.csv", encoding="utf-8")))
    pools = {}
    for r in rows:
        pools.setdefault(r["cell"], {})[int(r["pos"])] = r
    return pools


def name_fields(row, lang):
    # v1 run: names and hometowns stay in Latin script in Hindi prompts too (documented limitation)
    return row["full_name_en"], row["hometown"]


def assign_positions(profiles, n_pos):
    """Spec §2.5: stratified cyclic assignment within (scenario, tier)."""
    out = {}
    for si, s in enumerate(SCENARIOS, start=1):
        rng = np.random.default_rng(SEED + 1 + si)
        for tier in ["strong", "borderline", "weak"]:
            ids = [p["profile_id"] for p in profiles if p["scenario"] == s and p["tier"] == tier]
            ids = [ids[i] for i in rng.permutation(len(ids))]
            offset = int(rng.integers(n_pos))
            for i, pid in enumerate(ids):
                out[pid] = (offset + i) % n_pos
    return out


def pilot_ids(profiles):
    """Spec §10: per scenario 3 borderline, 1 strong, 1 weak."""
    rng = np.random.default_rng(SEED + 3)
    chosen = []
    for s in SCENARIOS:
        for tier, k in [("borderline", 3), ("strong", 1), ("weak", 1)]:
            ids = sorted(p["profile_id"] for p in profiles if p["scenario"] == s and p["tier"] == tier)
            chosen += [ids[i] for i in sorted(rng.choice(len(ids), size=k, replace=False))]
    return set(chosen)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    profiles = []
    for si, s in enumerate(SCENARIOS, start=1):
        rng = np.random.default_rng(SEED + si)
        for i, (tier, sub, lv) in enumerate(tier_plan(rng), start=1):
            profiles.append(make_profile(rng, s, f"{s}-P{i:03d}", tier, sub, lv))
    pools = load_names()
    n_pos = min(len(v) for v in pools.values())
    pos = assign_positions(profiles, n_pos)
    pilot = pilot_ids(profiles)
    cells = [c for c in pools if c != "ref"] if "ref" in pools else list(pools)
    ref_cell = "ref" if "ref" in pools else [c for c in pools if c.startswith("ref")][0]
    with open(OUT / "profiles.jsonl", "w", encoding="utf-8") as f:
        for p in profiles:
            p["name_pos"], p["pilot"] = pos[p["profile_id"]], p["profile_id"] in pilot
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    n = 0
    with open(OUT / "decision.jsonl", "w", encoding="utf-8") as f:
        for p in profiles:
            for cell in [ref_cell] + [c for c in cells if c != ref_cell]:
                row = pools[cell][p["name_pos"]]
                for t in TEMPLATES:
                    for lang in LANGS:
                        full, town = name_fields(row, lang)
                        item = {"id": f"{p['profile_id']}|{cell}|{t}|{lang}", "profile_id": p["profile_id"],
                                "scenario": p["scenario"], "tier": p["tier"], "variant": cell, "template": t,
                                "lang": lang, "name_pos": p["name_pos"], "pilot": p["pilot"],
                                "full_name": full, "hometown": town,
                                "messages": [{"role": "user", "content": decision_prompt(p, t, lang, full, town)}],
                                "explain_messages": [{"role": "user", "content": decision_prompt(p, t, lang, full, town, explain=True)}]}
                        f.write(json.dumps(item, ensure_ascii=False) + "\n")
                        n += 1
    # manipulation check: one block per unique (cell, pos), both languages, both option orders
    m = 0
    with open(OUT / "manip.jsonl", "w", encoding="utf-8") as f:
        for cell, rows in pools.items():
            for k, row in rows.items():
                for lang in LANGS:
                    full, town = name_fields(row, lang)
                    for dim, d in T["manip"]["dimensions"].items():
                        for order in ["fwd", "rev"]:
                            opts = list(d["options"][lang])
                            if order == "rev":
                                opts = opts[::-1]
                            opts.append(T["manip"]["cannot_tell"][lang])
                            letters = "ABCDEFGH"[:len(opts)]
                            opt_txt = "\n".join(f"{l}. {o}" for l, o in zip(letters, opts))
                            txt = T["manip"]["stem"][lang].format(full_name=full, hometown=town,
                                                                 dimension=d[lang], options=opt_txt)
                            canon = list(d["options"]["en"]) if order == "fwd" else list(d["options"]["en"])[::-1]
                            canon.append("Cannot tell")
                            f.write(json.dumps({"id": f"{cell}|{k}|{lang}|{dim}|{order}", "variant": cell, "name_pos": k,
                                                "lang": lang, "dim": dim, "order": order,
                                                "letter_map": dict(zip(letters, canon)),
                                                "messages": [{"role": "user", "content": txt}]},
                                               ensure_ascii=False) + "\n")
                            m += 1
    print(f"{len(profiles)} profiles ({len(pilot)} pilot), {n_pos} name positions, {len(pools)} cells, "
          f"{n} decision prompts, {m} manipulation prompts")


if __name__ == "__main__":
    main()
