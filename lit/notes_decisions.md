# Literature notes — LLM decision discrimination, audits, counterfactual fairness

Lit Reviewer, compiled 2026-10-30. Every entry below was opened at the source named in "Verified". Anything not confirmed at a primary record is marked `[UNVERIFIED]`. Summaries come from abstracts and, where noted, the paper's HTML. Before quoting a number in the paper, re-check it against the PDF.

---

## Area 1a — Classic correspondence (field) audits

### bertrand2004emily — Are Emily and Greg More Employable Than Lakisha and Jamal? A Field Experiment on Labor Market Discrimination (Bertrand & Mullainathan, 2004, American Economic Review 94(4):991–1013)
URL: https://doi.org/10.1257/0002828042002561   Verified: yes (opened Crossref record)
Summary: The authors sent fictitious resumes to job ads in Boston and Chicago and randomly assigned African-American- or White-sounding names. White names received about 50% more callbacks. Callbacks also responded more to resume quality for White names.
Relevance: This is the template for our paired name-swap design: identical profile, only the name changes. We transfer it to LLM deciders and Indian markers, and we measure a continuous P(Yes) shift as well as a binary "callback".

### banerjee2009labor — Labor market discrimination in Delhi: Evidence from a field experiment (Banerjee, Bertrand, Datta & Mullainathan, 2009, Journal of Comparative Economics 37(1):14–27)
URL: https://doi.org/10.1016/j.jce.2008.09.002   Verified: yes (opened Crossref and OpenAlex records; online 2008, issue dated March 2009)
Summary: A correspondence study in Delhi that sent applications varying caste (and religion; OpenAlex tags it Caste/Tribe/Callback) to software and call-centre jobs. [UNVERIFIED: the Crossref record has no abstract, so I could not confirm the specific findings, e.g. little caste gap for software jobs and some gap for call-centre jobs. Read the paper before citing results.]
Relevance: This is the closest human-audit precedent for caste-coded names in Indian hiring, and its software-job setting matches our fresher-SWE scenario. Use it to justify the caste/religion markers and as the human baseline LLMs could reproduce.

> **Thorat & Attewell (2007), "The Legacy of Social Exclusion: A Correspondence Study of Job Discrimination in India", Economic and Political Weekly 42(41):4141–4145.** `[UNVERIFIED — NOT INCLUDED IN .bib]`. I found this only as a secondary citation, in a World Bank bibliography and an Authorea preprint reference list. It also appears as Ch. 1 of *Blocked by Caste* (Thorat & Newman eds., OUP). I could not open an EPW, JSTOR, Crossref or OpenAlex record for it. It is very likely real and central (Dalit and Muslim surnames on resumes sent to private-sector jobs). Someone with EPW or JSTOR access should confirm the volume, issue and pages before it is cited.

---

## Area 1b — LLMs as decision-makers: name/demographic-swap audits

### tamkin2023evaluating — Evaluating and Mitigating Discrimination in Language Model Decisions (Tamkin, Askell, Lovitt, Durmus, Joseph, Kravec, Nguyen, Kaplan & Ganguli, 2023, arXiv preprint)
URL: https://arxiv.org/abs/2312.03689   Verified: yes (opened arXiv abstract page; no journal-ref or venue listed)
Summary: An LLM generated 70 yes/no decision scenarios (loans, housing, etc.) and the demographic details in each were varied. They measured discrimination in Claude 2.0 and found both positive and negative discrimination in some settings. Prompt interventions substantially reduced it. They released the dataset.
Relevance: This is the direct methodological parent: templated yes/no decisions with demographic variation, read through the probability of "yes". Its markers are US-centric (explicit age, gender and race), it tests one proprietary model, and it does not analyse explanations or Indian markers.

