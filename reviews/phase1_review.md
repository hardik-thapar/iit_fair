# Reviewer 2: Phase 1 (literature review and claimed gap)

*Track 4, Fair and Explainable Language and Multimodal AI. Reviewed 2026-10-30. Files read: `PROPOSAL.md`, `lit/gap_analysis.md`, `lit/notes.md`, `paper/refs.bib` (skimmed), `lit/ref_check.csv`.*

## Summary

The authors plan a paired name-swap audit of open-weight LLMs on Indian yes/no allocation decisions (English vs Hindi), followed by explanation-disclosure and self-prediction probes. The literature review is careful, honestly flagged and mostly accurate: the 4 spot-checked entries hold up, and all 57 bib titles were machine-checked. The restated novelty claim, however, rests on a conjunction of five features rather than on one sharp question. It also under-reads the two closest papers and misses several literatures that bear on measurement validity.

## Scores (1–5)

| Criterion | Score | One-line reason |
| --- | --- | --- |
| Novelty | 3 | No single piece is new; the combination is new. Defensible for a short paper only if framed around implicit-signal disclosure. |
| Soundness of gap | 3 | The gap is real but argued as "no paper has all 5 columns". Two of the columns (yes/no + open-weight; self-prediction) are weaker than stated. |
| Coverage | 3 | Strong on LLM audits and CoT faithfulness. Weak on name-signal validity, first-token/logprob validity, prompt sensitivity of bias audits, Indian social-science evidence, and India-fairness framing. |

## Is the §2 restated novelty claim defensible? Where I would attack it

Restating the claim (dropping "first to do both decision bias and faithfulness") was the right move, since arcuschin2026biases already does that for hiring, loan and admissions. The five sub-claims are uneven:

- **Claim 1 (first paired audit of Indian name-coded identity on yes/no decisions with open-weight models).** This is the weakest claim. rao2025invisible already swaps Indian names for caste × region × gender in hiring (GPT-4o; I confirmed 50 transcripts × 8 conditions, 60 names, null for caste and region). zaveri2025caste swaps caste surnames in shortlisting. Dammu et al. 2024 (EMNLP, *not cited*) audit Brahmin vs Dalit hiring conversations with 8 LLMs, including open Llama models. "Yes/no rather than Likert" and "open rather than closed" are operational choices, not research gaps. A reviewer will say this is a replication with a different response format.
- **Claim 2 (first English vs Devanagari Hindi decision-bias comparison).** This is plausible, and I found no direct counterexample. But girhepuje2023legal already studies Hindi-language decision fairness (with classifiers), and BharatBBQ / IndiBias already show Hindi vs English bias gaps on QA and likelihood tasks. The claim must also deal with a confound: in Hindi the *name itself* changes script, so the identity signal and the language move together.
- **Claim 3 (disclosure of implicit, name-coded markers).** This is the strongest and most Track-4-relevant claim, and it should be the headline. There is a caveat. arcuschin2026biases measures *CoT before the decision*, whereas this design asks for a *post-hoc justification* in a separate pass. Those are different constructs, and tan2026small shows that asking for a rationale changes decisions. Also, with names, "mention" is ill-defined: models almost never write "because the surname is Dalit-coded". The paper needs to argue why a low mention rate is evidence of unfaithfulness and not merely an artefact of the signal being implicit.
- **Claim 4 (self-prediction probe; "only christian2026self is close").** This understates the overlap. I checked the full text. christian2026self already uses Tamkin-style yes/no decisions scored by the yes/no **logit difference** on an **open model (Qwen2.5-7B)** plus GPT-4.1. Its "If you didn't know" condition asks the model to estimate its counterfactual (blinded) decision and compares that estimate against an actual blinded run. That condition was the *worst* intervention (5.46 vs 1.34 logits deviation for Qwen). This is close to RQ3b. The difference that remains is a *direct, per-pair verbal prediction scored for accuracy*, with Indian markers. Say exactly that.
- **Claim 5 (within-family scale).** This is fine as an analysis but not a contribution. siegel2025verbosity (75 models) and lanham2023measuring already address scale and faithfulness.

