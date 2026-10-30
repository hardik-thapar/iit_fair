# Phase 6 results review (Reviewer 2)

*2026-10-30. Reviewer 2 (fairness / NLP / statistics), Track 4. I read PROPOSAL.md, lit/gap_analysis.md,
RESEARCH_LOG.md (last two entries), src/analysis.py, every file in results/, design/name_validation_v1.csv
and the figures. I re-read the RQ1/RQ2 files after the lead switched the primary test to the two-way
bootstrap. Every number below was recomputed from `results/` or `results/raw/` with the project's own
functions (scratch scripts only; no project file changed apart from this one).*

## Summary

The pipeline is careful: paired design, logprob P(Yes), same-group controls, two-way bootstrap, a
manipulation check, and caching. The results support a **modest, honest paper**, but several current
claims go further than the data:

- **RQ1.** Effects are small (|mean ΔP| ≤ 2.2 pp). Under the new primary test (two-way bootstrap,
  Holm per model) **10/64** tests are significant, and **8/64** with flagged names removed. The earlier
  "26/64" came from the profile-level sign-flip test. I reproduced it exactly (26 = Holm on
  `p_signflip`). That test ignores the clustering by name, so it was anti-conservative, and that
  number must not appear anywhere. Counting significant cells is less convincing than the
  *direction* evidence. Pooled over 8 models, female swaps flip decisions to Yes 73 times and to No
  18 times (binomial p < 1e-4). Northeast is 89:37 (p < 1e-4) and Sikh 51:25 (p = 0.004). The two
  controls are balanced (36:28, 23:28), and so are caste, South and Christian. This is the strongest
  RQ1 result, and the paper does not report it yet.
- **Caste null and Christian results cannot be interpreted.** The manipulation check shows that no
  model decodes caste (Cannot tell = 100% in English, all 8 models). The forced-choice "decoding" for
  caste is option-position bias: every model gives the same General/OBC split for *every* cell,
  including the reference and the controls. Biblical names with a UP hometown are never labelled
  Christian. Forced choice gives "Hindu" in 123 of 128 cases, so the Christian ΔPs (Qwen3-8B −1.8 pp,
  OLMo −0.7 pp, Holm-significant) are effects of *Biblical/Western-sounding names*, not of Christian
  identity.
- **RQ3a (headline).** Zero of 10,236 identity-swap explanations are labelled A. This does not depend
  on the judge: a keyword search finds **0** occurrences of gender/religion/caste words (gender,
  female, woman, religio*, Muslim, Sikh, Christian, caste, Dalit, reservation, महिला, धर्म, जाति) in
  any explanation. That part is solid. The problem is the **denominator**. Identity flip rates are
  about the same as control flip rates, and flips are almost perfectly predicted by the reference
  margin (AUROC of |P_ref − 0.5| = 0.88–0.99). So "identity-flipped" pairs are mostly near-threshold
  noise, and nothing needs disclosing. As framed, "0% disclosure on flipped pairs" cannot tell
  unfaithfulness apart from absent bias.
- **RQ3b.** At chance, and more clearly so than the authors say. The two apparently above-chance
  models (Qwen3-32B AUROC 0.65, Granite 0.68) are explained by the margin: Spearman ρ(self-prediction
  score, margin) = −0.63 for Granite. Inside the near-threshold band (|P_ref − 0.5| < 0.2), AUROC is
  0.39–0.58 for every model. The predicted-change rate is a model-specific response style, from 0%
  (Sarvam, Qwen3-32B, OLMo) to 40% (Qwen3-4B), and it is the same for identity and control swaps.
- **RQ2.** Mostly inconclusive. Only 34/64 cells fall inside a ±2 pp equivalence bound, and that
  bound is as large as the largest RQ1 effect, so "equivalent" says little. RQ2 also has a readout
  confound for Granite and Sarvam (below) and a script confound (Latin-script names in Hindi text).
- **RQ4.** No monotone trend over Qwen3 4B→32B. 14B is the most decisive model (strong-tier P_ref =
  1.000), and this alone shrinks its ΔP. Model decisiveness is confounded with size.

## Major issues (ranked)

### M1. RQ3a's denominator is mostly noise, so 0% disclosure is not yet evidence of unfaithfulness
- Identity vs control flip rates are close for every model (e.g. Qwen3-8B 4.4 vs 3.5%, Granite
  0.4 vs 0.3% in English). `auroc_margin_baseline` is 0.88–0.99 in `rq3b_selfprediction.csv`.
- Only 13–82% of "identity-flipped" pairs replicate in the explanation pass
  (`identity_flipped_replicated`: Granite 13/38, Qwen3-32B 43/95). The explanation therefore usually
  justifies a *different* decision from the one that flipped. Reason-first generation flips 5–12% of
  pairs, versus 0.3–4.5% in the decision pass, and the identity and control rates are similar
  (Qwen3-32B 9.3 vs 9.3%, Qwen3-4B 6.6 vs 6.5%).
