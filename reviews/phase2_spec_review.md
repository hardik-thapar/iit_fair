# Reviewer 2 — Phase 2 experiment-design review

*Reviewed: `PROPOSAL.md`, `lit/gap_analysis.md`, `design/spec.md` (draft v1), `design/templates_en.md`, `design/name_pools.csv`. Read as the methods section of a submitted Track 4 short paper, before any data exists.*

## Summary

The paired design is careful: positions are matched, the reference is narrow and stated, controls exist, a manipulation check is included, the pilot is blinded and the drop order is pre-registered. RQ1 as specified would probably survive review.
The **headline (RQ3)** is the weak part. Explanations are post-hoc rationales of a prefilled decision. The flips they are scored on are mostly noise flips at a 0.5 threshold. Self-prediction can be solved without any identity awareness. As designed, a low mention rate or poor self-prediction would be hard to interpret.
Inference also ignores name-sampling variance (8 names per cell), and two of the four attribute families have no valid matched noise floor. All of these have cheap fixes, and several of them cost no GPU time.

---

## Major issues (ranked)

### M1. RQ3a mention rate is confounded by noise flips and by post-hoc rationalisation

**Problem.**
- (a) The primary RQ3a set is *replicated flips*. Flips are counted at a 0.5 threshold on a borderline-heavy sample, so many identity-pair flips are the same kind of flip that the same-group controls produce. Suppose FR_a = 8% and FR_ctrl = 6%. Then about 75% of the attribute's flips are not attributable to the attribute, and it is not a failure of faithfulness when their explanations do not mention it. MR_a therefore mixes "unfaithful" with "nothing to disclose".
- (b) The explanation pass prefills `Decision:` and asks for a reason afterwards. The reason is a rationalisation conditioned on a fixed answer, so a low mention rate is close to guaranteed. The paper you will be compared with, arcuschin2026biases, scores reasoning that comes *before* the decision. Reviewers will say the result is an artefact of the format.
- (c) Restricting to replicated flips selects pairs whose flip survives a change of prompt format. These are plausibly the stronger effects, which biases MR in an unknown direction relative to "all identity-driven decision changes".

**Why it matters.** RQ3 is the claimed contribution. Under the current design, every outcome has an innocuous explanation.

**Cheap fixes.**
1. Make the **CCT (all sampled pairs, continuous |ΔP|) co-primary** with MR. Report MR *against the control-flip mention baseline* (lenient definition), i.e. MR_a − MR_ctrl. Also report a deconvolved "excess-flip" mention rate, (MR_a·FR_a − MR_c·FR_c)/(FR_a − FR_c), with a bootstrap CI, *only* for (model, attribute) cells whose RQ1 excess is significant. Say explicitly that MR is not interpreted where there is no excess.
2. Use a **reason-first format** ("Reason: … Decision: …"; no decision prefill) as the primary explanation format, or at minimum as a second arm on the flipped pairs. The cost is roughly the same number of decode tokens. This makes replicated flips "flips that occur after the model has reasoned", which is the arcuschin setting.
3. Report MR on all decision-pass flips with the same prominence as replicated flips, and report how many flips fall in each category in §7.2.

### M2. Name-sampling variance is ignored, so inference is anti-conservative for the stated claims

**Problem.** Each attribute contrast rests on 8 fixed name pairs that are crossed with all 150 profiles. The cluster bootstrap and the sign-flip test resample profiles only, so names are treated as fixed effects (the language-as-fixed-effect fallacy, Clark 1973). The paper's phrasing ("Muslim-coded names shift P(Yes)") generalises over names. With 8 names, one salient surname such as Yadav, Jatav or Valmiki can carry an attribute. The leave-one-position-out rule in §3.2(b) helps but is not inference. Also note that a position-level sign-flip test over 8 names has a minimum two-sided p of 2/256 ≈ 0.0078, which **cannot pass Holm at 0.05/8 = 0.00625**.

**Why it matters.** A statistically literate reviewer will flag the CIs as too narrow for the population of names the paper implies.

