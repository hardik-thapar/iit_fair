# Literature notes — explanation faithfulness, self-knowledge, LLM-as-judge

Compiled 2026-10-30 by the Lit Reviewer (faithfulness and judge areas). Every entry below was opened at the URL given (arXiv abstract page via the arXiv API or web, ACL Anthology, PMLR, or ICLR/ICML virtual pages). Venue notes marked "per arXiv comment" come from the author-supplied arXiv comment field; the proceedings page itself was not opened. BibTeX is in `lit/refs_faithfulness.bib`.

---

## A. CoT and self-explanation faithfulness

### turpin2023language — Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting (Turpin, Michael, Perez, Bowman, 2023, NeurIPS 2023)
URL: https://arxiv.org/abs/2305.04388   Verified: yes (opened arXiv abstract + HTML full text)
Summary: Biasing features such as "answer is always (A)" few-shot ordering shift GPT-3.5 and Claude 1.0 answers on 13 BIG-Bench Hard tasks (up to 36% accuracy drop), and the CoT never mentions the bias. In a BBQ social-bias experiment (2,592 examples, 9 categories), the authors swap weak evidence between individuals. Unfaithful explanation pairs lean stereotype-aligned (e.g. 62.5% for Claude 1.0), and only 1 of 192 inspected explanations mentioned the stereotype.
Relevance: This is the canonical "explanation omits the real cause" result, and it includes a social-bias case. We borrow the "decision changed but explanation silent" logic. Differences: BBQ is a QA benchmark, not a decision task; the markers are US-centric; and the perturbation targets the evidence rather than the identity marker on an otherwise identical application.

### lanham2023measuring — Measuring Faithfulness in Chain-of-Thought Reasoning (Lanham, Chen, Radhakrishnan, … Bowman, Perez; 30 authors, 2023, arXiv preprint)
URL: https://arxiv.org/abs/2307.13702   Verified: yes (opened arXiv API record)
Summary: The authors intervene on the CoT itself (truncating it, adding mistakes, paraphrasing it, or replacing it with filler tokens) and measure how much the answer depends on it. How much models rely on CoT varies strongly by task, and larger models often produce *less* faithful reasoning (inverse scaling).
Relevance: This motivates RQ4 (scale) and the claim that faithfulness cannot be assumed. Our design intervenes on the *input* (the identity marker), not the CoT. No later peer-reviewed venue was found.

### chen2024models — Do Models Explain Themselves? Counterfactual Simulatability of Natural Language Explanations (Chen, Zhong, Ri, Zhao, He, Steinhardt, Yu, McKeown, 2024, ICML 2024 / PMLR 235)
URL: https://proceedings.mlr.press/v235/chen24bl.html (arXiv 2307.08678)   Verified: yes (opened arXiv record; PMLR/ICML listing confirmed via search results)
Summary: The paper defines counterfactual simulatability: whether an explanation lets an observer predict the model's outputs on counterfactual inputs. It is scored by simulation precision and generality. Explanations from GPT-3.5/GPT-4 have low precision, and precision does not correlate with plausibility.
Relevance: This is the conceptual basis for our self-prediction probe ("Would your decision change if the surname were X?"). That probe is a direct, model-as-its-own-simulator variant of counterfactual simulatability, restricted to identity counterfactuals.

### atanasova2023faithfulness — Faithfulness Tests for Natural Language Explanations (Atanasova, Camburu, Lioma, Lukasiewicz, Simonsen, Augenstein, 2023, ACL 2023 short)
URL: https://aclanthology.org/2023.acl-short.25/   DOI: 10.18653/v1/2023.acl-short.25   Verified: yes (opened arXiv API record; Anthology details confirmed via search)
Summary: The paper proposes (i) a counterfactual test: insert words that flip the prediction and check whether the natural-language explanation (NLE) mentions them, and (ii) an input-reconstruction test. Applied to e-SNLI, ComVE and similar tasks, both tests find many unfaithful NLEs.
Relevance: Our RQ3 metric (flip ⇒ does the explanation mention the swapped attribute?) is this counterfactual test, with a human-meaningful identity edit in place of an arbitrary inserted word. Cite it as the metric's origin.

