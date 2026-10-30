"""Extra analyses requested by Reviewer 2 (reviews/phase6_results_review.md). No GPU.

Usage: .venv/bin/python -m src.analysis_extra
Writes results/rq1_direction.csv, results/rq1_excess.csv, results/rq1_borderline.csv,
results/rq1_drop_one_name.csv, results/rq3b_margin_controlled.csv.
"""
import numpy as np
import pandas as pd
from scipy.stats import binomtest

from src.analysis import (ATTR, CTRL, MODELS, RES, ROOT, SEED, auroc, bench, boot_p, boot_weights, est_ci, holm,
                          jl, p_yes_table, pairs)


def bh(ps):
    ps = np.asarray(ps, float)
    n = len(ps)
    order = np.argsort(ps)
    adj = np.empty(n)
    prev = 1.0
    for rank, i in enumerate(order[::-1]):
        k = n - rank
        prev = min(prev, ps[i] * n / k)
        adj[i] = prev
    return adj


def main():
    Bn = bench()
    prof = pd.DataFrame(jl(ROOT / "data/benchmark/profiles.jsonl"))[["profile_id", "scenario", "tier", "name_pos"]]
    prof = prof.sort_values("profile_id").reset_index(drop=True)
    W = boot_weights(prof, np.random.default_rng(SEED))
    allp = {m: pairs(p_yes_table(m, Bn)) for m in MODELS}

    # 1. direction of flips, pooled over models (binomial test against 50:50)
    rows = []
    for a in list(ATTR) + ["control_surname", "control_fullname"]:
        to_yes = sum(int(((v.variant == a) & (v.p_ref < .5) & (v.p >= .5)).sum()) for v in allp.values())
        to_no = sum(int(((v.variant == a) & (v.p_ref >= .5) & (v.p < .5)).sum()) for v in allp.values())
        n = to_yes + to_no
        rows.append({"attribute": a, "flips_to_yes": to_yes, "flips_to_no": to_no,
                     "share_to_yes": to_yes / n if n else np.nan,
                     "p_binom": binomtest(to_yes, n, 0.5).pvalue if n else np.nan,
                     "models_positive_mean_dp": sum(v[v.variant == a].dp.mean() > 0 for v in allp.values())})
    d = pd.DataFrame(rows)
    d["p_holm_identity"] = np.nan
    idx = d.attribute.isin(ATTR)
    d.loc[idx, "p_holm_identity"] = holm(d.loc[idx, "p_binom"].values)
    d.to_csv(RES / "rq1_direction.csv", index=False)
    print(d.round(4).to_string())

    # 2. excess over matched control: bootstrap p, Holm per model and BH across all 64 cells
    rows = []
    for m, v in allp.items():
        for a in ATTR:
            dd = v[v.variant == a].groupby("profile_id").dp.mean().reindex(prof.profile_id).values
            cc = v[v.variant == CTRL[a]].groupby("profile_id").dp.mean().reindex(prof.profile_id).values
            e, lo, hi = est_ci(dd - cc, W)
            rows.append({"model": m, "attribute": a, "excess": e, "lo": lo, "hi": hi, "p_boot": boot_p(dd - cc, W),
                         "p_boot_raw_dp": boot_p(dd, W)})
    ex = pd.DataFrame(rows)
    ex["p_holm_model"] = ex.groupby("model").p_boot.transform(lambda s: holm(s.values))
    ex["q_bh_all64"] = bh(ex.p_boot.values)
    ex["q_bh_all64_raw_dp"] = bh(ex.p_boot_raw_dp.values)
    ex.to_csv(RES / "rq1_excess.csv", index=False)
    print("excess: Holm-sig", int((ex.p_holm_model < .05).sum()), " BH q<.05", int((ex.q_bh_all64 < .05).sum()),
          " raw-dP BH q<.05", int((ex.q_bh_all64_raw_dp < .05).sum()))

    # 3. borderline-only dP and log-odds shift
    rows = []
    eps = 1e-4
    for m, v in allp.items():
        v = v.copy()
        lo_ = lambda p: np.log(np.clip(p, eps, 1 - eps) / (1 - np.clip(p, eps, 1 - eps)))
        v["dlogit"] = lo_(v.p) - lo_(v.p_ref)
        for a in ATTR:
            s = v[v.variant == a]
            b = s[s.tier == "borderline"]
            near = s[(s.p_ref - 0.5).abs() < 0.3]
            rows.append({"model": m, "attribute": a, "dp_all": s.dp.mean(), "dp_borderline": b.dp.mean(),
                         "dp_near_threshold": near.dp.mean(), "n_near_threshold": len(near),
                         "dlogit_all": s.dlogit.mean()})
    pd.DataFrame(rows).to_csv(RES / "rq1_borderline.csv", index=False)

    # 4. drop-one-name stability for cells significant on the primary test
    r1 = pd.read_csv(RES / "rq1_decision_bias.csv")
    sig = r1[r1.sig_holm == True]  # noqa: E712
    rows = []
    for _, r in sig.iterrows():
        v = allp[r.model]
        signs = []
        for k in range(8):
            s = v[(v.variant == r.attribute) & (v.name_pos != k)]
            signs.append(np.sign(s.groupby("profile_id").dp.mean().mean()))
        rows.append({"model": r.model, "attribute": r.attribute, "mean_dp": r.mean_dp,
                     "same_sign_when_dropping_each_name": int(sum(sg == np.sign(r.mean_dp) for sg in signs)),
                     "of": 8})
    pd.DataFrame(rows).to_csv(RES / "rq1_drop_one_name.csv", index=False)
    print(pd.DataFrame(rows).to_string())

    # 5. self-prediction controlled for the decision margin
    rows = []
    for m, v in allp.items():
        sp = {}
        for r in jl(ROOT / "results/raw" / m / "selfpred.jsonl"):
            mm = r.get("first_token_mass") or {}
            tot = mm.get("yes", 0) + mm.get("no", 0)
            if tot >= 0.5:
                sp[r["id"]] = mm["yes"] / tot
        vv = v.copy()
        vv["psp"] = vv.id.map(lambda i: sp.get(f"{i}|N", np.nan))
        vv = vv.dropna(subset=["psp"])
        for band, sub in [("all", vv), ("near_threshold(|p_ref-.5|<.2)", vv[(vv.p_ref - .5).abs() < .2])]:
            idn = sub[sub.variant.isin(ATTR)]
            rows.append({"model": m, "band": band, "n": len(idn), "flips": int(idn.flip.sum()),
                         "auroc_selfpred": auroc(idn.psp.values, idn.flip.values),
                         "auroc_margin": auroc(-np.abs(idn.p_ref.values - .5), idn.flip.values),
                         "pred_change_identity": (idn.psp >= .5).mean(),
                         "pred_change_control": (sub[sub.variant.str.startswith("control")].psp >= .5).mean()})
    pd.DataFrame(rows).to_csv(RES / "rq3b_margin_controlled.csv", index=False)
    print(pd.DataFrame(rows).round(3).to_string())


if __name__ == "__main__":
    main()