### an2024large — Do Large Language Models Discriminate in Hiring Decisions on the Basis of Race, Ethnicity, and Gender? (An, Acquaye, Wang, Li & Rudinger, 2024, ACL 2024 Short Papers, pp. 386–397)
URL: https://aclanthology.org/2024.acl-short.37/   Verified: yes (opened ACL Anthology page)
Summary: LLMs wrote acceptance or rejection emails, and only the applicant's first name was varied. Models favoured White over Hispanic applicants in many settings. Masculine White names had the highest acceptance and masculine Hispanic names the lowest. The direction of effects was sensitive to the prompt template.
Relevance: Supports our use of first names as the signal and our use of two paraphrased templates, since the paper shows template sensitivity. It is US-only and uses the binary outcome with no explanation analysis.

### salinas2024whats — What's in a Name? Auditing Large Language Models for Race and Gender Bias (Salinas, Haim & Nyarko, 2024, arXiv preprint; v3 Jan 2025)
URL: https://arxiv.org/abs/2402.14875   Verified: yes (opened arXiv abstract page; no venue listed; author order changed between v1 and v3, and v3 is used here)
Summary: The authors asked GPT-4o, GPT-4, GPT-3.5, Llama-3-70B, Mistral Large and PaLM-2 for advice about a named individual (salary, car negotiation, etc.) and varied names correlated with race and gender. Names associated with minorities and women were systematically disadvantaged, with Black women worst. Numerical, decision-relevant anchors reduced the bias. (Model list from search-result summary of the paper.)
Relevance: Supports a classic audit design with names as proxies. The anchoring finding suggests that our "strong" profiles should show less bias than borderline ones, which motivates our borderline-heavy design.

### armstrong2024silicon — The Silicon Ceiling: Auditing GPT's Race and Gender Biases in Hiring (Armstrong, Liu, MacNeil & Metaxa, 2024, EAAMO '24, pp. 1–18)
URL: https://doi.org/10.1145/3689904.3694699   Verified: yes (opened arXiv 2405.04412 page and Crossref record: Proc. 4th ACM Conf. on Equity and Access in Algorithms, Mechanisms, and Optimization)
Summary: A resume-audit-style study of GPT-3.5. Study 1 scored resumes with race- and gender-coded names across 10 occupations and found stereotype-based biases. Study 2 had the model generate resumes, which encoded stereotypes such as less experience for women and immigrant markers for Asian and Hispanic candidates.
Relevance: Another audit-study transfer to LLMs. It uses US markers, one closed model and scoring only.

### wilson2024gender — Gender, Race, and Intersectional Bias in Resume Screening via Language Model Retrieval (Wilson & Caliskan, 2024, AIES 2024)
URL: https://doi.org/10.1609/aies.v7i1.31748   Verified: yes (opened arXiv 2407.20371 page, whose comments give AIES 2024 and the DOI)
Summary: An embedding-retrieval resume screen over about 500 resumes, 500 job descriptions and 9 occupations, using massive text embedding models. White-associated names were favoured in 85.1% of tests and female names in only 11.1%. Black males were disadvantaged in up to 100% of cases.
Relevance: A large-scale name-swap audit, but for retrieval rather than generative yes/no decisions. Its significance testing over many paired comparisons is useful for our analysis plan.

### seshadri2025small — Small Changes, Large Consequences: Analyzing the Allocational Fairness of LLMs in Hiring Contexts (Seshadri, Chen, Singh & Goldfarb-Tarrant, 2025, arXiv preprint)
URL: https://arxiv.org/abs/2501.04316   Verified: yes (opened arXiv abstract page; no venue listed — [UNVERIFIED whether later published])
Summary: Synthetic resumes with controlled race and gender perturbations were used for summarisation and applicant ranking. Ranking was highly sensitive to the perturbations. Notably, retrieval models were about as sensitive to non-demographic changes as to demographic ones.
Relevance: Directly motivates our same-group control swaps. Effects must beat a noise floor of non-identity perturbations, otherwise "bias" may just be brittleness.

### bowen2025measuring — Measuring and Mitigating Racial Disparities in Large Language Model Mortgage Underwriting (Bowen, Price, Stein & Yang, 2025, ERES Working Paper eres2025_75)
URL: https://ideas.repec.org/p/arz/wpaper/eres2025_75.html   Verified: yes (opened RePEc/IDEAS record; first author's full name "Donald E. Bowen III" taken from search snippets only — [UNVERIFIED]; also listed as an AEA 2026 conference paper, not opened)
Summary: Real HMDA loan applications were used with race and credit score varied experimentally. LLMs recommended more denials and higher rates for Black applicants, with the largest gaps at low credit scores and for risky loans. Telling the model to be unbiased removed the approval gap.
Relevance: The closest lending-decision audit. It supports our loan scenario and our focus on borderline profiles, since bias concentrates at the margin. It is US and race-only, with no explanation analysis.