- The explanation describes the variant alone and never sees the counterfactual, so an RLHF'd model
  would almost never write "because she is a woman" even if biased. The measure has no variance (0
  everywhere), so CCT is undefined, as `rq3a_cct.csv` shows.
- **Cheap fix:** reframe RQ3a around the attributes with *directional* evidence (female, Northeast,
  Sikh). The claim becomes: "Across 8 models, gender swaps produce 55 more to-Yes than to-No flips
  [73 − 18], and Northeast swaps 52 more [89 − 37]. In 0 of the corresponding explanations is gender or
  region given as a reason." Estimate the *excess* number of identity-caused flips (identity minus
  control), not the raw flipped set. Add a paired ref-vs-variant explanation comparison (see A3).
  Report the "explicit denial" pattern ("his hometown … not relevant") as its own descriptive category.

### M2. Two attributes have a signal that was never established (caste, Christian), and Sikh is fragile
- Caste: abstention is 100%. Forced choice gives identical splits for the reference, the controls,
  the caste cells and the gender cell: Granite General 8 / ST 8, OLMo General 8 / OBC 8, Ministral
  almost always OBC. That is letter-position preference, not decoding. `ref_forced_accuracy_en` for
  caste ranges from 0.0 to 1.0, which confirms it. The caste null is therefore "not noticed or not
  admitted", which is exactly the ambiguity the manipulation check was added to resolve (gap_analysis
  §5.2).
- Christian: in reverse option order, Granite answers "Hindu" 8/8 for Samuel Thomas, Joel John and the
  rest, and "Christian" is never chosen in either order by any model. The Christian cell is
  operationally "Biblical first name and surname, UP hometown, read as Hindu or unknown".
- Sikh: all 8 names are "<X> Singh", and four first names are gender-ambiguous (Naampy share female
  0.46–0.70: Gurpreet, Harpreet, Manpreet, Jaspreet). With flagged names excluded, Qwen3-4B Sikh
  (p_holm 0.036 → 0.131) and Sarvam Sikh drop out. The positive Sikh shift may partly be the gender
  effect leaking through.
- **Cheap fix:** in every RQ1/RQ3 table, mark caste and Christian as "signal not decodable; null not
  interpretable as fairness". Compute forced-choice *discrimination* (variant vs reference
  letter-share difference, or AUROC on the target-option logprob) instead of forced accuracy. Report
  RQ3 on the decoded subset per model, as gap_analysis promised; `manip_per_name.csv` already allows it.

### M3. Statistical framing of RQ1: sign-flip vs bootstrap, nesting, and multiplicity
- With the old primary test, sign-flip and bootstrap disagreed: 26 vs 10 Holm-significant cells, and
  in 19/64 cells the CI excluded 0. The sign-flip permutes 150 profiles as if exchangeable, but each
  profile carries **one** name position, so names (8 per cell) are nested in profiles and the real
  replication unit for "this group of names" is 8. The bootstrap is the right primary test. Report
  the sign-flip only as a per-profile, fixed-names test, or drop it.
- A percentile bootstrap that resamples 8 name clusters can still under-cover.
- Holm is applied per model (8 tests). Across the 64-cell table there is no familywise or FDR
  control.
- Significance tests raw ΔP, but the paper's noise-floor logic is "excess over control". Sarvam's
  `control_fullname` is +0.49 pp (CI excludes 0) and Qwen3-32B's `control_surname` is −0.44 pp (CI
  excludes 0), so raw ΔP and excess disagree: Sarvam Sikh excess CI includes 0, and Qwen3-32B OBC/SC
  are significant only as excess.
- **Cheap fix:** primary = bootstrap on *excess over control* (already computed: `excess_lo/hi`). Add
  a leave-one-name-out jackknife for the 10 significant cells. Add BH-FDR over all 64 cells. Add a
  cross-model random-effects pooled ΔP per attribute plus a sign-consistency count (female: 8/8 models
  positive; Northeast: 7/8).

### M4. Effect-size scale: ΔP is compressed near 0/1, and the noise floor differs by model
- Qwen3-14B strong-tier P_ref = 1.000 and its strong-tier ΔP = 0.00 for every attribute. Qwen3 models
  have only 24–31 of 600 pairs per attribute with 0.1 < P_ref < 0.9 (Qwen3-32B 153, Ministral 307).
  Mean ΔP over all pairs mixes "how biased" with "how decisive". This drives RQ4 (14B looks fairest
  because it is the most saturated). It also makes "≤ 2.2 pp" sound smaller than it is: borderline-tier
  ΔP for female is 2.0–2.7 pp in Qwen3-4B/32B and Sarvam, and Northeast is 2.9 pp.
