# Review — "Silent Shifts: Name-Coded Indian Identity Moves LLM Decisions While Explanations and Self-Predictions Stay Uninformative"

**Track 4: Fair and Explainable Language and Multimodal AI**
**Reviewer 2**
**Reviewed version:** draft 1 (`paper/main.pdf`, `paper/main.tex`)

---

## 1. Summary

The paper audits eight open-weight LLMs (Qwen3 4B–32B, Granite-3.3-8B, OLMo-3-7B, Ministral-8B, Sarvam-M) on 150 synthetic job, loan and scholarship applications. Each application is paired with versions that differ only in a gender-, caste-, religion- or region-coded Indian name, with same-group controls, in English and Hindi. Shifts in P(Yes) are small (≤2.16 pp; 10/64 cells Holm-significant), but flips lean towards *Yes* for female- and Northeast-coded names. An LLM judge finds no identity mention in any of 576 explanations of flipped decisions. Self-prediction of counterfactual sensitivity is at chance near the threshold. A manipulation check shows that models refuse to infer caste, so the caste null cannot be read as caste fairness.

## 2. Scores (1–5)

| Criterion | Score | Comment |
|---|---|---|
| Originality | 3 | Combines known paired-audit and verbalisation designs (Tamkin, Arcuschin, Karvonen) for a new, under-studied setting: implicit Indian identity signals in English and Hindi, plus a self-prediction probe. The delta is the setting more than the method. |
| Technical soundness | 2.5 → **2** | Careful statistics in places (two-way bootstrap, matched controls, drop-one-name, margin baseline), but the headline rests on a disclosure measure with no variance and no positive control. The pooled direction test is pseudo-replicated, and the validation steps (names, Hindi translation, judge κ) are unfinished. |
| Clarity | 4 | Well written, honest and well hedged. RQs and findings are easy to follow. Some figures are hard to read at print size. |
| Significance | 3 | Practically relevant message (explanation review is no substitute for paired audits), but effects are 1–2 pp and the "silent" result may be a property of how these models write explanations generally. |
| Reproducibility | 3 | Pinned revisions, greedy decoding, cached requests, templates and judge prompt in the appendix, GPU time reported. However, the release URL is a TODO, the name lists are not in the paper, and the benchmark is gated. |

**Overall recommendation:** **Weak reject** (borderline; I would move to weak accept if Weaknesses 1–3 are addressed and all TODOs are removed).
**Confidence:** 4/5. I know LLM fairness auditing and faithfulness work well, and Indian caste and name signalling reasonably well.

## 3. Strengths

1. **Careful design for a signal that is hard to study.** Matched same-group controls, name positions aligned across cells, a two-way bootstrap over profiles *and* names, and drop-one-name checks are more careful than most LLM name-swap audits. This directly addresses the Seshadri et al. concern that non-demographic edits move outputs as much as demographic ones.
2. **The manipulation check is the paper's most valuable contribution.** Showing 100% "Cannot tell" on caste for every model (including reference and control names) turns a tempting "no caste bias" claim into a correctly calibrated "uninformative null". The Christian-cell finding (never read as Christian) is similarly useful. Many published audits skip this step.
3. **Honest self-limitation.** The noise-floor discussion (Fig. 2), the admission that individual flips are near-threshold events, "differential treatment, not discrimination", the RQ2 readout confound and the waived validation steps are all stated openly. The self-prediction analysis is compared against a non-introspective margin baseline instead of against chance only, which is the right comparison.
4. **Practitioner-relevant message.** "Explanation review and self-report are not substitutes for paired behavioural audits" is a clear and actionable takeaway for Track 4.
5. **Coverage of an under-served context.** Indian identity, Hindi prompts, and an Indic-focused model (Sarvam-M), across eight open-weight models with pinned revisions.

## 4. Major weaknesses (ranked)

### W1. The "silent" headline is a null with no variance and no positive control. *(Most important.)*
The judge assigns label A to **1 of 19,615** explanations, including all unflipped and control explanations. Disclosure is therefore 0% *everywhere*, not specifically where identity mattered. The result is equally consistent with:
(a) models hide an identity effect, or
(b) these models, prompted this way, never discuss applicant identity in any explanation, regardless of what drives the decision.
Hypothesis (b) is a known style property of aligned models and is much less interesting. On top of this, the judge has no validation yet (κ is a TODO, in two places). Only 317 of the 576 "flips" are reproduced in the explanation pass. Flip rates (≈1–3%) are close to the control rates (≈0.3–2.5%), so most "identity-flipped" pairs are plausibly noise flips that a faithful explanation *should not* attribute to identity. The paper half-acknowledges this in RQ3a ("the finding is therefore not that each flip was explained unfaithfully"), but the title, abstract and Discussion still frame it as "explanations silent while decisions shift".

