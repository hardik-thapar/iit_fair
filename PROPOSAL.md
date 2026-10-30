# Do LLMs Tell the Truth About Their Bias?

*Counterfactual Auditing of Decisions and Self-Explanations in the Indian Context*

Oct 30, 2026 · @hardik

## 1. Problem and motivation

LLMs are already used to screen job, loan and admission applications, and they are routinely asked to explain their decisions. We test two things in the Indian context: whether decisions change when only an applicant's identity signal changes, and whether the model's explanation admits it.

Most LLM bias audits use US identity markers (race and gender via American names). India-specific signals such as caste-coded surnames, religion, region and language are much less studied, even though Indian institutions are adopting these models. A model can also be biased while giving explanations that sound neutral. That is a transparency failure an auditor would never see by reading explanations alone.

**Target:** Short paper (6–11 pages), Track 4 (Fair and Explainable Language and Multimodal AI), with secondary relevance to Track 5 (auditing).

## 2. Research questions

1. **RQ1 — Decision bias.** Do open-weight LLMs change accept/reject decisions or confidence when only an Indian identity marker (caste-coded surname, religion, region, gender) is swapped?
2. **RQ2 — Language.** Does bias change when the same application is written in Hindi instead of English?
3. **RQ3 — Explanation faithfulness.** When a decision flips because of an identity swap, does the model's explanation mention that attribute? When asked directly, does the model correctly predict its own counterfactual behaviour?
4. **RQ4 — Scale.** Do these effects shrink or grow with model size within a model family?

## 3. Related work and gap

The gap: existing work studies either decision bias or explanation faithfulness, mostly with Western identity markers. No study we know of measures both on the same Indian decision prompts. The literature review phase must confirm this; the starting points below are from memory and need verifying.

- **Correspondence audits.** Bertrand & Mullainathan (2004) showed name-based hiring discrimination by swapping names on identical resumes. We apply the same paired design to LLMs.
- **LLM decision discrimination.** Tamkin et al. (2023, Anthropic) built templated decision prompts with varied demographics. Their markers are US-centric.
- **India-centric bias.** Work such as Indian-BhED (Khandelwal et al., 2024) measures caste and religion stereotypes. It focuses on stereotype association, not decisions or explanations.
- **Unfaithful explanations.** Turpin et al. (2023) and Lanham et al. (2023) show that chain-of-thought explanations can omit the real cause of an answer. These studies use reasoning tasks, not fairness-critical decisions in a non-Western setting.

## 4. Method

We run a paired counterfactual audit: identical applications that differ only in one identity signal, scored by local open-weight models. Every comparison is within a pair, so qualification differences cancel out.

**Benchmark construction**

- **Scenarios (3):** fresher software-engineer shortlisting, small personal loan approval, merit scholarship award.
- **Base profiles:** 50 per scenario (150 total), deliberately spread across strong, borderline and weak. Bias usually appears at the margin, so about half are borderline.
- **Identity variants:** one attribute changed at a time from a reference identity, signalled through names, surnames and hometowns drawn from published sources and checked by the team.
- **Controls:** swaps within the same group (two different upper-caste Hindu male names, for example). Their flip rate is the noise floor that real effects must beat.
- **Language:** each prompt in English and Hindi (machine-translated, then human-checked).
- **Prompt robustness:** 2 paraphrased instruction templates, so results are not artefacts of one wording.

| Attribute | Variants | Signal |
| --- | --- | --- |
| Gender | Male, female | First name |
| Religion | Hindu, Muslim, Sikh, Christian | Full name |
| Caste (coded) | Dominant-caste, OBC-coded, SC-coded surname | Surname |
| Region | North, South, Northeast | Name + hometown |
| Control | Same-group name swap | Name |

**Three passes per model**

1. **Decision pass:** a one-token Yes/No answer. We read the probability of "Yes" from the logits, giving a continuous confidence score, not just a binary flip.
2. **Explanation pass:** decision plus a short justification, for every flipped pair and a random sample of unflipped pairs.
3. **Self-prediction pass:** we ask, "Would your decision change if the applicant's surname were X?" and compare the answer with the model's actual behaviour.

**Models:** 6–7 open-weight instruction models run locally with vLLM. These include one family at 3 sizes (for RQ4), 2–3 other families at 7–9B, and one Indic-focused model. The latest stable versions are picked at the start of experiments.

**Metrics**

- Flip rate per attribute, compared against the control noise floor; McNemar's test on paired decisions.
- Mean change in P(Yes) per attribute, with bootstrap 95% confidence intervals.
- **Mention rate:** share of attribute-driven flips whose explanation names the attribute. Detected by keyword matching plus a judge model, validated against 200 human-labelled explanations (report Cohen's kappa).
- **Self-prediction accuracy:** how often the model correctly predicts its own counterfactual behaviour.

## 5. Compute budget (under 5 GPU-hours)

The full study fits in about 4 hours on one MI300X, because the design is inference-only and the main decision pass reads a single token. Each base profile yields 11 prompts (reference, 8 identity swaps, 2 controls) × 2 templates × 2 languages, or **6,600 decision prompts per model**.

| Job | Approx. GPU time |
| --- | --- |
| 5–6 models at 7–14B, all three passes (\~12–15 min each) | 1.5 h |
| One 70B-class model, all three passes | 1 h |
| Judge model for mention detection | 0.3 h |
| Pilot runs and debugging buffer | 1 h |
| **Total** | **\~3.8 h** |

Rules that keep it under 5 hours: pilot every change on 10% of the data first, cache every model output to disk, and never re-run a finished model. No fine-tuning or training is in scope. These figures are estimates; the pilot run will confirm them.

## 6. Contributions, plan, team and risks

**Expected contributions**

1. A released benchmark of about 6,600 validated counterfactual decision prompts with Indian identity markers in English and Hindi.
2. An open-source, reproducible auditing toolkit (prompt generation, local inference, metrics, plots).
3. Measured decision bias across 6–7 models, and the first measurement, to our knowledge, of whether their explanations disclose that bias.

**Plan**** **

1. literature review, gap confirmation, name and surname lists, templates.
2. human validation of templates and translations; pilot on 10% of data.
3. full runs; human labelling of 200 explanations.
4. &#32;statistics, plots, error analysis.
5. &#32;writing, internal review, submission.

**Team roles**

| Member | Owns |
| --- | --- |
| Member 1 | Benchmark: templates, name lists, translation checks |
| Member 2 | Toolkit: inference pipeline, caching, reproducibility |
| Member 3 | Analysis: metrics, statistics, figures |
| Member 4 | Literature review, ethics section, paper writing |

**Risks and mitigations**

- *Unrealistic prompts* → human validation and the control-swap noise floor.
- *Judge model errors* → validated against human labels with Cohen's kappa reported.
- *Few flips, little to analyse* → the continuous P(Yes) shift and borderline-heavy profiles still give measurable effects. A null result with tight confidence intervals is also reportable.

**Ethics.** Caste and religion are sensitive. We use names only as signals, never as claims about groups. We report aggregate effects, release the benchmark with a usage statement, and include an explicit ethics and limitations section. No human subjects data is collected beyond the team's own annotations.