**Is it enough for a short paper?** Given arcuschin2026biases, rao2025invisible, nair2026rupeebias and zaveri2025caste: **yes, but only with a sharper frame.** The publishable question is: *"When Indian identity is signalled only implicitly, do models (a) pick up the signal, (b) act on it, and (c) admit it, in English and Hindi?"* That needs a manipulation check, which `gap_analysis.md` §5.2 currently treats as optional. Without it, a null (which rao2025invisible and gao2026llms make likely) cannot be told apart from "the model did not notice". The paper then has nothing to say on RQ3.

## Major issues (ranked, each with a cheap fix)

1. **The novelty argument is a feature conjunction ("no paper has all five columns").** Reviewers discount this kind of argument heavily, and Claim 1 in particular is already covered by rao2025invisible, zaveri2025caste and Dammu et al. 2024.
   *Fix (½ day):* Rewrite §2 so the single headline is disclosure and self-prediction under *implicit* Indian signals, with decision bias as the necessary precondition. Demote claims 1 and 5 to "setting" rather than "contribution". Add Dammu et al. 2024 to the comparison table.

2. **Name-signal validity is assumed, not established, and the literature on it is missing.** Only DECASTE is cited for "surnames carry caste signal". Gaddis (2017) shows that audit names carry *class* as well as race. Caste surnames in India are similarly entangled with region, language and class. Sikh names also confound religion with region and gender.
   *Fix (≈0.2 GPU-h):* Make the manipulation check mandatory: ask each model to classify caste, religion, region and gender from each name, and report decoding accuracy per model and per language. Condition RQ3 analyses on names the model decodes correctly. Cite Gaddis 2017 and report Outkast/Pranaam/Naampy scores per name.

3. **The self-prediction gap is overstated (christian2026self) and the claim about it is inaccurate.** `notes.md` says "e.g. scholarship" and "the exact protocol needs checking". The protocol is actually closer to RQ3b than §2 admits: yes/no decisions, logit difference, an open 7B model, and a counterfactual self-estimate compared against actual blinded behaviour.
   *Fix (1 hour):* Update the notes entry and the §1 table cell from "partly" to a precise description. In §2 claim 4, state the residual difference: direct per-pair verbal prediction scored for accuracy, with implicit Indian markers. Consider adopting their logit-difference metric so the numbers are comparable.

4. **The measurement validity of P(Yes) and the bias metric is not grounded in the literature.** The design reads a single first token, but Wang et al. 2024 show first-token probabilities often disagree with the text answer of instruction-tuned models (over 60% mismatch for Llama-2-7B-chat). Prompt formatting alone can swing results enormously (Sclar et al. 2024). Shallow dataset-construction choices can reorder models by measured bias (Selvam et al. 2023). Two templates is thin given this evidence.
   *Fix (≈0.1 GPU-h):* On a 10% pilot, report agreement between argmax P(Yes) and the greedy text answer per model, and drop or flag models below roughly 90% agreement. Add a third template, or format-only perturbations, and report the spread across templates as a robustness band. Cite all three papers.

5. **The Indian human-discrimination grounding is thin and partly unverified.** banerjee2009labor's findings are marked UNVERIFIED in the notes yet are used to motivate the SWE scenario. Thorat & Attewell 2007 is excluded, even though its EPW 42(41):4141–45 citation is confirmable through a World Bank bibliography and the OUP *Blocked by Caste* reprint. Siddique 2011 (the main caste correspondence study) and any caste-and-credit evidence for the loan scenario are missing. Sambasivan et al. 2021, the canonical "fairness in India" paper for a FAccT-adjacent audience, is also missing.
   *Fix (½ day, no compute):* Add Siddique 2011, Kumar & Venkatachalam 2019 (loan scenario) and Sambasivan et al. 2021. Read banerjee2009labor before citing any numbers. Cite Thorat & Attewell through the *Blocked by Caste* chapter if EPW access fails.

## Minor issues