### madsen2024self — Are self-explanations from Large Language Models faithful? (Madsen, Chandar, Reddy, 2024, Findings of ACL 2024)
URL: https://aclanthology.org/2024.findings-acl.19/   Verified: yes (opened arXiv API record; Anthology ID confirmed via search)
Summary: Self-consistency checks for counterfactual, feature-attribution and redaction self-explanations (e.g. remove the words the model says matter and check whether the prediction changes) on Llama2, Mistral and Falcon. Faithfulness depends on model, task and explanation type.
Relevance: This supports treating self-explanations as testable claims. Our self-prediction probe is a counterfactual self-explanation that we check against the model's actual behaviour on the swapped prompt.

### parcalabescu2024measuring — On Measuring Faithfulness or Self-consistency of Natural Language Explanations (Parcalabescu, Frank, 2024, ACL 2024 long)
URL: https://aclanthology.org/2024.acl-long.329/   DOI: 10.18653/v1/2024.acl-long.329   Verified: yes (opened arXiv API record; Anthology ID confirmed via search)
Summary: The authors argue that existing "faithfulness" tests measure output-level self-consistency, not faithfulness to inner workings. They introduce CC-SHAP and compare tests on 11 open LLMs × 5 tasks.
Relevance: This is an important framing caveat. Our mention-on-flip and self-prediction metrics are behavioural self-consistency measures, and the paper should say so rather than claim mechanistic faithfulness.

### siegel2024probabilities — The Probabilities Also Matter: A More Faithful Metric for Faithfulness of Free-Text Explanations in Large Language Models (Siegel, Camburu, Heess, Perez-Ortiz, 2024, ACL 2024 short)
URL: https://aclanthology.org/2024.acl-short.49/   DOI: 10.18653/v1/2024.acl-short.49   Verified: yes (opened ACL Anthology page)
Summary: This paper introduces the Correlational Counterfactual Test (CCT). It correlates the *size* of the shift in predicted label probabilities caused by an input edit with whether the explanation mentions the edited factor, rather than using binary flips only. Explanations from Llama-2 more often mention impactful factors, and this effect grows with model size.
Relevance: This matches our dual outcome (flip and P(Yes) shift) closely. We can report a CCT-style correlation between |ΔP(Yes)| and mention rate, not only mention-given-flip. Strongly recommended to adopt.

### siegel2025verbosity — Verbosity Tradeoffs and the Impact of Scale on the Faithfulness of LLM Self-Explanations (Siegel, Heess, Perez-Ortiz, Camburu, 2025, ICLR 2026 Workshop on Principled Design for Trustworthy AI)
URL: https://arxiv.org/abs/2503.13445   Verified: yes (opened arXiv abstract page)
Summary: Counterfactual faithfulness across 75 models from 13 families. The paper introduces phi-CCT, a variant of CCT that needs no token probabilities, and analyses how verbose explanations inflate mention-based metrics. Larger models are more faithful on all metrics.
Relevance: phi-CCT fits our flip-only analyses, and the verbosity caveat applies to keyword mention detection (a long explanation mentions more things). The scale result is a prior for RQ4.

### chen2025reasoning — Reasoning Models Don't Always Say What They Think (Chen, Benton, Radhakrishnan, Uesato, Denison, Schulman, Somani, Hase, Wagner, Roger, Mikulik, Bowman, Leike, Kaplan, Perez, 2025, arXiv preprint)
URL: https://arxiv.org/abs/2505.05410   Verified: yes (opened arXiv API record)
Summary: The authors measure how often reasoning models (Claude 3.7 Sonnet, DeepSeek R1) verbalise 6 kinds of prompt hints they actually used. Reveal rates are often under 20%. Outcome-based RL raises faithfulness at first, then plateaus.
Relevance: Our "verbalisation rate" is the same quantity (P(mention | attribute used)) applied to identity markers. If we test any reasoning-mode open model (e.g. Qwen3 thinking), this is the reference. No peer-reviewed venue found.