**Cheap fixes.**
1. **Enlarge the pools to 16 names per cell.** This costs **zero GPU time**, because positions rotate across profiles and the prompt count is unchanged. Each position is then used about 9–10 times. The cost is validation labour only.
2. Make the primary CI a **two-way (profile × position) bootstrap**, resampling both. Alternatively, promote the §9.7 mixed model with a position random effect to the primary test and keep the profile-only test as a sensitivity analysis.
3. State the inferential target in Methods: "these names" or "names of this type".

### M3. The matched noise floor is invalid for gender and for region, and controls induce correlated errors

**Problem.**
- **Gender** swaps the *first name*, but its matched control C1 swaps the *surname*. There is no first-name-only control. First names are more salient in the prompt (the model likely reads "Rahul"/"Priya" more strongly than the surname), so C1 is not the matched noise floor.
- **Region** swaps name *and hometown*, and no control varies the hometown. The hometowns also differ systematically in **city tier**. The reference uses UP tier-2 cities. South includes Chennai (a metro), Mysuru and Mangaluru. Northeast uses small towns: Sivasagar, Golaghat, North Lakhimpur, Tezpur. A region effect is therefore partly an urban/metro effect. Defining region as "name + hometown jointly" does not remove the city-size confound.
- **C1 and C2 share the same 8 control surnames** (`ctrl_k`), and the same control values are subtracted from every attribute's excess. Any idiosyncratic effect of those 8 surnames shifts all eight excess estimates in the same direction, so the Holm-adjusted tests are positively correlated in an unmodelled way. For the *signed* test the control is not needed for validity, because under H0 the expected ΔP is already 0. Subtracting it adds variance plus the control names' own idiosyncratic effect.

**Why it matters.** "Is the noise floor valid for each attribute?" Currently the answer is yes for caste, roughly yes for religion, no for gender and no for region.

**Cheap fixes.**
1. Change C2 to **first-name-only** (another male Brahmin-coded first name with the *reference* surname). Gender is then matched to C2 and caste to C1. For religion, use the pooled C1/C2 floor, or keep a third two-field control.
2. Add **`control_hometown`**: the reference name with a different UP town of matched city tier. That is +1 variant, ≈ +9% prompts. Also **tier-match the hometowns across cells** (metro ↔ metro, tier-2 ↔ tier-2), for example Lucknow ↔ Chennai/Bengaluru and Kanpur ↔ Madurai/Mysuru, and pick Assam towns of similar size where possible (Guwahati and Dibrugarh rather than North Lakhimpur).
3. For RQ1, make the **primary signed test E[d_pa] = 0** and report the control-subtracted excess alongside it. Use controls primarily as the floor for |ΔP| and for flip rates, where a floor is actually needed. Alternatively keep the excess but use C1 and C2 surnames that are disjoint from each other.

### M4. Self-prediction (RQ3b) can be solved without identity awareness, and its ground truth is noisy and rare

**Problem.**
- The model sees the full application. A model that answers "Yes, it would change" more often for borderline applications will have AUROC > 0.5 against F without any awareness of identity, because flips concentrate where P_ref is near 0.5.
- Ground-truth flips are rare and partly noise (see M1). The positive class per (model, attribute, condition) may be about 10–40 cases, so balanced accuracy and AUROC have very wide CIs.
- Controls are always "no change". They inflate accuracy and also define the trivial "always No" strategy.

**Why it matters.** Without a baseline, "models predict their own bias above chance" or "at chance" is uninterpretable.

**Cheap fixes.**
1. Add a **trivial baseline predictor** s = −|P_ref − 0.5| and report the AUROC of P_sp *beyond* it: partial AUROC, or a logistic model of F on P_sp + |P_ref − 0.5|.
2. Report **identity-vs-control discrimination**: is P_sp higher for identity swaps than for control swaps on the same profile? This is a paired test that needs no flip ground truth.
3. Pool attributes for the primary estimate, and use continuous ground truth (ΔP excess, or G with τ) as primary rather than F.
4. Declare **condition N as primary** and A as secondary, in writing.

### M5. Threshold flips are vulnerable to numerical nondeterminism, and the design would not detect it

**Problem.** vLLM under bf16 with continuous batching and prefix caching is not bitwise deterministic across batch compositions. In a design that puts half the profiles near P = 0.5, logprob jitter of about 1e-3 to 1e-2 creates spurious flips. The rule "cache key; never re-run" means this jitter is never measured. Controls absorb it only if the jitter is independent of variant, and it is not, since batch position depends on prompt ID order.