*Fixes (no new experiments):*
- **Reframe the claim to what the data supports.** For example: "Explanations never mention identity, in any condition, so they cannot reveal the aggregate directional shift." Present it as an *auditing* finding (explanations carry zero identity information), not as an unfaithfulness finding about individual decisions. Change the title, abstract sentence and Discussion paragraph to match.
- **Re-analyse the existing explanations for indirect signal.** For example, compare which factors are cited, the explanation length, or the sentiment between female/Northeast and reference explanations of the *same* profile. If explanations differ systematically in a way that tracks the ΔP direction, that is informative. If they do not, that strengthens "uninformative".
- **Finish the 200-item human κ** (the labelling sheet is ready; this is annotation, not a model experiment).
- *(New experiment, small)* **Add a positive control.** Run the explanation pass with the attribute stated explicitly (as in self-prediction condition A), or with a non-identity factor that is known to flip decisions. This shows that the judge and the explanations *can* surface a cause when one exists. Without it, "0%" cannot be distinguished from "the instrument never fires".

### W2. Claims are not calibrated to the effect sizes, and the pooled direction test is pseudo-replicated.
Mean shifts are ≤2.16 pp, and most significant cells are 1–1.7 pp. The title verb "moves LLM decisions" and the abstract's "directional" carry more weight than ~2% vs ~1% flip rates support. The strongest evidence (female 73:18, Holm p=4×10⁻⁸) pools flips across 8 models that share profiles and names, and treats them as independent (this is acknowledged only in Scope). The binomial test is also against 50:50, not against the control's own direction split. The "+6.37 pp near threshold" figure conditions on |P_ref−0.5|<0.3, where ΔP is mechanically larger. No control value is given for the same band, so it reads as more alarming than it is.

*Fixes (re-analysis only):*
- **Replace or augment the pooled binomial test with a cluster-aware one.** Options: a per-model sign test (female positive in 8/8 models, p≈0.008 two-sided), a bootstrap of the to-Yes share over name positions and profiles, or a mixed-effects logit on flip direction with name and profile random effects.
- **Test direction against the matched control.** For example, female 73:18 vs. control (surname) 23:28 with Fisher's exact test, or excess-ΔP within the band.
- **Report the control ΔP in the near-threshold band** next to +6.37 and +5.91 pp.
- **Soften the title and abstract.** For example: "…shifts LLM decisions slightly but consistently…". Lead the abstract with the size of the effect.

### W3. Validity of the identity signals is unfinished and narrows the scope of the contribution.
- The human review of names and of the Hindi translations was "waived by the team so that GPU runs could start".
- The Hindi wrappers are machine-translated and unvalidated.
- 15 of 88 names are flagged by Outkast/Naampy.
- Caste is not decoded at all; Christian names are not read as Christian; Sikh names are confounded with gender.

Only two of the eight attributes (gender, region) are both decoded and shifted. One of those (Northeast) changes name *and* hometown with no hometown control. South is decoded at 100% but shows no direction (48:51). This undercuts the Discussion claim that the shifted signals "are exactly the signals models decode reliably": decoding is necessary but clearly not sufficient.

*Fixes:*
- **State the effective scope explicitly** (gender and Northeast region, plus an uninformative caste null) in the abstract and contributions, instead of implying eight attributes.
- **Rewrite the "waived" sentences in neutral reporting language.** For example: "Name lists and Hindi translations were not human-validated before the runs; a post-hoc automated check…".
- **Promote the validated-names robustness result** (8/64 significant cells) to a column in Table 3, or a sentence alongside each headline number.
- **Address the South/Northeast contrast in the Discussion.**
- *(Cheap, no model runs)* Have a native speaker validate the Hindi templates post hoc and report the result.

### W4. The self-prediction analysis is underpowered and not well posed.
Positives are 0.8–2.7% of pairs, and several models predict "change" in under 1% of cases (Sarvam-M 0.2%, OLMo 0.7%). AUROC from such near-constant scores is fragile. The near-threshold AUROCs (0.43–0.59) are reported without n or CIs. Because control swaps flip at similar rates, the target ("did it flip?") is mostly noise, so the margin baseline wins by construction. The probe therefore tests whether models can predict near-threshold instability, not whether they can predict identity sensitivity.

