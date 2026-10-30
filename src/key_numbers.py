"""Collect every number the paper may quote into results/key_numbers.md, each with its source.

Usage: .venv/bin/python -m src.key_numbers
The Writer may only use numbers that appear in this file (or directly in results/*.csv).
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
MODELS = ["qwen3-4b", "qwen3-8b", "qwen3-14b", "qwen3-32b", "granite-3.3-8b", "olmo-3-7b", "ministral-8b", "sarvam-m"]
ATTR = ["gender_female", "religion_muslim", "religion_sikh", "religion_christian", "caste_obc", "caste_sc",
        "region_south", "region_northeast"]
out = []


def h(t):
    out.append(f"\n## {t}\n")


def line(t, src):
    out.append(f"- {t}  `[src: {src}]`")


def pp(x):
    return f"{100 * x:+.2f} pp"


# budget
b = pd.read_csv(ROOT / "logs" / "gpu_budget.csv")
h("Compute")
line(f"Total GPU minutes logged: {b.minutes.sum():.1f} ({b.minutes.sum() / 60:.2f} h) over {len(b)} jobs", "logs/gpu_budget.csv minutes")
for task in ["smoke", "run_model", "rescore", "run_judge"]:
    s = b[b.task.str.startswith(task)]
    line(f"{task}: {s.minutes.sum():.1f} min ({len(s)} jobs)", "logs/gpu_budget.csv")

# health
h("Data health (per model)")
hl = pd.read_csv(R / "health.csv")
for _, r in hl.iterrows():
    line(f"{r.model}: n={r.n}; full-candidate scoring used for {r.full_candidate_used} items; missing P(Yes)={r.missing_p}; "
         f"argmax-vs-generated agreement (English) {100 * r.argmax_text_agreement_en:.1f}%; reference P(Yes) strong/borderline/weak "
         f"{r.ref_pyes_strong:.2f}/{r.ref_pyes_borderline:.2f}/{r.ref_pyes_weak:.2f}", "results/health.csv")
line(f"Benchmark: 150 profiles x 11 variants x 2 templates x 2 languages = 6,600 decision prompts per model", "data/benchmark (src/make_benchmark.py)")

# RQ1
h("RQ1 decision shifts (mean ΔP(Yes) vs reference; two-way bootstrap CI; primary test = two-way bootstrap p, Holm over 8 attributes per model)")
r1 = pd.read_csv(R / "rq1_decision_bias.csv")
a = r1[r1.attribute.isin(ATTR)]
line(f"Holm-significant cells: {int(a.sig_holm.sum())} of {len(a)}", "results/rq1_decision_bias.csv sig_holm")
v = pd.read_csv(R / "rq1_decision_bias_validated_names.csv")
v = v[v.attribute.isin(ATTR)]
line(f"With the 15 automatically flagged names removed: {int(v.sig_holm.sum())} of {len(v)} significant", "results/rq1_decision_bias_validated_names.csv")
line(f"Largest |mean ΔP| over all 64 cells: {100 * a.mean_dp.abs().max():.2f} pp", "results/rq1_decision_bias.csv mean_dp")
for _, r in a[a.sig_holm == True].iterrows():  # noqa: E712
    line(f"SIGNIFICANT {r.model} {r.attribute}: ΔP {pp(r.mean_dp)} [{100 * r.ci_lo:+.2f}, {100 * r.ci_hi:+.2f}], Holm p={r.p_holm:.4f}; "
         f"flip rate {100 * r.flip_rate:.1f}% vs matched control {100 * r.ctrl_flip_rate:.1f}%", "results/rq1_decision_bias.csv")
for att in ATTR:
    s = a[a.attribute == att]
    line(f"{att}: ΔP range across models {100 * s.mean_dp.min():+.2f} to {100 * s.mean_dp.max():+.2f} pp; "
         f"models with positive mean ΔP {int((s.mean_dp > 0).sum())}/8; Holm-significant {int(s.sig_holm.sum())}/8",
         "results/rq1_decision_bias.csv")
c = r1[r1.attribute.str.startswith("control")]
line(f"Control swaps: mean ΔP range {100 * c.mean_dp.min():+.2f} to {100 * c.mean_dp.max():+.2f} pp; flip rate range "
     f"{100 * c.flip_rate.min():.1f}-{100 * c.flip_rate.max():.1f}%", "results/rq1_decision_bias.csv control rows")
d = pd.read_csv(R / "rq1_direction.csv")
h("RQ1 direction of flips pooled over the 8 models (binomial test vs 50:50; Holm over 8 identity attributes)")
for _, r in d.iterrows():
    line(f"{r.attribute}: {r.flips_to_yes} flips to Yes vs {r.flips_to_no} to No ({100 * r.share_to_yes:.1f}% to Yes), "
         f"binomial p={r.p_binom:.2g}" + (f", Holm p={r.p_holm_identity:.2g}" if pd.notna(r.p_holm_identity) else "")
         + f"; models with positive mean ΔP {r.models_positive_mean_dp}/8", "results/rq1_direction.csv")
e = pd.read_csv(R / "rq1_excess.csv")
line(f"Excess over matched control: Holm-significant {int((e.p_holm_model < .05).sum())}/64; BH q<.05 across all 64: "
     f"{int((e.q_bh_all64 < .05).sum())}; raw ΔP BH q<.05 across all 64: {int((e.q_bh_all64_raw_dp < .05).sum())}", "results/rq1_excess.csv")
dn = pd.read_csv(R / "rq1_drop_one_name.csv")
line(f"Drop-one-name: {int((dn.same_sign_when_dropping_each_name == 8).sum())} of {len(dn)} significant cells keep their sign "
     f"when any single name position is dropped", "results/rq1_drop_one_name.csv")
bl = pd.read_csv(R / "rq1_borderline.csv")
for att in ["gender_female", "region_northeast"]:
    s = bl[bl.attribute == att]
    line(f"{att}: mean ΔP over models, all profiles {100 * s.dp_all.mean():+.2f} pp; borderline profiles {100 * s.dp_borderline.mean():+.2f} pp; "
         f"near threshold (|P_ref-0.5|<0.3) {100 * s.dp_near_threshold.mean():+.2f} pp", "results/rq1_borderline.csv")

# RQ2
h("RQ2 language (Hindi minus English excess-over-control ΔP; two-way bootstrap; Holm per model; TOST ±2 pp)")
r2 = pd.read_csv(R / "rq2_language.csv")
line(f"Holm-significant language differences: {int((r2.p_holm < .05).sum())}/64; 95% CI entirely inside ±2 pp (conservative TOST-style equivalence): "
     f"{int(r2.tost_equiv_2pp.sum())}/64", "results/rq2_language.csv")
for _, r in r2[r2.p_holm < .05].iterrows():
    line(f"SIGNIFICANT {r.model} {r.attribute}: Hindi-English {pp(r.hi_minus_en_excess)} [{100 * r.lo:+.2f}, {100 * r.hi:+.2f}]",
         "results/rq2_language.csv")
fl = pd.read_csv(R / "flip_rates_by_language.csv")
for _, r in fl.iterrows():
    line(f"{r.model} {r.lang}: identity flip {100 * r.identity_flip_rate:.2f}%, control flip {100 * r.control_flip_rate:.2f}%",
         "results/flip_rates_by_language.csv")

# RQ3a
h("RQ3a disclosure (judge label A = names an identity attribute; keyword = attribute words)")
r3 = pd.read_csv(R / "rq3a_disclosure.csv")
tot = r3[r3.set.isin(["identity_flipped", "identity_unflipped", "control_flipped", "control_unflipped"])]
line(f"Explanations of swapped variants analysed: {int(tot.n.sum())}", "results/rq3a_disclosure.csv n")
fl_ = r3[r3.set == "identity_flipped"]
line(f"Identity-flipped explanations: {int(fl_.n.sum())}; strict (judge A) rate max over models {100 * fl_.strict_rate.max():.1f}%",
     "results/rq3a_disclosure.csv")
for _, r in r3[r3.set == "identity_flipped"].iterrows():
    line(f"{r.model}: identity-flipped n={r.n}, judge-A {100 * r.strict_rate:.1f}%, keyword {100 * r.keyword_rate:.1f}%, "
         f"mean words {r.words_mean:.0f}", "results/rq3a_disclosure.csv")
j = [json.loads(l) for l in open(R / "raw" / "mistral-small-24b-judge" / "mentions.jsonl")]
labs = [max(x["first_token_mass"], key=x["first_token_mass"].get) for x in j if x.get("first_token_mass")]
line(f"Judge outputs: {len(labs)} explanations judged; A={labs.count('A')}, B={labs.count('B')}, C={labs.count('C')}",
     "results/raw/mistral-small-24b-judge/mentions.jsonl")

# RQ3b
h("RQ3b self-prediction (condition N = counterfactual name only; A = attribute stated)")
s3 = pd.read_csv(R / "rq3b_selfprediction.csv")
for _, r in s3[(s3.group == "identity")].iterrows():
    line(f"{r.model} cond {r.condition}: actual flip {100 * r.actual_flip_rate:.1f}%, predicted change {100 * r.predicted_change_rate:.1f}%, "
         f"balanced acc {r.balanced_accuracy:.3f}, AUROC {r.auroc_selfpred:.3f} (margin baseline {r.auroc_margin_baseline:.3f})",
         "results/rq3b_selfprediction.csv identity rows")
for _, r in s3[(s3.group == "control") & (s3.condition == "N")].iterrows():
    line(f"{r.model} control cond N: predicted change {100 * r.predicted_change_rate:.1f}%", "results/rq3b_selfprediction.csv")
mc = pd.read_csv(R / "rq3b_margin_controlled.csv")
near = mc[mc.band.str.startswith("near")]
line(f"Near threshold (|P_ref-0.5|<0.2), identity pairs: self-prediction AUROC range {near.auroc_selfpred.min():.2f}-{near.auroc_selfpred.max():.2f}; "
     f"margin-only AUROC range {near.auroc_margin.min():.2f}-{near.auroc_margin.max():.2f}", "results/rq3b_margin_controlled.csv")
alls = mc[mc.band == "all"]
line(f"All pairs: self-prediction AUROC range {alls.auroc_selfpred.min():.2f}-{alls.auroc_selfpred.max():.2f}; margin-only AUROC "
     f"{alls.auroc_margin.min():.2f}-{alls.auroc_margin.max():.2f}", "results/rq3b_margin_controlled.csv")

# RQ4
h("RQ4 scale (Qwen3 4B/8B/14B/32B)")
q = ["qwen3-4b", "qwen3-8b", "qwen3-14b", "qwen3-32b"]
for m in q:
    s = a[a.model == m]
    f = fl[fl.model == m]
    line(f"{m}: mean |ΔP| over 8 attributes {100 * s.mean_dp.abs().mean():.2f} pp; Holm-significant {int(s.sig_holm.sum())}/8; "
         f"identity flip rate (avg en/hi) {100 * f.identity_flip_rate.mean():.2f}% vs control {100 * f.control_flip_rate.mean():.2f}%",
         "results/rq1_decision_bias.csv + flip_rates_by_language.csv")

# manipulation check
h("Manipulation check (English; primary = abstention 'Cannot tell'; forced choice from top-20 first-token logprobs, unreliable when abstention ≈ 1)")
mc = pd.read_csv(R / "manip_accuracy.csv").dropna(subset=["accuracy_en"])
for att in ATTR:
    s = mc[mc.cell == att]
    line(f"{att} (dim {s.dim.iloc[0]}): abstention range {100 * s.cannot_tell_rate_en.min():.0f}-{100 * s.cannot_tell_rate_en.max():.0f}%; "
         f"free-answer accuracy range {100 * s.accuracy_en.min():.0f}-{100 * s.accuracy_en.max():.0f}%; forced-choice range "
         f"{100 * s.forced_accuracy_en.min():.0f}-{100 * s.forced_accuracy_en.max():.0f}%", "results/manip_accuracy.csv")
ma = pd.read_csv(R / "manip_answers.csv")
chr_ = ma[(ma.cell == "religion_christian") & (ma.dim == "religion") & (ma.lang == "en")]
line(f"Christian-coded names, forced answers: {dict(chr_.forced.value_counts())}", "results/manip_answers.csv")
ind = pd.read_csv(R / "manip_accuracy.csv")
ind = ind[ind.dim == "indian"]
line(f"'Not Indian' share for any cell, any model: max {100 * ind.share_not_indian.max():.0f}%", "results/manip_accuracy.csv dim=indian")

nv = pd.read_csv(ROOT / "design" / "name_validation_v1.csv")
h("Name validation (Outkast SECC-2011, Naampy electoral rolls)")
line(f"Names flagged by automated checks: {int(nv.auto_check.str.contains('below|ambiguous').sum())} of {len(nv)}", "design/name_validation_v1.csv")

(R / "key_numbers.md").write_text("# Key numbers (auto-generated by src/key_numbers.py; do not edit by hand)\n" + "\n".join(out) + "\n")
print("\n".join(out))