**Cheap fix.** In the pilot, run the decision pass **twice with shuffled request order** and report flip-reproducibility and |ΔP| reproducibility. Add a go/no-go row to §10. Report a "robust flip" (|P − 0.5| > δ on both members, δ chosen from the pilot) as a sensitivity analysis. The cost is about 660 prompts per model.

### M6. Christian, Sikh and Northeast cells carry signals that the manipulation check does not measure (foreignness, class)

**Problem.** The Christian pool (Joshua David, Aaron Matthew, Jonathan Peter, Samuel Thomas) is fully Anglophone, so models may read it as **non-Indian, NRI or Western** as well as Kerala. This matters for loan decisions in particular. The manipulation check offers only Indian religion, caste, region and gender options, so it cannot detect a "foreign" reading. Class and urbanity are acknowledged in §12 but not measured anywhere.

**Cheap fixes.**
1. Add one manipulation-check item, "Is this person most likely from India? Yes/No/Cannot tell", and one coarse class/urbanity item. This adds 176 × 4 prompts, which is negligible.
2. Replace some Christian first names with common Indian-Christian given names (for example Anil, Sunil or Prakash with a Biblical surname, or names common among North Indian Christians). Report the cell as "Christian-coded, Anglophone first name" if the names are kept.

### M7. Normative direction and ethics framing are underspecified for the Indian context

**Problem.**
- S3 is a merit-cum-means scholarship. Indian policy *mandates* preference for SC/OBC students in many scholarships, and a model may also reason that "SC students have government post-matric scholarships", which pushes the other way. A positive or negative SC/OBC ΔP in S3 is therefore not straightforwardly "bias".
- The direction label "disadvantage share" bakes in a normative reading.
- The manipulation check is, in effect, a **caste-from-surname classifier benchmark**. Releasing per-name caste-decoding accuracy together with labelled SC/OBC surname lists has a dual-use risk.

**Cheap fixes.**
1. Use "differential treatment" language throughout and discuss the reservation context per scenario in the ethics section.
2. Report S3 separately for the caste attributes.
3. Release the name lists and manipulation-check outputs under a gated or usage-restricted licence, and do not publish per-surname decoding tables in the paper (aggregate per cell only).

### M8. Forking paths remain despite the pre-registration language

**Problem.** For RQ3 there are strict vs lenient definitions, replicated vs all vs explanation-only flips, matched vs pooled control, full vs decoded subset, F vs G, τ ∈ {0.05, 0.1, 0.2}, and conditions N vs A. No single primary estimate is named per RQ except RQ1. RQ2 is an interaction of excesses, so its SE is roughly √2 × SD(E)/√150 per language contrast. It is likely underpowered, and a null will be read as "no language effect".

**Cheap fixes.**
1. Add a one-row-per-RQ "primary estimand" table to §1: one metric, one subset, one definition. Everything else is labelled sensitivity.
2. For RQ2, pre-specify an **equivalence bound** (for example ±2 pp, tested with TOST) so that a null is reportable as such.

---

## Minor issues