- `gap_analysis.md` §5.3 correctly notes the gap between CoT and post-hoc explanation, but §2 claim 3 still says "extending" arcuschin's measurement. Call it an *analogous post-hoc* measure, and report decision-pass vs explanation-pass disagreement as its own result. tan2026small predicts that the two will disagree.
- arcuschin2026biases: the κ values are consistent and verified (human–human 0.737; GPT-5-mini judge vs human 0.67). The "ICML 2026" venue label did not appear on the abstract page or the v5 HTML when I checked. Cite it as an arXiv preprint unless the venue is confirmed elsewhere.
- siegel2024probabilities: the notes say the mention–impact association "grows with model size" but omit that the abstract says it "var[ies] significantly by task". Add that caveat before using it as an RQ4 prior.
- rao2025invisible: the notes are accurate. The gender effect was nominally significant in the mixed models (p ≈ .03) but not in post-hoc tests. Report it as such, not as a "weak effect".
- The gap table has nair2026rupeebias's signal as "explicit labels". The abstract does not say this; the notes attribute it to the HTML limitations section. Keep it, but cite the section.
- The OBC-coded surname source is still open: Outkast and Zaveri cover only SC/ST/Other. This is a Phase 2 blocker for one of the three caste levels and should be listed as such.
- §3 G2 should mention the Hindi tokenisation issue (§5.4) as a *validity* threat for RQ2, not just an engineering issue. Different answer-token entropy across scripts can shift P(Yes) with no bias involved.
- `ref_check.csv`: zaveri2025caste is "partial". Do not cite the "16%" figure until the PDF is re-opened.

## Missing references (each verified by search; URLs given)

| Topic | Reference | URL |
| --- | --- | --- |
| India fairness framing | Sambasivan, Arnesen, Hutchinson, Doshi, Prabhakaran. *Re-imagining Algorithmic Fairness in India and Beyond.* FAccT 2021 | https://arxiv.org/abs/2101.09995 |
| Caste in LLM hiring (open models) | Dammu, Jung, Singh, Choudhury, Mitra. *"They are uncultured": Unveiling Covert Harms and Social Threats in LLM Generated Conversations.* EMNLP 2024 | https://aclanthology.org/2024.emnlp-main.1134 |
| Name-signal validity | Gaddis. *How Black Are Lakisha and Jamal? Racial Perceptions from Names Used in Correspondence Audit Studies.* Sociological Science 4 (2017) 469–489 | https://sociologicalscience.com/articles-v4-19-469/ |
| First-token / P(Yes) validity | Wang et al. *"My Answer is C": First-Token Probabilities Do Not Match Text Answers in Instruction-Tuned Language Models.* 2024 (ACL Findings 2024) | https://arxiv.org/abs/2402.14499 |
| Prompt sensitivity | Sclar, Choi, Tsvetkov, Suhr. *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design.* ICLR 2024 | https://arxiv.org/abs/2310.11324 |
| Bias benchmark fragility | Selvam, Dev, Khashabi, Khot, Chang. *The Tail Wagging the Dog: Dataset Construction Biases of Social Bias Benchmarks.* ACL 2023 (short) | https://aclanthology.org/2023.acl-short.118 |
| Caste hiring discrimination (field) | Siddique. *Evidence on Caste Based Discrimination.* Labour Economics 18(S1):S146–S159, 2011 | https://ideas.repec.org/a/eee/labeco/v18y2011is1ps146-s159.html |
| Caste hiring discrimination (field) | Thorat & Attewell. *The Legacy of Social Exclusion: A Correspondence Study of Job Discrimination in India.* EPW 42(41):4141–45, 2007; citation confirmed via World Bank *Perspectives on Poverty in India* bibliography | https://issuu.com/world.bank.publications/docs/9780821386897/291 |
| Caste and lending | Kumar & Venkatachalam. *Caste and Credit: A Woeful Tale?* Journal of Development Studies 55(8):1816–1833, 2019 | https://ideas.repec.org/a/taf/jdevst/v55y2019i8p1816-1833.html |

I also searched for a multilingual (prompt-language) *decision*-bias study in LLM hiring or lending and found **none** that compares identical applications across prompt languages. That supports Claim 2. State in the paper that this was searched for.

**Spot-checks performed:** arcuschin2026biases (accurate; venue unconfirmed), rao2025invisible (accurate), christian2026self (under-described; see Major 3), siegel2024probabilities (accurate, task caveat omitted), nair2026rupeebias (abstract consistent; signal type is not in the abstract).