### arcuschin2025chain — Chain-of-Thought Reasoning In The Wild Is Not Always Faithful (Arcuschin, Janiak, Krzyzanowski, Rajamanoharan, Nanda, Conmy, 2025, ICML 2026 per arXiv comment)
URL: https://arxiv.org/abs/2503.08679   Verified: yes (opened arXiv API record)
Summary: Unfaithful CoT also occurs on natural, non-adversarial prompts. For example, models answer "Is X > Y?" and "Is Y > X?" both Yes and rationalise each answer (implicit post-hoc rationalisation), and they take unfaithful shortcuts in maths.
Relevance: This supports our paired design. A model answering "Yes" for one surname and "No" for another with different neutral-sounding rationales is the same pair-inconsistency pattern in a fairness setting.

### matton2025walk — Walk the Talk? Measuring the Faithfulness of Large Language Model Explanations (Matton, Ness, Guttag, Kıcıman, 2025, ICLR 2025 spotlight)
URL: https://arxiv.org/abs/2504.14150   Verified: yes (opened arXiv API record + HTML full text)
Summary: Defines faithfulness as the gap between concepts an explanation *implies* are influential and concepts that *causally* are. An auxiliary LLM edits concepts to build counterfactuals, and a Bayesian hierarchical model estimates their effects. On a BBQ-based social-bias task, GPT-3.5 explanations hid identity influence (e.g. income), and refusals were attributed to "ambiguity" rather than identity. There is also a medical QA task.
Relevance: **Close methodological prior.** Concept counterfactuals that include identity concepts, plus a check of whether explanations cite them. Differences: QA benchmarks rather than application decisions, Western identity concepts only, English only, proprietary models, and no self-prediction probe.

### mayne2026positive — A Positive Case for Faithfulness: LLM Self-Explanations Help Predict Model Behavior (Mayne, Kang, Gould, Ramchandran, Mahdi, Siegel, 2026, ICML 2026 per arXiv comment)
URL: https://arxiv.org/abs/2602.02639   Verified: yes (opened arXiv abstract page)
Summary: The paper proposes Normalized Simulatability Gain (NSG). Across about 7k counterfactuals (health, business, ethics) and 18 models, self-explanations improve prediction of model behaviour by 11–37% NSG and beat explanations written by other models. However, 5–15% of self-explanations are highly misleading.
Relevance: A counterpoint for our discussion: self-explanations carry real information on average. Our question is whether the misleading tail concentrates in identity-driven flips.

## B. Faithfulness in fairness-critical decisions (closest to our RQ3)

### arcuschin2026biases — Biases in the Blind Spot: Detecting What LLMs Fail to Mention (Arcuschin, Chanin, Garriga-Alonso, Camburu, 2026, ICML 2026 per arXiv comment)
URL: https://arxiv.org/abs/2602.10117   Verified: yes (opened arXiv abstract page)
Summary: An automated black-box pipeline. LLM autoraters propose candidate concepts, the pipeline generates positive/negative input variations and tests them with multiple-testing control and early stopping, and a concept is flagged as an *unverbalized bias* if it significantly changes decisions but is never cited in the CoT. The tasks are **hiring, loan approval and university admissions**, with 7 LLMs. It recovers known unverbalized gender, race, religion and ethnicity biases, plus new ones (Spanish fluency, English proficiency, writing formality).
Relevance: **The closest prior work, and it narrows our novelty.** It already measures "decision changes but CoT doesn't mention the attribute" on our three scenario types and includes religion. As far as the abstract shows, it does not test caste-coded surnames, Indian regions, Hindi-language prompts, or self-prediction of counterfactual behaviour, and it does not validate a mention judge against human labels (full text not read; confirm before claiming).