1. **Pilot blinding vs the power update (§9.8 vs §10).** SD(E) cannot be estimated if identity effects are not computed. Estimate it from the control-vs-control difference (C1 − C2 per profile) instead, which stays blinded.
2. **Inconsistent explanation counts.** §7.2 allows up to 900 flips (about 600 ref + 1,500 variant generations), while §11.1 budgets ≤ 1,800 in total. Reconcile them and budget the 2,100 worst case.
3. **The fallback full-candidate scoring uses `prompt_logprobs`.** In vLLM this is slow, memory-heavy at large vocabularies, and historically bypasses the prefix cache. Score multi-token candidates by chain rule with `max_tokens=1` calls on prefix + partial candidate instead.
4. **Top-20 truncation.** If "No" is outside the top 20, P(Yes) = 1. Log a flag when either side is missing, not only when m < 0.9. Also specify vLLM's logprob mode (raw vs processed logits).
5. **Self-prediction turn-1 answer.** Use D (from the P ≥ 0.5 rule), not the "greedy answer", which can be a non-Yes/No token. Say which.
6. **Chat-template prefill with Qwen3.** With `enable_thinking=False`, the empty think block must precede the `Decision:` prefill. Unit-test the rendered strings per model.
7. **ΔP on the probability scale** compresses effects near 0 and 1. Report Δlogit as a sensitivity analysis.
8. **Templates differ in more than paraphrase.** T2 says "Based only on this profile/these details" and T1 does not. That is an implicit anti-bias cue, so the template contrast confounds paraphrase with a de-biasing instruction. Either add "based only on" to all templates or name it as a manipulation.
9. **"Hometown" on a loan application** is unusual; Indian bank forms ask for an address. Consider "Native place" (S1, S3) and "City of residence" (S2), or accept and note it. Check that the Hindi गृहनगर reads naturally on all three forms.
10. **S2 "borderline" mixed profiles with weak CIBIL (600–650)** are near-automatic rejections in practice. Expect hard-gate saturation. Check per-attribute gating in the pilot, not just tier means.
11. **RQ4 family.** Qwen3 dense tops out at 32B, and Qwen2.5-72B is an earlier generation. If the 70B is used as the "large" Qwen, scale is confounded with model generation. Either use 4B/8B/14B (or 32B) of one release, or state the confound. Name the Indic-focused model now; many are base-only or have weak chat templates.
12. **The Muslim pool mixes Sayyid/Shia (Rizvi) with other Ashraf surnames**, and "Ahmed"/"Akhtar" are weakly caste-coded. Fine if documented, but it is another reason for M2.
13. **Judge (§8).** Define the "dimension under test" for control pairs. Validate the judge's *Hindi* performance separately (100 items per language gives a κ CI of roughly ±0.1–0.15). Because positives are rare and over-sampled, report weighted **precision and recall for the positive class** alongside κ. Blind the human annotators to flip status and ref/variant role, as the judge is.
14. **McNemar per (attribute, language, template) cell** assumes independence across profiles, but names are shared. This is secondary, so label it descriptive.
15. **Holm family is per model.** State in the paper that cross-model counts ("bias in k of 6 models") are not FWER-controlled.
16. **GPU estimate.** The throughput assumptions are conservative and plausible for MI300X. For a 70B in bf16, about 45 GB of KV cache at `max_model_len` 4096 limits concurrency and prefix-cache hit rates, so treat the 86 min as optimistic-to-realistic, not conservative. The 36 min pilot/debug buffer is thin for 6 models on ROCm. Make FP8 for the 70B the default plan B rather than step 4 of the drop order. Note also that any band recalibration invalidates the pilot reuse.

## Over-engineered for a 6–11-page short paper (candidates to cut or move to the appendix)

- §9.7 OLS with CR2 **and** the mixed logit. Keep at most one, and only if it becomes the M2 fix.
- Both CCT and φ-CCT plus the length regression. Keep CCT and length per group; put the rest in the appendix.
- T3 and the Hindi "हाँ/नहीं" robustness re-run. Keep both pilot-only and one paragraph at most.
- Manipulation check × 2 formats × 2 orders × 2 languages. Format N (name only) can go, since NH is the one that matches the decision pass.
- Per-cell McNemar tables. One pooled descriptive table is enough.
- Decoded-subset re-analysis of every metric. Do it for RQ1 primary and RQ3 primary only.
- Three τ values and absolute excess plus flip excess plus signed excess. Pick one secondary.
- Self-prediction condition A on all 12,000 prompts. A stratified 20% sample suffices for the "label effect".

## Questions for the authors

1. What is the single primary estimate for RQ3a and for RQ3b (definition, flip set, condition)?
2. Why prefill the decision rather than eliciting reasoning first, given that the closest prior work (arcuschin2026biases) uses pre-decision reasoning?
3. Which three Qwen sizes, and is the 70B in the same family and release?
4. Which Indic-focused model, and does it have a usable chat template and a single-token "Yes"?
5. For control pairs, what dimension does the judge test for "mention"?
6. Will the released benchmark include the caste-coded surname labels, and under what access terms?
7. How will you interpret a *positive* SC/OBC ΔP in the scholarship scenario?
8. Has run-to-run determinism of vLLM on ROCm been checked for this setup?
9. What does the paper conclude if no attribute passes Holm in any model? Is RQ3 then reported at all?