*Fixes (re-analysis):*
- **Report n (pairs and flips) and bootstrap CIs** for every AUROC in Table 4, especially the near-threshold band.
- **Add a target that isolates identity sensitivity.** For example, correlate the predicted-change probability with |ΔP|, or with excess-ΔP over the control for the same profile.
- **Moderate "cannot report their own counterfactual sensitivity"** to "show no detectable ability, with limited power".

### W5. RQ2 and RQ4 dilute the paper.
Both are confounded or descriptive:
- RQ2 compares two different readouts for Granite and Sarvam-M; the noise floor shifts with language; names stay in Latin script; and the ±2 pp equivalence margin is as large as the largest effect.
- RQ4 shows no trend and is explained by decisiveness.

Together they take about a page that W1 and W2 need.

*Fix:* Compress RQ2 and RQ4 into one short "Secondary analyses" subsection (or an appendix). Keep Fig. 3 only if it is made legible (see minor issues). Use the freed space for the cluster-aware direction test, the control near-threshold row, and the explanation-content analysis.

### W6. Unfinished manuscript.
There are `\TODO` macros in the author block (4×), κ (2×) and the release URL. These render in red in the PDF. At many venues this alone is grounds for desk rejection. Remove or complete them before submission (anonymise authors if the review is double-blind).

## 5. Minor issues

- **Fig. 3 (language)** is a full-width plot squeezed into `\columnwidth`. The 8-model legend and tick labels are unreadable in print. Make it `figure*` or split it into two panels, and enlarge the fonts.
- **Fig. 6 (manipulation)**
  - White annotation text on yellow cells is almost invisible.
  - The colour-bar label is clipped in the source image, and the `trim=0 0 45 0` crop removes it entirely, leaving an unlabeled colour bar. Use dark text on light cells and regenerate the figure with a short colour-bar label.
  - The caption says "English"; consider a Hindi panel, since RQ2 relies on decoding differences across languages.
- **Fig. 1**
  - The title is clipped in the PNG (`p<0.0…`) and removed with `trim=… 22` in the paper. Remove titles in the plotting code rather than by cropping.
  - Eight series per attribute with default matplotlib colours is dense, and the colours are not colour-blind-safe (red/green and brown/pink pairs).
  - Consider marking the control range as a shaded band.
- **Fig. 2:** the colour scale is centred on 0 but the cell annotations show raw rates. State the colour meaning in the caption more explicitly ("colour = identity − control, pp").
- **Unused figures:** `fig4_disclosure` and `fig5_selfprediction` exist but are not referenced. Either use one of them (a bar chart of the 0% disclosure next to the directional flips would help skimmers) or drop them.
- **Table 4 (RQ3)**
  - It has 11 columns at `\footnotesize` in a `table*`, and mixes two analyses. Split it into an explanation table and a self-prediction table, or drop BA (it is redundant with AUROC).
  - Margin AUROCs are given to 3 decimals and the near-threshold AUROCs to 2. Be consistent.
- **Table 3:** add the validated-names column and the control near-threshold row (W2/W3).
- **Abstract:** it is dense with numbers (≈12). Keep 3–4 (2.16 pp, 73:18, 0/576, AUROC 0.43–0.59) and move the rest to the body. "10 of 64 model–attribute cells Holm-significant" should say "Holm within model".
- **Notation:** "Holm p" in Table 3 is Holm over attributes, while elsewhere Holm is within model. Name the family each time.
- **Equivalence:** "more conservative than the 90% CI of a standard TOST" is true, but the margin choice (±2 pp) needs a justification, not only the CI level.
- **Self-prediction parse rule:** "falling back to the parsed text when that mass is below 0.5" mixes a probability with a binary score. State how the binary score enters the AUROC (it creates ties).
- **Explanation sampling:** flips were defined from the run-time first-token readout, which differs from the final readout for Granite and Sarvam Hindi. State how many final-readout flips lack explanations.
- **Appendices after references:** IEEE conference style normally places appendices before the bibliography, or omits them in short papers. Check the venue template. Appendix B ("These are the intended sources; only the Outkast and Naampy checks were run") reads as an internal note; rephrase it.
- **Phrasing:**
  - "the team lead", "waived by the team so that GPU runs could start" and "licence access was not granted in time" are process details; rephrase them neutrally.
  - "Putting the reason first avoids rationalising a fixed answer" is too strong; it *reduces the risk* of post-hoc rationalisation, and the 317/576 replication rate shows that the decision is not fixed either.
- **References**
  - Several 2026 entries are `@misc` preprints (christian2026self, gao2026llms, nair2026rupeebias, veldanda2026explanation). Add arXiv IDs/URLs consistently.
  - Check that `mayne2026positive` and `arcuschin2026biases` have final venue and page details.
  - Use consistent capitalisation protection (`{LLM}`).