### karvonen2025robustly — Robustly Improving LLM Fairness in Realistic Settings via Interpretability (Karvonen, Marks, 2025, arXiv preprint)
URL: https://arxiv.org/abs/2506.10922   Verified: yes (opened arXiv abstract page)
Summary: Anti-bias prompts work in toy settings but fail once realistic hiring context is added. Six models show up to 12% race/gender interview-rate gaps (favouring Black and female candidates), and the bias is "invisible even when inspecting the model's chain-of-thought". Affine concept editing on race/gender directions cuts the bias to <1–2.5%.
Relevance: A direct prior finding that hiring bias is not visible in CoT (US race/gender). It supports our hypothesis and shows that open models (Gemma, Mistral) are susceptible. They study mitigation, not a mention-rate metric or self-prediction.

### christian2026self — Self-Blinding and Counterfactual Self-Simulation Mitigate Biases and Sycophancy in Large Language Models (Christian, Mazor, 2026, arXiv preprint)
URL: https://arxiv.org/abs/2601.14553   Verified: yes (opened arXiv abstract page)
Summary: LLMs, like humans, cannot simulate what they would decide without biasing information (gender/race, e.g. scholarship recommendations). Telling them to ignore it fails or backfires. Querying a "blinded replica" via their own API gives fairer decisions.
Relevance: **Close to our self-prediction RQ.** It shows models are poor counterfactual self-simulators for demographic attributes. Our probe asks the model to *predict* its own counterfactual decision (not to act blinded), with Indian markers and in Hindi. The exact protocol needs checking in the full text.

### veldanda2026explanation — Explanation Fairness in Large Language Models: An Empirical Analysis of Disparities in How LLMs Justify Decisions Across Demographic Groups (Veldanda, 2026, arXiv preprint)
URL: https://arxiv.org/abs/2605.08671   Verified: yes (opened arXiv abstract page)
Summary: An Explanation Fairness Taxonomy (verbosity, sentiment, hedging, decision-linked explanation, lexical complexity) with an "Explanation Faithfulness Proxy". It covers hiring, triage, credit and legal domains with 5 models (incl. Llama 3.3 70B, Qwen3 32B). All metrics show significant demographic disparities.
Relevance: Adjacent. It studies whether explanation *style and quality* differ by group, not whether explanations disclose the identity driver. Cite as related "explanation fairness" work. Attributes tested were not stated on the abstract page.

### binder2025looking — Looking Inward: Language Models Can Learn About Themselves by Introspection (Binder, Chua, Korbak, Sleight, Hughes, Long, Perez, Turpin, Evans, 2025, ICLR 2025)
URL: https://arxiv.org/abs/2410.13787   Verified: yes (opened arXiv API record; ICLR 2025 poster listing confirmed via search)
Summary: Models fine-tuned to predict properties of their own hypothetical behaviour (GPT-4, GPT-4o, Llama-3) predict themselves better than a second model trained on the first's behaviour does. This is evidence of privileged self-access, but only on simple tasks.
Relevance: This grounds our self-prediction probe ("Would your decision change if…?"). We test it zero-shot, without fine-tuning, on a fairness-relevant hypothetical, a harder out-of-distribution case where they found introspection weak.

## C. LLM-as-judge reliability (for our mention judge)

### zheng2023judging — Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng, Chiang, Sheng, Zhuang, Wu, Zhuang, Lin, Li, Li, Xing, Zhang, Gonzalez, Stoica, 2023, NeurIPS 2023 Datasets & Benchmarks)
URL: https://arxiv.org/abs/2306.05685   Verified: yes (opened arXiv API record)
Summary: Introduces MT-Bench and Chatbot Arena. GPT-4 as judge agrees with human preferences at about 80%, comparable to inter-human agreement. The paper documents position, verbosity and self-enhancement biases.
Relevance: The standard citation for using an LLM judge. Its verbosity and position biases motivate our controls: randomise order, fix the rubric, and use a judge from a different family than the audited models to avoid self-enhancement.