### gao2026llms — Can LLMs Hire Fairly? Racial Bias in Resume Screening (Gao, Jiang & Yan, 2026, arXiv preprint)
URL: https://arxiv.org/abs/2606.28978   Verified: yes (opened arXiv abstract page; no venue listed)
Summary: A paired-resume audit of 14 LLMs following Kline, Rose & Walters (2022), with 24,024 paired postings per model. The single 2023-vintage model reproduced a pro-White gap of +2.12 pp. Every model from 2024 onward showed a null or pro-Black reversal of up to −3.01 pp. Gender showed the same pattern.
Relevance: Shows that bias direction can flip across model generations. Our hypotheses should be two-sided, and we should report direction as well as magnitude, including for RQ4 on scale. It also offers a paired-statistics precedent.

### tan2026small — Small Changes, Big Impact: Demographic Bias in LLM-Based Hiring Through Subtle Sociocultural Markers in Anonymised Resumes (Tan, Khoo, Doan, Liu, Chen & Lee, 2026, EMNLP 2026)
URL: https://arxiv.org/abs/2603.05189   Verified: yes (opened arXiv abstract page; comments say "EMNLP 2026")
Summary: In a Singapore setting, 100 resumes were expanded into 4,100 variants across 4 ethnicities and 2 genders that differ only in proxy markers such as languages and hobbies. 18 LLMs were tested on 1v1 comparison and score-and-shortlist tasks. Models inferred demographics from the proxies and favoured Chinese and Caucasian males. Asking for a rationale could amplify bias.
Relevance: A non-Western, multi-model hiring audit, and the strongest evidence that explanation prompting changes decisions. Our explanation pass should therefore be kept separate from the decision pass, which our design already does. It does not cover India, caste or religion, or explanation faithfulness.

### rao2025invisible — Invisible Filters: Cultural Bias in Hiring Evaluations Using Large Language Models (Rao, Venkatesan, Cherubini & Jayagopi, 2025, AIES 2025, Vol. 8 No. 3, pp. 2164–2176)
URL: https://doi.org/10.1609/aies.v8i3.36703   Verified: yes (opened AIES OJS page and arXiv 2508.16673 HTML)
Summary: GPT-4o and Gemini Flash 1.5 scored real interview transcripts from the UK and India. Indian transcripts scored lower even when anonymised, which the authors link to linguistic features. In a GPT-4o-only Indian-name substitution test (gender × North/South region × upper/lower caste; 60 names; 50 transcripts × 8 conditions), caste and region had no significant effect and gender had only a weak effect.
Relevance: **The most similar study found: Indian-name swaps for caste, region and gender in an LLM hiring evaluation.** It reports a null result for caste and region, which we must cite and engage with. Differences: Likert scores rather than yes/no with P(Yes); a single model; no religion; no Hindi; no explanation analysis (named as future work); small n.

### zaveri2025caste — Caste And Occupational Identity In Large Language Models (Zaveri & Shah, 2025, IIM Bangalore Working Paper No. 724 / SSRN)
URL: https://doi.org/10.2139/ssrn.5427214   Verified: partial (opened OpenAlex record for title, authors, year and DOI; the IIMB PDF returned HTTP 403, so details come from search-result abstracts — [UNVERIFIED specifics])
Summary: Five studies on ChatGPT about caste and occupational identity in India. The model links Indian surnames to caste-typed occupations, under-represents marginalised castes, and shows selection bias: resumes with dominant-caste names were more likely to be shortlisted (reported as marginalised-caste picks only about 16% of the time — [UNVERIFIED number]). The authors propose a training approach to reduce the bias.
Relevance: **A direct precedent for caste-surname bias in LLM resume shortlisting.** It weakens any claim that ours is the "first caste hiring audit". Differences: one closed model; hiring only; no religion, region or Hindi; no paired P(Yes) or noise-floor control; no explanation or self-prediction analysis.