- **Hindi rendering:** `\hindi{}` falls back to a placeholder under pdfLaTeX. Make sure the camera-ready build uses XeLaTeX, or the Devanagari in §III-C and the appendix disappears.
- **Gender control:** gender is compared against the *surname* control, even though the full-name control changes the first name. Justify this choice or report both.
- **Model naming:** "Sarvam-M-24B" in the figures vs. "Sarvam-M" in the text; "Ministral-8B" vs. "Ministral-8B-Instr.-2410". Unify the names.

## 6. Specific checks

**Does the abstract match the results?**
Mostly, yes. All numbers I checked (2.16 pp, 10/64, 73:18, 89:37, 576, 0.43–0.59, caste 100% abstention) match the body. Two problems:
1. "An LLM judge finds an identity attribute in none of 576 explanations" omits that the rate is ~0% for *all* explanations, which is the context needed to interpret it.
2. "Directional" is stated without the caveat that flips are ≈1–3% vs. a ≈0.3–2.5% control floor.

**Are the claims calibrated to effect sizes (sub-2-pp shifts)?**
The body is well calibrated: "small", "differential treatment", "not evidence of harm", and the noise-floor discussion. The title ("moves LLM decisions"), the "Silent Shifts" framing and the Discussion ("which is where real screening decisions are contested") are less so. The +6.37 pp near-threshold number needs its control counterpart, and the pooled p=4×10⁻⁸ overstates certainty because of pseudo-replication (W2).

**Is the headline (explanations silent while decisions shift) convincingly supported, given that flips are rare and close to the control rate?**
Only partially. The *aggregate* shift for female and Northeast names is reasonably supported: it is consistent across 7–8/8 models and robust to dropping single names. The "silent" part, however, cannot be distinguished from "never mentions identity in any condition", because disclosure has no variance and no positive control (W1). The paper's own careful sentence ("explanations carry no information about an identity effect that exists in aggregate") is defensible. The title and abstract framing goes further than that sentence.

**Is the related-work positioning fair?**
Broadly fair and current. It cites Arcuschin et al. 2026 and Karvonen et al. 2025 as closest, and Christian & Mazor 2026 for self-simulation. It should state the delta from Arcuschin et al. more precisely (implicit vs. explicit concepts, *and* a self-prediction probe), and acknowledge that Karvonen et al. already show bias that is invisible in the chain-of-thought for implicit name signals (race/gender). The novelty is mostly the Indian setting plus the manipulation check, which is worth saying plainly. The comparison to Rao et al. and Zaveri et al. on caste is handled well.

**Is the ethics section adequate for caste and religion?**
Adequate but thin for this track. Good points: aggregate-only reporting, gated release, "signals, not claims about people", the reservation-norm discussion, and differential treatment vs. discrimination. Missing:
1. Any community or expert input on the caste and religion name lists. They are drawn from Wikipedia and were not human-reviewed, which matters for a sensitive caste taxonomy.
2. Dual-use risk: a released caste-surname list paired with model-sensitivity results could be used to tune or evade audits. Who gets gated access, and on what criteria?
3. The risk that "favours female/Northeast" is misread as "LLMs are biased against Brahmin men". One sentence on how the findings should not be used is enough.
4. The author-annotation statement: will the κ annotators include people familiar with Indian identity signals?

**Is the paper self-contained, and does it make sense to a reader who skims (title, abstract, figures, conclusion)?**
Mostly. The title, abstract and conclusion tell a coherent story. However:
- A skimmer would take away "LLMs hide identity bias in explanations", which is stronger than the evidence.
- Fig. 1 alone shows mostly CIs crossing zero, without the direction story.
- The disclosure result, the paper's headline, has *no figure*, while fig4_disclosure exists but is unused.
- Fig. 3 and Fig. 6 are hard to read at print size.

A single figure that pairs "flip direction (to-Yes vs. to-No, identity vs. control)" with "disclosure rate (identity-flipped vs. control vs. unflipped, all ≈0)" would let a skimmer see the claim and its limitation at once.

## 7. Single change that would most increase acceptance probability

**Re-scope the headline to the claim the data supports, and show the disclosure null in context.** Retitle and reword the abstract to "explanations never mention identity in any condition, so they cannot reveal a small but consistent aggregate shift". Add one figure or table that sets the directional flips (identity vs. control, with a cluster-aware test) next to the disclosure rates (identity-flipped, control-flipped and unflipped, all ≈0). Ideally, also add a small positive-control explanation run with the attribute stated explicitly, to show that the instrument can detect disclosure. This turns the main vulnerability, a null with no variance, into an honest and still useful auditing result.
