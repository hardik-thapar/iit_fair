# Gap analysis (Phase 1)

*2026-10-30. Based on 57 papers in `lit/notes.md`. All keys refer to `paper/refs.bib`.*

## 1. Has someone already done our exact study?

**No.** No paper we found combines all five parts of our design:

| | (a) Indian identity via names / surnames | (b) Paired yes/no allocation decisions + P(Yes) | (c) English vs Devanagari Hindi | (d) Does the explanation disclose the bias? | (e) Self-prediction of own counterfactual behaviour |
| --- | --- | --- | --- | --- | --- |
| rao2025invisible (AIES 2025) | yes (gender, caste, region) | scores, not yes/no; GPT-4o only | no | no | no |
| zaveri2025caste (IIMB WP) | yes (caste surnames) | list shortlisting; ChatGPT only | no | no | no |
| nair2026rupeebias (arXiv 2026) | explicit labels, not names | salary / price outputs | Hinglish only | no | no |
| mahajan2026ifaab (arXiv, 28 Oct 2026) | personas (signal type unverified) | free-text financial advice; GPT-4o | unverified | no | no |
| nawale2025fairi (ACL 2025) | group terms | judgement tasks, no paired applications | no | no | no |
| arcuschin2026biases (ICML 2026) | no (US-style; religion stated explicitly) | yes (hiring, loan, admissions) | no | **yes** (verbalisation rate on discordant pairs) | no |
| karvonen2025robustly | no (race, gender) | yes (hiring) | no | qualitative (bias "invisible" in CoT) | no |
| matton2025walk (ICLR 2025) | no (BBQ) | QA, not decisions | no | **yes** | no |
| christian2026self (arXiv 2026) | no (gender, race) | yes (incl. scholarship) | no | no | **partly** (counterfactual self-simulation) |
| **Our study** | yes | yes | yes | yes | yes |

The stop condition in the brief ("if they have, stop and report") is **not triggered**. Our
searches covered caste hiring, Indian-name resume screening, LLM loan approval in India, Hindi vs
English decisions, caste-surname counterfactuals, scholarship/admissions, and bias-disclosure in
explanations. They were thorough but not exhaustive, so the paper should say "to our knowledge".

## 2. What changes: the novelty claim must be narrower

The proposal says *"No study we know of measures both [decision bias and explanation
faithfulness] on the same … prompts."* For Western markers this is **no longer true**:
arcuschin2026biases measures exactly that (decision flip + whether the CoT mentions the swapped
concept) on hiring, loan and admissions tasks, and matton2025walk / karvonen2025robustly /
turpin2023language show biased explanations that hide the cause.

**Recommended restated contribution** (does not change RQ1–RQ4, only how we frame them):

1. The first paired audit of **Indian name-coded identity** (caste-coded surname, religion,
   region, gender) on **yes/no allocation decisions** across open-weight model families, with a
   within-group control as the noise floor.
2. The first **English vs Devanagari Hindi** comparison of such decision bias.
3. Extending explanation-disclosure measurement (arcuschin2026biases, matton2025walk) to
   **implicit, name-coded Indian markers**, which are harder for a model to "notice" than an
   explicit sentence like "I am a practising Hindu".
4. A direct **self-prediction probe** ("would your decision change if the surname were X?")
   scored against the model's actual paired behaviour; only christian2026self is close.
5. A **within-family scale** analysis (RQ4).

This is a framing change, not a scope change, but the humans should agree to it (flagged for
checkpoint (a)).

## 3. Specific gaps and how our design answers them

**G1 — Conflicting evidence on Indian name bias in decisions.** zaveri2025caste reports strong
dominant-caste preference in ChatGPT shortlisting; rao2025invisible finds *no* significant caste
or region effect with GPT-4o (n = 50 transcripts). Neither uses open-weight models, yes/no
decisions with confidence, or a noise floor. *Our answer:* paired P(Yes) shifts with bootstrap
CIs compared against same-group control swaps, borderline-heavy profiles, three scenarios. A
tight null is a publishable answer to this conflict.