### phutane2026ableist — ABLEIST: Intersectional Disability Bias in LLM-Generated Hiring Scenarios (Phutane, Jung, Kim, Mitra & Vashistha, 2026, AIES 2026, Vol. 9 No. 3, pp. 2089–2104)
URL: https://doi.org/10.1609/aies.v9i3.43291   Verified: yes (opened AIES OJS page)
Summary: Six LLMs were audited across 2,820 India-situated hiring scenarios that vary disability, gender, nationality and caste. The paper proposes five ableism metrics and three intersectional-harm metrics. It finds much higher ableist harms, often missed by safety tools, and tokenism that increases for candidates marginalised by caste or gender.
Relevance: An India-focused hiring audit that includes caste. However, it measures harms in generated text (conversations), not accept/reject decisions or explanation faithfulness, and its main axis is disability.

### naik2026sima — Sima AIunty: Caste Audit in LLM-Driven Matchmaking (Naik, Kar, Sharma, Rajadesingan & Saha, 2026, arXiv preprint)
URL: https://arxiv.org/abs/2603.29288   Verified: yes (opened arXiv abstract page; no venue listed)
Summary: A controlled audit of real matrimonial profiles that varies caste (Brahmin, Kshatriya, Vaishya, Shudra, Dalit) and income across GPT, Gemini, Llama, Qwen and BharatGPT. Same-caste matches were rated up to 25% higher, and inter-caste matches were ordered by the traditional hierarchy.
Relevance: A counterfactual caste swap evaluated on LLM judgments, and it includes an Indic model (as we plan to). The domain is matchmaking, not allocation decisions, and it uses ratings rather than yes/no and has no explanation analysis.

---

## Area 1c — Decision bias combined with explanation faithfulness

### arcuschin2026biases — Biases in the Blind Spot: Detecting What LLMs Fail to Mention (Arcuschin, Chanin, Garriga-Alonso & Camburu, 2026, ICML 2026)
URL: https://arxiv.org/abs/2602.10117   Verified: yes (opened arXiv abstract page, which says "Accepted at ICML 2026", and the HTML)
Summary: An automated black-box pipeline. LLM autoraters propose candidate bias concepts, then paired positive and negative input variations test each concept with multiple-testing control. A concept is flagged when it changes decisions significantly but the chain-of-thought does not cite it. It covers hiring, loan approval and admissions across 7 LLMs (Gemma 3 12B and 27B, Gemini 2.5 Flash, GPT-4.1, Grok 4.1 Fast, QwQ-32B, Claude Sonnet 4). It recovers known gender, race and religion biases and finds new ones (e.g., Spanish fluency, writing formality). Verbalisation is judged by GPT-5-mini (κ=0.67 vs humans).
Relevance: **The closest prior work on our RQ3. It combines paired decision bias with whether the explanation mentions the attribute, in the same three domains.** Our "mention rate" is essentially their verbalisation check. Differences: no caste, no Indian names, no region, no Hindi (religion is stated explicitly, not name-coded); no self-prediction probe; no logit P(Yes); no scale sweep within one family.

### matton2025walk — Walk the Talk? Measuring the Faithfulness of Large Language Model Explanations (Matton, Ness, Guttag & Kıcıman, 2025, ICLR 2025)
URL: https://arxiv.org/abs/2504.14150   Verified: yes (opened arXiv abstract page, which says ICLR 2025 spotlight)
Summary: Faithfulness is defined as the gap between the concepts an explanation implies were influential and the concepts that causally were. An auxiliary LLM writes concept-level counterfactuals, and a Bayesian hierarchical model estimates the effects. On a social-bias task, the method finds explanations that conceal the influence of bias.
Relevance: Gives a principled counterfactual definition of explanation faithfulness that we can cite for RQ3. It is not India-specific, does not use realistic allocation decisions with Indian markers, and does not probe self-prediction.