- The mid-band is also where controls move most (Qwen3-4B `control_fullname` mid-band ΔP = 12.8 pp,
  n = 28), so a mid-band analysis needs its own control.
- **Cheap fix:** report Δlog-odds (computed from logprobs, clipped at 1e-4) and borderline-tier ΔP
  next to raw ΔP, and redo RQ4 on these.

### M5. Readout and language confounds in RQ2
- Granite uses the full-candidate readout for **all 3,300 Hindi** items and the first-token readout for
  all English ones. Sarvam uses the full-candidate readout for 2,398 items. RQ2's Hindi − English
  difference for these models therefore partly compares two readouts with different calibration.
  Within-pair mixing is rare but harmful. Ministral has 0.4% mixed pairs with mean |ΔP| = 40 pp,
  against 0.9 pp for matched pairs: these are pure artefacts and can create spurious flips. Sarvam has
  0.8% mixed pairs.
- Hindi prompts keep names and hometowns in Latin script, which makes the name the most salient
  token in the prompt. The manipulation check shows decoding *changes* in Hindi: OLMo region 100% →
  0%, Granite Northeast 100% → 0%, Qwen3-4B Northeast 100% → 25%. RQ2 differences may therefore
  reflect signal strength, not language-specific bias.
- Noise floors differ by language (Qwen3-8B control flips 3.5% EN vs 0.7% HI; Granite 0.3% vs 2.5%).
- **Cheap fix:** `rescore.py` already scored the full candidates in both languages for all decision
  prompts. Rerun the analysis with the full-candidate readout everywhere, as primary or sensitivity.
  Report RQ2 conditional on per-language decoding. Name the condition "Hindi template, Latin-script
  names".

### M6. Region (and gender) controls do not match the manipulation
- Region swaps change the name **and** the hometown (Lucknow → Chennai/Guwahati). Both controls keep
  the hometown, so nothing measures the noise of a hometown change. The Northeast uplift could be a
  hometown effect (Assam towns), a rare/long-name effect (Bhaskarjyoti, Dhrubajyoti) or an ethnicity
  effect. All South names are Brahmin-coded and all Northeast names are Assamese caste-Hindu, so
  "region" means "region holding high caste roughly fixed". That is good design, but it must be said.
- Gender swaps the first name, while its control (`control_surname`) swaps the surname. No control
  swaps the first name within gender.
- **Cheap fix:** report the gender excess against `control_fullname` as well; Qwen3-4B's gender excess
  then shrinks, because control_fullname is +0.82. State the region confound plainly. If one GPU
  experiment is run, run G1.

### M7. Judge validity and Granite truncation
- The rubric's B ("name, hometown or personal background") absorbs about 80% of explanations in both
  languages. "Background" alone appears 998 times, so the lenient rate (55–100%) is meaningless and
  should be dropped.
- The judge labels "from Tezpur, Assam" / "from Chennai, Tamil Nadu" restatements as B, although the
  rubric defines region/state of origin as A. These are restatements, not attributions, so the rubric
  must separate *mentions* from *gives as a reason*.
- The 200-item human sheet is not labelled yet. With 0 positives, kappa will be degenerate, so the
  validation set has to be enriched with positives.
- Granite: 302 explanations are still at `finish_reason=length` after the 768-token rerun, and 201
  have no parseable "Decision:". These count in `identity_flipped` but not in the replicated set.
- **Cheap fix:** report the keyword zero-hit counts as judge-independent evidence. Run a 2-label
  rubric (attribute *cited as a reason* / not) on the human sheet, enriched with about 30 synthetic
  positive explanations so that kappa is defined. Exclude truncated or undecided explanations, or
  report them separately for Granite.

## Minor
- `summary.json` (`n_sig_holm` = 10) is now consistent. Make sure no text still says 26/64.
- RQ2 `tost_equiv_2pp` uses the 95% CI; TOST at α = .05 uses the 90% CI. This is conservative, so
  just say so. A ±1 pp bound would be more informative.
- The pooled flip-direction counts treat models as independent, but they share profiles and names.
  Report them per model as well (female is to-Yes-dominant in 7/8 models individually).
- `KW` includes "state" and "hometown" for region, which matches neutral restatements. The name check
  in the keyword detector is dead code (`... and False`).
- Fig 1: the title is cut off, and it plots raw ΔP, not excess. Add the control band or plot excess.
- Fig 4 shows only zero bars. Replace it with a small table (n flipped, n excess flips, keyword hits,
  judge A) or show the denial rate.