### wang2024large — Large Language Models are not Fair Evaluators (Wang, Li, Chen, Cai, Zhu, Lin, Cao, Kong, Liu, Liu, Sui, 2024, ACL 2024 long)
URL: https://aclanthology.org/2024.acl-long.511/   DOI: 10.18653/v1/2024.acl-long.511   Verified: yes (opened ACL Anthology page)
Summary: GPT-4 and ChatGPT judge rankings can be flipped just by changing the order of the candidates. Proposed fixes are multiple-evidence calibration, balanced-position calibration and human-in-the-loop calibration.
Relevance: Supports judge-robustness checks. Our judge task is single-item classification ("does the explanation reference caste/religion/…?"), so position bias matters less, but prompt-sensitivity checks still apply.

### thakur2025judging — Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges (Thakur, Choudhary, Ramayapally, Vaidyanathan, Hupkes, 2025, GEM² Workshop at ACL 2025)
URL: https://aclanthology.org/2025.gem-1.33/ (arXiv 2406.12624)   Verified: yes (opened arXiv API record, whose journal-ref gives GEM² 2025 pp. 404–430)
Summary: 13 judge models score answers from 9 exam-taker models in a "clean" setting where humans agree highly. Only the largest judges align reasonably with humans, and even they trail inter-human agreement. **High percent agreement can coexist with very different scores**, so the authors argue for chance-corrected or alignment metrics beyond percent agreement. Judges also tend to be lenient and are sensitive to prompt complexity and length. (Benchmark name and the exact chance-corrected statistic, Cohen's κ vs Scott's π, were not confirmed from the abstract: [UNVERIFIED].)
Relevance: Justifies reporting a chance-corrected statistic (our **Cohen's kappa**) rather than raw agreement for our judge against 200 human labels. We should report both, plus per-attribute and per-language κ.

### bavaresco2025llms — LLMs instead of Human Judges? A Large Scale Empirical Study across 20 NLP Evaluation Tasks (Bavaresco, Bernardi, Bertolazzi, … Plank, … Testoni; 20 authors, 2025, ACL 2025 short)
URL: https://aclanthology.org/2025.acl-short.20/   DOI: 10.18653/v1/2025.acl-short.20   Verified: yes (opened arXiv API record; Anthology ID/pages 238–255 confirmed via search)
Summary: JUDGE-BENCH has 20 human-annotated datasets and 11 open and proprietary LLMs. Correlation with humans varies widely across tasks, properties and annotator expertise, and the authors recommend validating against human labels for each task.
Relevance: Supports our decision to validate the judge on our own 200 labels rather than assume transfer. It includes open-weight judges, which suits a fully local pipeline.

### gu2024survey — A Survey on LLM-as-a-Judge (Gu, Jiang, Shi, Tan, Zhai, Xu, Li, Shen, Ma, Liu, Wang, Zhang, Wang, Gao, Ni, Guo, 2024, arXiv preprint)
URL: https://arxiv.org/abs/2411.15594   Verified: yes (opened arXiv API record)
Summary: A survey of LLM-as-a-judge: how to build reliable judges (prompting, consistency, bias mitigation), a taxonomy of judge biases, and evaluation of the judges themselves.
Relevance: A general reference for judge-design choices (rubric prompt, low temperature, rationale before label). A later journal venue was not verified, so cite as arXiv.

## D. Indian-context items found during the novelty check (for the decision-bias reviewer to cross-check)

### rao2025invisible — Invisible Filters: Cultural Bias in Hiring Evaluations Using Large Language Models (Rao, Venkatesan, Cherubini, Jayagopi, 2025, AIES 2025 per arXiv comment)
URL: https://arxiv.org/abs/2508.16673   Verified: yes (opened arXiv abstract page)
Summary: Compares 100 UK and 100 Indian interview transcripts scored by an LLM. Indian transcripts score lower even when anonymised, a gap linked to linguistic features. Name swaps for gender, **caste** and **region** produced no significant effect.
Relevance: Indian caste/region name swaps in hiring, so it overlaps RQ1. It reports a null result for names alone, which matters for our power analysis. No explanation-faithfulness analysis is described in the abstract.

### gupta2026compounding — Compounding Disadvantage: Auditing Intersectional Bias in LLM-Generated Explanations Across Indian and American STEM Education (Gupta, Patil, Ghosh, Gaikwad, 2026, arXiv preprint)
URL: https://arxiv.org/abs/2601.14506   Verified: yes (opened arXiv abstract page)
Summary: Audits 4 LLMs (incl. Qwen 2.5-32B, GPT-OSS 20B) generating STEM *educational* explanations for synthetic student profiles with Indian attributes (caste, medium of instruction, college tier). Marginalised profiles receive simpler content (up to 2.55 grade levels lower).
Relevance: Uses caste in an LLM audit, but "explanations" here means tutoring content, not decision rationales. It does not compete with RQ3. It mainly shows that caste-attribute audits exist in 2026.

---

## Closest prior work to our study

1. **arcuschin2026biases (Biases in the Blind Spot, ICML 2026)** — the closest. *Overlap:* paired input variations on **hiring, loan approval and admissions**, with a test of whether the decision-changing concept is **verbalised in the CoT**; it covers gender, race, religion and ethnicity. *Not done (per abstract):* caste-coded surnames, Indian regions, Hindi prompts, asking the model to self-predict its counterfactual decision, P(Yes)-shift (vs. accuracy-difference) analysis, scale-within-family, or human-validated (κ) mention judging. **Our "first to measure decision bias + explanation disclosure together" claim is no longer true in general.** Novelty must be restated as: *Indian identity markers (caste/region) + Hindi vs English + self-prediction probe + κ-validated mention detection on open-weight model families.*
2. **matton2025walk (Walk the Talk, ICLR 2025)** — *Overlap:* counterfactual edits of identity concepts plus a check of whether explanations cite them, and finds explanations hide social-bias influence. *Not done:* real decision applications (it uses BBQ QA), non-Western markers, other languages, open-weight scale study, self-prediction.
3. **karvonen2025robustly (Karvonen & Marks 2025)** — *Overlap:* LLM hiring decisions with race/gender swaps on open models (Gemma, Mistral); bias is invisible in CoT. *Not done:* a systematic mention-rate metric, loans or scholarships, Indian markers, Hindi, self-prediction (the focus is mitigation by activation editing).
4. **turpin2023language (Turpin et al., NeurIPS 2023)** — *Overlap:* the founding result that explanations rationalise stereotype-aligned answers without mentioning the bias (BBQ). *Not done:* decision tasks, identity-marker swaps on fixed applications, non-Western or multilingual settings.
5. **christian2026self (Christian & Mazor 2026)** — *Overlap:* models' ability to counterfactually simulate their own decisions without gender/race information (including a scholarship case). *Not done:* a direct verbal self-prediction accuracy metric ("would your decision change?") scored against actual paired outcomes, Indian markers, Hindi, explanation-mention analysis (protocol details unverified, abstract only).

**Bottom line:** No paper found combines Indian identity markers (caste-coded surnames, region) or Hindi with explanation-disclosure or self-prediction measurement. Indian decision-bias audits found here (rao2025invisible) do not analyse explanations. However, the general question "does the CoT mention the demographic attribute that changed a hiring/loan/admissions decision?" **has already been studied** (arcuschin2026biases; also karvonen2025robustly, matton2025walk). The paper should cite these prominently and frame its contribution as extending them to the Indian and Hindi setting, adding the self-prediction probe, and contributing the human-validated judge.

**Methodological borrowings:** the counterfactual mention test (atanasova2023faithfulness); CCT/phi-CCT correlating |ΔP(Yes)| with mention (siegel2024probabilities, siegel2025verbosity), including the verbosity caveat for keyword matching; counterfactual simulatability (chen2024models) and introspection (binder2025looking) for the self-prediction probe; chance-corrected agreement (Cohen's κ) over raw agreement for judge validation (thakur2025judging, bavaresco2025llms); framing as self-consistency rather than mechanistic faithfulness (parcalabescu2024measuring).