### veldanda2026explanation — Explanation Fairness in Large Language Models: An Empirical Analysis of Disparities in How LLMs Justify Decisions Across Demographic Groups (Veldanda, 2026, arXiv preprint)
URL: https://arxiv.org/abs/2605.08671   Verified: yes (opened arXiv abstract page; no venue listed)
Summary: Measures disparities in how explanations are written (verbosity, sentiment, hedging, decision-linked content, lexical complexity) across demographic groups. It covers 80 templates in hiring, triage, credit and legal domains and 5 models (GPT-4.1, Claude Sonnet, Llama 3.3 70B, GPT-OSS 120B, Qwen3 32B). All metrics showed significant disparities. Prompting reduced the faithfulness-proxy gap by 78–95% but did not change the stylistic gaps.
Relevance: Adjacent to our work. It studies whether explanations differ by group, whereas we study whether explanations disclose the attribute that caused a flip. It does not cover the Indian context.

---

## Area 2 — Counterfactual fairness and counterfactual / perturbation evaluation of NLP models

### kusner2017counterfactual — Counterfactual Fairness (Kusner, Loftus, Russell & Silva, 2017, NeurIPS 2017 / Advances in Neural Information Processing Systems 30)
URL: https://papers.nips.cc/paper/6995-counterfactual-fairness   Verified: yes (opened NeurIPS proceedings page and arXiv 1703.06856)
Summary: A decision is counterfactually fair if it would be the same in a counterfactual world where the individual's protected attribute had been different. The definition is formalised with causal models.
Relevance: The formal grounding for our metric: a flip under an identity swap is a violation of counterfactual fairness at the level of the input text. We should note that a name swap is a proxy intervention, not a full causal counterfactual.

### garg2019counterfactual — Counterfactual Fairness in Text Classification through Robustness (Garg, Perot, Limtiaco, Taly, Chi & Beutel, 2019, AIES 2019, pp. 219–226)
URL: https://doi.org/10.1145/3306618.3317950   Verified: yes (opened Crossref record and arXiv 1809.10610)
Summary: Defines counterfactual token fairness (CTF): would the prediction change if the identity token in the input were substituted? It relates CTF to group fairness and compares blindness, counterfactual augmentation and counterfactual logit pairing for a toxicity classifier.
Relevance: Our identity swap is CTF applied to LLM decisions. Measuring the change in P(Yes) mirrors their logit-level comparison.

### prabhakaran2019perturbation — Perturbation Sensitivity Analysis to Detect Unintended Model Biases (Prabhakaran, Hutchinson & Mitchell, 2019, EMNLP-IJCNLP 2019, pp. 5740–5745)
URL: https://aclanthology.org/D19-1578/   Verified: yes (opened ACL Anthology page)
Summary: A framework for detecting biases tied to named entities by perturbing the names in inputs and measuring the change in a model's score. It needs no new annotation and was applied to sentiment and toxicity models.
Relevance: The precedent for name-perturbation scoring and for reporting a distribution of score shifts, not just averages. This applies to our ΔP(Yes) analysis.

### huang2020reducing — Reducing Sentiment Bias in Language Models via Counterfactual Evaluation (Huang, Zhang, Jiang, Stanforth, Welbl, Rae, Maini, Yogatama & Kohli, 2020, Findings of EMNLP 2020, pp. 65–83)
URL: https://aclanthology.org/2020.findings-emnlp.7/   Verified: yes (opened ACL Anthology page)
Summary: Swaps sensitive attributes (country, occupation, name/gender) in prompts and measures the shift in sentiment of the generated text, using individual and group fairness metrics adapted from fair ML. It finds substantial bias and mitigates it with embedding and sentiment regularisation.
Relevance: Gives a method for distinguishing individual (paired, within-template) from group counterfactual fairness metrics. Our flip rate and mean ΔP(Yes) follow the individual-fairness version.