**G2 — Language.** Indian-context bias work is almost all English (khandelwal2024indian,
sahoo2024indibias, nawale2025fairi) or Hinglish (nair2026rupeebias). Multilingual bias work
(e.g. vashishtha2023evaluating, tomar2025bharatbbq) uses stereotype or QA tasks, not decisions.
*Our answer:* identical applications in English and Devanagari Hindi (RQ2).

**G3 — Disclosure of implicit Indian markers.** Disclosure has been measured only for explicit or
Western markers. *Our answer:* mention rate on flipped pairs (RQ3a).
*Design issue for Phase 2:* with name-coded signals, what counts as a "mention"? Options: (i)
names the attribute (caste, religion, region, gender), (ii) refers to the applicant's name or
background at all. We should pre-register a definition and report both.

**G4 — Self-prediction.** Introspection work (binder2025looking) and counterfactual
simulatability (chen2024models, christian2026self) suggest models predict their own behaviour
poorly, but nobody has scored a direct "would you change your decision?" probe against actual
counterfactual outcomes for Indian identity swaps. *Our answer:* RQ3b.

**G5 — Scale.** Most audits test one or a few unrelated models. *Our answer:* one family at three
sizes (RQ4). Prior results on whether bias shrinks with scale are mixed, so either direction is
informative.

## 4. Methods we should borrow (with citations)

- **Yes/No probability as a continuous decision score**, normalised over the two tokens:
  tamkin2023evaluating.
- **McNemar's test on discordant pairs plus a verbalisation rate on those same pairs:**
  arcuschin2026biases. Using the same definition makes our RQ3 numbers comparable to theirs.
- **Correlational counterfactual test (CCT / phi-CCT):** correlate |ΔP(Yes)| with whether the
  explanation mentions the attribute, so that we use all pairs, not only flips
  (siegel2024probabilities, siegel2025verbosity). siegel2025verbosity also warns that keyword
  matching is biased by explanation length; we should report explanation length per group.
- **Counterfactual mention test** framing: atanasova2023faithfulness.
- **Judge validation with chance-corrected agreement** (Cohen's kappa, not raw accuracy):
  thakur2025judging, bavaresco2025llms. arcuschin2026biases reports human–human kappa = 0.737
  for a similar verbalisation judgement, which is a useful benchmark for our 200-label study.
- **Framing faithfulness as self-consistency**, not as access to internal mechanisms:
  parcalabescu2024measuring.
- **Name-list validation tools:** Outkast (SC/ST vs other share per surname), Pranaam (Muslim
  association of names), Naampy (gender of first names); OBC lists cross-checked against the
  central OBC list, following vijayaraghavan2025decaste (see `lit/notes.md`, last section).

## 5. Risks the literature points to

1. **Small effects.** rao2025invisible's null result means we may see few flips on strong or
   weak profiles. Borderline-heavy sampling and the continuous P(Yes) metric are essential.
2. **Signal strength.** Name-coded caste is weaker than an explicit label (nair2026rupeebias uses
   labels and finds large effects). We may need a manipulation check: can the model identify the
   coded attribute from the name? Cheap, and it separates "model is fair" from "model did not
   notice". *Recommended for Phase 2.*
3. **Post-hoc explanations vs CoT.** Blind Spot analyses reasoning *before* the decision; our
   explanation pass asks for decision + justification. The decision in the explanation pass may
   differ from the decision pass; Phase 2 must define how to handle disagreement.
4. **Hindi tokenisation.** The single-token "हाँ / नहीं" answer may not be one token in every
   tokenizer; Phase 2 must check this per model or keep the answer tokens in English.

## 6. Items still unverified

- zaveri2025caste: paper exists (OpenAlex), but the PDF was blocked on recheck; method details
  rely on one reviewer's reading. Re-open before citing specific numbers.
- Thorat & Attewell 2007 and Shah 2024: seen only via secondary citations; **not** in refs.bib.
- Some 2026 venue labels come from arXiv comments only (see `lit/ref_check.csv` and the notes).