- Fig 5: the symlog axis hides that three models predict ~0 changes. Use a linear axis or a table.
- Fig 6: forced accuracy for caste is an artefact (M2). Show abstention and forced *discrimination*
  instead.
- The SES manipulation item gives 0% "lower income" for every cell, so it is uninformative about a
  class confound. Do not cite it as evidence that names carry no class signal.
- Names are nested in profiles, so per-name ΔP mixes name and profile effects. Say so if per-name
  results are shown.
- The reference is a single privileged intersection (UP Brahmin male). All effects are relative to
  it. Say this in the abstract-level claims ("female-coded vs Brahmin-male-coded").
- The log says checkpoints (a) and (b) were waived and the names and translations are unvalidated
  v1. Put this in the limitations section, not only in the log.

## Suggested cheap analyses (ranked; no GPU)
1. **Flip-direction asymmetry and cross-model pooling.** Per attribute: to-Yes vs to-No flips
   against both controls, per model and pooled (binomial/McNemar). Random-effects pooled ΔP and
   excess across the 8 models, with sign-consistency counts. This is already partly computed above
   (female 73:18, Northeast 89:37, Sikh 51:25; controls balanced). It replaces cell-counting with a
   claim reviewers will accept.
2. **Uniform readout plus decisiveness-robust scales.** Recompute RQ1/RQ2/RQ4 with the full-candidate
   readout everywhere (it exists for all prompts), and report Δlog-odds and borderline-tier ΔP. This
   fixes the Ministral/Sarvam mixed-readout artefacts, the Granite/Sarvam RQ2 readout confound, and
   the RQ4 decisiveness confound.
3. **RQ3a re-slice on paired explanations.** Reference explanations exist (about 570 per model).
   For identity vs control pairs, compare the reasons cited (set difference of cited fields: CGPA,
   percentile, income…), length, hedging and the "not relevant" denial rate. Compute
   explanation-pass flips (ref vs variant "Decision:") and disclosure on those. Restrict to
   attributes with directional evidence and to the excess-flip count. Drop truncated Granite
   explanations. Report keyword zero-hits.
4. **Margin-controlled self-prediction.** Fit logistic(flip ~ margin + self-prediction score) per
   model; compute AUROC inside the near-threshold band (already 0.39–0.58); test whether the
   self-prediction score separates identity from control swaps on the same profile. This turns RQ3b
   into "no introspective signal beyond the margin" rather than "chance".
5. **Name-level robustness and decoded-subset analysis.** Leave-one-name-out jackknife for the 10
   significant cells. Gender excess against `control_fullname`. RQ1/RQ3 restricted to names each model
   decodes (`manip_per_name.csv`). Forced-choice discrimination instead of accuracy. Relabel caste and
   Christian as signal-not-established.

## At most one GPU experiment (≤ 20 GPU-min)
**G1. Name × hometown decomposition for region** (the most novel RQ1 finding, and currently
confounded):
- Add 2 cells: Northeast names + UP hometown, and reference names + Assam hometown (same name
  positions and profiles).
- Size: 2 × 150 × 2 templates × 2 langs = 1,200 single-token decision prompts per model, × 8 models
  ≈ 9,600 prompts. At run 1's throughput (6,600 decision prompts per model in minutes) this is well
  under 20 min.
- Optional, if budget remains: one first-name-only male control cell (fixes M6 for gender).
- Do not spend GPU on more explanations or self-prediction; those RQs are limited by design, not by n.

## Suggested framing of each RQ answer (one honest sentence each)
- **RQ1:** Name-coded identity shifts open-weight models' yes/no decisions only slightly (≤ ~2 pp
  mean, ~3 pp on borderline profiles), but consistently in one direction: female-coded and
  Assamese-coded applicants are pushed toward Yes across most models. Caste-coded surnames show no
  shift, and the models also never recognised caste from the surname, so this null says nothing
  about fairness.
- **RQ2:** Switching the template to Hindi (with Latin-script names) changes both decisiveness and
  the noise floor, but we find no consistent language-specific increase in identity effects. About
  half the cells are equivalent within ±2 pp and the rest are inconclusive.
- **RQ3a:** In more than 10,000 explanations, including those for pairs where identity measurably
  pushed decisions in one direction, no model ever cited gender, religion, caste or region as a
  reason. Because most individual flips are near-threshold noise, this shows that explanations are
  uninformative about identity effects, not that every flip was unfaithfully explained.
- **RQ3b:** Asked whether a name change would alter its decision, each model gives a fixed,
  model-specific answer rate that is the same for identity and same-group swaps and carries no
  information beyond the reference margin. Models cannot report their own counterfactual
  sensitivity.
- **RQ4:** Across Qwen3 4B–32B there is no monotone relation between scale and identity effects. The
  apparent differences track how decisive each model is more than its size.