### chaudhary2025certifying — Certifying Counterfactual Bias in LLMs (Chaudhary, Hu, Kumar, Ziyadi, Gupta & Singh, 2025, ICLR 2025)
URL: https://arxiv.org/abs/2405.18780   Verified: yes (opened arXiv abstract page, which says "Published at ICLR 2025")
Summary: LLMCert-B gives high-confidence bounds on the probability of unbiased responses over a distribution of counterfactual prompts that differ only by demographic group, rather than reporting point estimates on a fixed prompt set.
Relevance: The statistical framing for paired audits. It motivates reporting confidence intervals on per-attribute flip probability (our bootstrap CIs) and treating prompt and paraphrase variation as a distribution.

---

## Closest prior work to our study

1. **Rao et al. 2025, "Invisible Filters" (AIES 2025).** *Overlap:* LLM hiring evaluation with Indian-name swaps across gender, caste (upper/lower) and region (North/South), on Indian applicants. *Did not do:* religion, Hindi-language prompts, loan or scholarship decisions, binary decisions with logit P(Yes), multiple open-weight models or a scale sweep, a same-group noise-floor control, or any explanation or self-prediction analysis. *Key point:* they found **no significant caste or region effect** with GPT-4o (n=50 transcripts). Our study must cite this and can frame itself as testing whether that null result holds for open-weight models, for margin cases, and in Hindi.
2. **Arcuschin et al. 2026, "Biases in the Blind Spot" (ICML 2026).** *Overlap:* paired input variations in hiring, loan approval and admissions, flagging biases that change decisions but are not mentioned in the reasoning. This is our RQ3 "mention rate". *Did not do:* caste, Indian names, region, name-coded religion (religion was stated explicitly), Hindi, a self-prediction probe, logit-based P(Yes), or within-family scaling. **This substantially narrows our novelty claim for "decision bias + explanation disclosure". Our novelty must rest on the Indian markers, Hindi, self-prediction and scale.**
3. **Zaveri & Shah 2025, "Caste and Occupational Identity in LLMs" (IIMB WP 724).** *Overlap:* caste-coded Indian surnames in LLM resume shortlisting, finding dominant-caste favouritism. *Did not do:* open-weight models, religion, region, Hindi, loan or scholarship, paired P(Yes) with controls, or explanations. (Details only partly verified.)
4. **Tamkin et al. 2023.** *Overlap:* templated yes/no high-stakes decisions with demographic variation, read via the probability of "yes"; it covers loans and other allocation decisions. *Did not do:* Indian markers, name-coded identity, open-weight models, other languages, or explanations.
5. **Matton et al. 2025, "Walk the Talk?" (ICLR 2025).** *Overlap:* counterfactual test of whether explanations disclose a socially biased factor. *Did not do:* Indian context, real allocation decisions with name swaps, or self-prediction.

Also relevant: Tan et al. 2026 (EMNLP), a non-Western hiring audit where rationale prompting amplified bias; Phutane et al. 2026 (ABLEIST), India hiring with caste but measuring generated-text harms; Naik et al. 2026, a caste counterfactual in matchmaking.

**Bottom line on the gap (as of 2026-10-30):** I found no paper that combines (a) Indian caste-, religion- and region-coded names in (b) yes/no allocation decisions with logit P(Yes), in (c) English and Hindi, with (d) explanation mention-rate and (e) self-prediction. Components (a) and (b) exist separately (Rao 2025; Zaveri & Shah 2025). Components (b) and (d) together exist for Western markers (Arcuschin 2026). The self-prediction probe of counterfactual bias (RQ3, second half) and Hindi-versus-English decision bias (RQ2) appear untested. A quick search found only general introspection work (e.g., Binder et al. 2024, "Looking Inward", arXiv 2410.13787 — seen in search results only, not opened, so it is not included here).

## Could not verify
- Thorat & Attewell 2007 (EPW). No primary record opened; excluded from .bib.
- Banerjee et al. 2009: specific findings (abstract not available in the record).
- Zaveri & Shah 2025: the PDF was blocked (403), so the methods and the 16% figure are unverified.
- Bowen et al. 2025: first author's full first name; whether the paper has since been published in a journal.
- Seshadri et al. 2025, Salinas et al. 2024, Gao et al. 2026, Veldanda 2026, Naik et al. 2026: no venue beyond arXiv found.
