# Project summary (first draft stage, 2026-10-30)

Every number below comes from `results/key_numbers.md`, which names its source file.

## What was done
- **Literature:** 65 verified references (`paper/refs.bib`, checks in `lit/ref_check.csv`), with a
  gap analysis in `lit/gap_analysis.md`. Nobody had run our exact study. The closest paper is
  arcuschin2026biases (ICML 2026), which studied Western markers and had no self-prediction or
  Hindi, so our headline is narrowed to RQ3 under implicit Indian name signals.
- **Benchmark:** 150 synthetic applications (hiring, loan, scholarship) × 11 name variants ×
  2 templates × English/Hindi = 6,600 decision prompts per model.
- **Models:** 8 official open-weight models: Qwen3 at 4B, 8B, 14B and 32B, Granite-3.3-8B,
  OLMo-3-7B, Ministral-8B and Sarvam-M-24B. The judge is Mistral-Small-24B.
- **Compute:** 131.6 GPU-minutes (2.19 h) on one MI300X, against a 5 h budget. This includes a
  positive-control run that states identity explicitly. Every job is logged in
  `logs/gpu_budget.csv`.
- **Reviews:** Reviewer 2 ran four times, on the literature review, the spec, the results and
  draft 1. Draft 1 got a weak reject; the fix was the positive control plus calibrated claims.
  An independent fact-check found 33 issues in draft 1, all addressed. In the final draft,
  308 of 308 distinct numbers trace to a results file. All reviews are in `reviews/`.

## Key findings
1. **RQ1, small but systematic shifts.** All 64 attribute×model mean shifts are within 2.16
   points of P(Yes). After Holm correction, 10 of 64 are significant, and 8 of 64 once the
   15 automatically flagged names are dropped. The clearest pattern is the direction of the flips
   that do happen, pooled across models. Female-coded names flip toward "Yes" 73 times against 18
   toward "No", and Northeast-coded names 89 against 37. Same-group controls are balanced (23:28
   and 36:28). In other words, the differential treatment *favours* these names.
2. **Caste: null, but not perceived.** Caste-coded surnames show no detectable effect. Every model
   also answers "Cannot tell" when asked for the caste category of a name (100%). A null
   therefore cannot be read as caste fairness.
3. **RQ3a, headline: explanations are silent.** The judge flagged 1 of 19,615 explanations as
   naming an identity attribute, and none of the 576 explanations where the decision flipped
   after an identity swap. Decisions shift systematically on gender and region signals while the
   explanations never mention them.
4. **RQ3b: self-prediction is uninformative.** Near the decision threshold, models predict their
   own counterfactual flips at chance (AUROC 0.43–0.59). Predicted-change rates range from 0.2% to
   39.5% across models and are similar for identity and control swaps.
5. **Positive control (identity stated explicitly, no name).** Explicit caste labels move
   decisions strongly: up to +9.72 points, and every caste flip goes to "Yes" (SC 51:0,
   OBC 34:0). Explanations name explicit caste labels on average 15–26% of the time. So the
   caste null with surnames reflects non-perception, and the silence under names is
   informative. Explicit gender still flips decisions toward "Yes" (35:1) yet is almost never
   mentioned.
6. **RQ2 and RQ4 are mostly null.** For language, 5 of 64 Hindi-vs-English differences are
   significant and 34 of 64 have 95% CIs inside ±2 points. For scale, Qwen3 shows no monotone
   trend from 4B to 32B.

## What is solid
- The pipeline is reproducible: seeds are fixed, model revisions and the container digest are
  pinned, and every output is cached by prompt hash. Regenerating the benchmark gives
  byte-identical prompts.
- Parsing is clean: no item is missing P(Yes), and the probability readout agrees with the
  generated answer 99.0–100% of the time in English.
- The silent-explanation result and the flip-direction result are large and robust. The 10
  significant cells all keep their sign when any single name is dropped.

## What is weak
- The team never validated the name lists or the Hindi translations before the run; that
  checkpoint was waived. 15 of 88 names fail the automated checks.
- Christian-coded names were never read as Christian, so the Christian results do not measure
  religion.
- Hindi prompts keep names in Latin script, and two models were scored with a different method on
  Hindi items than on English items.
- Region swaps change both the name and the hometown, so the two cannot be separated.
- Flips are rare (about 0.3–4% of pairs) and close to the control rates, so the per-model flip
  denominators behind RQ3 are noisy.
- The judge has not yet been checked against human labels (kappa is pending), and 302 Granite
  Hindi explanations are still cut off at 768 tokens.
- Each cell has only 8 names, and the profiles are synthetic.

## Open [TODO]s in the paper
- Author names and affiliations, the release URL, and the human-judge kappa.
- Anything else marked `\TODO` in `paper/main.tex`. Search for "TODO".

## GPU hours used
131.6 minutes (2.19 h) of the 5 h budget.
