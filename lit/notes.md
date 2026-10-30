# Literature notes

57 papers, merged from three Lit Reviewer passes (2026-10-30), plus 8 added after Reviewer 2 (Part D; 65 in refs.bib). Each entry was opened at
its source by a reviewer; titles were then machine-checked against arXiv / Crossref /
ACL Anthology / OpenAlex (`lit/ref_check.csv`, script `lit/verify_refs.py`).
Per-area originals: `lit/notes_decisions.md`, `lit/notes_india.md`, `lit/notes_faithfulness.md`.
Synthesis and closest prior work: `lit/gap_analysis.md`.

# Part A - LLM decision audits and counterfactual fairness

## Area 1a — Classic correspondence (field) audits

### bertrand2004emily — Are Emily and Greg More Employable Than Lakisha and Jamal? A Field Experiment on Labor Market Discrimination (Bertrand & Mullainathan, 2004, American Economic Review 94(4):991–1013)
URL: https://doi.org/10.1257/0002828042002561   Verified: yes (opened Crossref record)
Summary: The authors sent fictitious resumes to job ads in Boston and Chicago and randomly assigned African-American- or White-sounding names. White names received about 50% more callbacks. Callbacks also responded more to resume quality for White names.
Relevance: This is the template for our paired name-swap design: identical profile, only the name changes. We transfer it to LLM deciders and Indian markers, and we measure a continuous P(Yes) shift as well as a binary "callback".

### banerjee2009labor — Labor market discrimination in Delhi: Evidence from a field experiment (Banerjee, Bertrand, Datta & Mullainathan, 2009, Journal of Comparative Economics 37(1):14–27)
URL: https://doi.org/10.1016/j.jce.2008.09.002   Verified: yes (opened Crossref and OpenAlex records; online 2008, issue dated March 2009)
Summary: A correspondence study that sent 3,160 fictitious resumes to 371 software and call-centre job openings in and around Delhi, randomly allocating caste-linked surnames (upper caste vs SC, ST and OBC; plus Muslim names). It found no evidence of discrimination against non-upper-caste applicants for software jobs, but large and significant callback gaps between upper castes and OBCs (and, to a lesser extent, SCs) for call-centre jobs. It found no discrimination against Muslims in either job type, and the authors conclude that overall caste identity does not significantly affect callbacks. (Findings now confirmed from the abstract in the OpenAlex record for DOI 10.1016/j.jce.2008.09.002, opened 2026-10-30 after Reviewer 2; full text not read, so do not quote numbers beyond the abstract.)
Relevance: This is the closest human-audit precedent for caste-coded names in Indian hiring. Note that for *software* jobs, which match our fresher-SWE scenario, the human baseline is a **null**; the caste gap appeared only for call-centre jobs. Use it to justify caste/religion surname markers, and frame it honestly: an LLM caste gap in the SWE scenario would *not* simply be "reproducing" this human pattern.

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
URL: https://arxiv.org/abs/2602.10117   Verified: yes (opened arXiv abstract page, which says "Accepted at ICML 2026", and the HTML). Venue re-checked after Reviewer 2: page 1 of the v5 PDF reads "Proceedings of the 43rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026"; bib entry now cites it as ICML 2026, PMLR vol. 306.
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


# Part B - India-centric and multilingual / Hindi bias

## Area 1: India-centric bias in NLP and LLMs (caste, religion, region, gender)

### bhatt2022recontextualizing — Re-contextualizing Fairness in NLP: The Case of India (Bhatt et al., 2022, AACL-IJCNLP 2022)
URL: https://aclanthology.org/2022.aacl-main.55/ (DOI 10.18653/v1/2022.aacl-main.55)   Verified: yes (opened ACL Anthology + arXiv 2209.12226)
Summary: A position paper with an empirical component. It describes the main axes of social disparity in India (region, caste, religion, gender and others), builds resources for Indian fairness evaluation, and shows prediction biases and region and religion stereotypes in corpora and models. It ends with a research agenda for re-contextualising fairness to India.
Relevance: This is the foundational framing citation for using Indian axes instead of US race. It works on stereotypes and pre-LLM models, with no decision tasks and no explanations.

### khandelwal2024indian — Indian-BhED: A Dataset for Measuring India-Centric Biases in Large Language Models (Khandelwal et al., 2024, GoodIT 2024)
URL: https://arxiv.org/abs/2309.08573 (DOI 10.1145/3677525.3678666)   Verified: yes (opened arXiv; venue from OpenAlex record = ACM Int. Conf. on Information Technology for Social Good, GoodIT 2024)
Summary: An English dataset of stereotypical and anti-stereotypical sentences for caste and religion in India. Most LLMs tested prefer stereotypes. GPT-2, GPT-2 Large and GPT-3.5 chose the stereotype in 63–79% of caste items and 69–72% of religion items, more than on Western axes such as gender and race.
Relevance: It motivates caste and religion as high-bias axes. It measures stereotype preference only, not allocation decisions, and covers neither Hindi nor explanations.

### sahoo2024indibias — IndiBias: A Benchmark Dataset to Measure Social Biases in Language Models for Indian Context (Sahoo et al., 2024, NAACL 2024)
URL: https://aclanthology.org/2024.naacl-long.487/ (DOI 10.18653/v1/2024.naacl-long.487)   Verified: yes (opened ACL Anthology + arXiv 2403.20147)
Summary: The authors filtered and translated CrowS-Pairs into Hindi and India-adapted English, then augmented it with LLM-generated Indian stereotypes. It has 800 sentence pairs and 300 intersectional tuples covering gender, religion, caste, age, region, appearance and occupation, in English and Hindi. Ten LMs show bias, and the bias is larger on intersectional groups.
Relevance: This is the main prior English-plus-Hindi bias resource for India, but it uses sentence-likelihood probing, not decisions. Its translation-and-adaptation pipeline is a useful template for our Hindi prompts.

### vijayaraghavan2025decaste — DECASTE: Unveiling Caste Stereotypes in Large Language Models through Multi-Dimensional Bias Analysis (Vijayaraghavan et al., 2025, IJCAI 2025)
URL: https://arxiv.org/abs/2505.14971 (DOI 10.24963/ijcai.2025/1100)   Verified: yes (opened arXiv abstract + HTML; IJCAI DOI via OpenAlex)
Summary: A framework that probes caste bias in socio-cultural, economic, educational and political dimensions. It uses implicit probing with Indian first names and caste-associated surnames (SWAT) and explicit persona prompts (PSAT). Nine models are tested, seven of them open-weight (Llama-2/3, Mixtral and others). Bias is highest for Dalit and Shudra versus dominant castes. The study is English only.
Relevance: It shows that surnames alone carry caste signal to LLMs, which supports our surname manipulation. Its surname list method is described under "Name and surname list sources" below. It has no hiring, loan or scholarship decision, no Hindi and no explanation check.

### nawale2025fairi — FairI Tales: Evaluation of Fairness in Indian Contexts with a Focus on Bias and Stereotypes (Nawale et al., 2025, ACL 2025)
URL: https://arxiv.org/abs/2506.23111 (DOI 10.18653/v1/2025.acl-long.1465)   Verified: yes (opened arXiv; ACL DOI via OpenAlex)
Summary: Introduces the INDIC-BIAS benchmark: 85 identity groups across caste, religion, region and tribe, about 1,800 expert-curated topics and 20k validated scenario templates. Its three tasks are plausibility, judgment and generation. All 14 LLMs tested show strong negative bias against marginalised identities, and asking them to rationalise their choice does not reduce it.
Relevance: Its "judgment" task is the closest benchmark-style decision setting, and the rationalisation finding links to our RQ3. Identity is given as explicit group labels inside scenarios, not as names in high-stakes applications, and it does not compare Hindi with English. Its identity list (github.com/AI4Bharat/indic-bias) is a vetted source of group terms.

### seth2025deep — How Deep Is Representational Bias in LLMs? The Cases of Caste and Religion (Seth et al., 2025, AIES 2025)
URL: https://arxiv.org/abs/2508.03712 (DOI 10.1609/aies.v8i3.36718)   Verified: yes (opened arXiv; AIES DOI via OpenAlex)
Summary: The authors had GPT-4 Turbo write more than 7,200 stories about Indian life events and compared the religion and caste make-up of the stories with census shares. Dominant groups are over-represented far beyond their population share in a "winner-take-all" pattern, and prompt nudges to diversify have limited effect.
Relevance: It is evidence of representational, not allocational, caste and religion bias. This motivates testing whether such bias reaches decisions. It uses one closed model, English, and no decisions.

### nair2026rupeebias — RupeeBias: Auditing Demographic Bias in Indian Economic Guidance from Large Language Models (Nair et al., 2026, arXiv preprint)
URL: https://arxiv.org/abs/2609.31245   Verified: yes (opened arXiv abstract + HTML full text)
Summary: 39,150 single-attribute counterfactual prompts covering salary estimation, increments, counter-offers and service pricing, with 87 India-specific identifiers across caste, religion, region, gender, disability and urban/rural. Prompts are in English and Hinglish, and nine LLMs are tested, including Sarvam-105B. Outputs differ by 20.2% on average when only the identifier changes.
Relevance: This is the closest in design: a single-attribute counterfactual on Indian axes, with an Indian language variant and an Indic model. However, identity is given as an explicit self-label, not through names or surnames (the authors list this as a limitation). The outputs are numeric guidance, not accept/reject decisions. It uses Hinglish, not Devanagari Hindi, and does not analyse explanations.

### mahajan2026ifaab — The Indian Financial Automated Advice Bias (IFAAB) Dataset: Auditing Socioeconomic and Demographic Disparities in LLM-Generated Financial Advice in India (Mahajan, 2026, arXiv preprint)
URL: https://arxiv.org/abs/2610.38239   Verified: yes (opened arXiv; submitted 2026-10-28)
Summary: A counterfactual audit of 31,734 GPT-4o financial-advice responses for synthetic Indian personas that vary gender, caste, education, district and other traits. Male-labelled and General-category profiles receive higher projected resources than female and OBC, SC or ST profiles, and the advice content is gendered.
Relevance: A very recent India finance audit. It uses one closed model and free-text advice, not loan approval. How identity is signalled (names or labels) and what language is used are `[UNVERIFIED]`. It does not test explanation faithfulness.

### gupta2026compounding — Compounding Disadvantage: Auditing Intersectional Bias in LLM-Generated Explanations Across Indian and American STEM Education (Gupta et al., 2026, arXiv preprint)
URL: https://arxiv.org/abs/2601.14506   Verified: yes (opened arXiv)
Summary: Four LLMs, including the open models Qwen2.5-32B and GPT-OSS-20B, generate STEM explanations for synthetic student profiles that vary caste, medium of instruction and college tier (India) and race and school type (US). Explanations for marginalised profiles are simplified by up to 2.55 grade levels, and effects compound non-additively.
Relevance: An Indian education audit with caste. Here "explanations" means tutoring content, not decision rationales, so it does not address our RQ3. How caste is signalled is `[UNVERIFIED]`.

## Area 2: Multilingual and Hindi bias, and Indic LLMs

### tomar2025bharatbbq — BharatBBQ: A Multilingual Bias Benchmark for Question Answering in the Indian Context (Tomar et al., 2025, TACL vol. 13)
URL: https://arxiv.org/abs/2508.07090 (DOI 10.1162/tacl.a.55)   Verified: yes (opened arXiv; TACL DOI via OpenAlex record)
Summary: A BBQ adaptation covering 13 Indian social categories, 3 of them intersectional, with 49,108 examples translated and verified into 8 languages (Hindi, English, Marathi, Bengali, Tamil, Telugu, Odia, Assamese), for 392,864 items in total. Five multilingual LM families are evaluated. Bias is often amplified in Indian languages compared with English.
Relevance: This is the key evidence for our RQ2 hypothesis that bias is higher in Hindi than in English. It is a QA benchmark, not allocation decisions, and it does not check explanations.

### hada2024akal — Akal Badi ya Bias: An Exploratory Study of Gender Bias in Hindi Language Technology (Hada et al., 2024, FAccT 2024)
URL: https://arxiv.org/abs/2405.06346 (DOI 10.1145/3630106.3659017)   Verified: yes (opened arXiv; FAccT DOI via OpenAlex)
Summary: A mixed-methods study of gender bias in Hindi. Mining biased Hindi sentences with existing methods failed, so the authors collected examples through field studies with rural and low-income women, finding diverse perceptions of bias. They also tried social media, news and translated datasets as sources.
Relevance: It shows that translated English bias resources transfer poorly to Hindi, which is a caution for our machine-translated Hindi prompts and supports our human-check step. It does not cover LLM decisions.

### vashishtha2023evaluating — On Evaluating and Mitigating Gender Biases in Multilingual Settings (Vashishtha et al., 2023, Findings of ACL 2023)
URL: https://aclanthology.org/2023.findings-acl.21/ (DOI 10.18653/v1/2023.findings-acl.21)   Verified: yes (opened ACL Anthology)
Summary: Extends the DisCo gender-bias benchmark to several Indian languages with human annotation. Adapts English debiasing methods to massively multilingual masked LMs and evaluates them with a new metric. The exact language list, including whether Hindi is covered, is `[UNVERIFIED]` because the abstract says only "different Indian languages".
Relevance: An early multilingual gender-bias measurement for Indian languages, on masked LMs. Useful background for RQ2, but there are no generative LLMs and no decisions.

### gamboa2025social — Social Bias in Multilingual Language Models: A Survey (Gamboa et al., 2025, EMNLP 2025)
URL: https://aclanthology.org/2025.emnlp-main.1416/ (DOI 10.18653/v1/2025.emnlp-main.1416)   Verified: yes (opened ACL Anthology)
Summary: A systematic review of bias evaluation and mitigation beyond English. It finds a skew toward a few languages, few multilingual mitigation studies, and recurring problems when adapting bias benchmarks across languages and cultures.
Relevance: A survey citation for RQ2 and for our method of translating benchmark prompts.

### singh2026inspect — Inspect India Evals: An Open Benchmarking Framework for Evaluating Large Language Models in the Indian Linguistic and Cultural Context (Singh et al., 2026, arXiv preprint)
URL: https://arxiv.org/abs/2607.25375   Verified: yes (opened arXiv)
Summary: An open framework built on UK AISI Inspect. It has six benchmarks, including a BharatBBQ adaptation for Indian social bias, 16-language MMLU and Indian safety tests. Five open-weight models from 8B to 32B are evaluated. Sarvam-M 24B and Gemma-2-27B tie on the composite "India Fairness Index" at 80%.
Relevance: One of the few bias evaluations that includes an Indic model (Sarvam-M), which helps us choose and justify our Indic model. The results are benchmark-style with no decision audit.

### girhepuje2023legal — Are Models Trained on Indian Legal Data Fair? (Girhepuje et al., 2023, arXiv preprint; presented at SAIL 2023)
URL: https://arxiv.org/abs/2303.07247   Verified: yes (opened arXiv; venue from comments)
Summary: Trains bail-prediction models on Hindi legal documents and measures demographic parity between Hindu- and Muslim-associated inputs. A decision-tree model shows a fairness gap of 0.237.
Relevance: An early Hindi-language decision-fairness study with Hindu and Muslim identity cues in a high-stakes Indian decision. The models are trained classifiers, not LLMs, and it does not check explanations.


# Part C - Explanation faithfulness and LLM-as-judge

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
Summary: This paper introduces the Correlational Counterfactual Test (CCT). It correlates the *size* of the shift in predicted label probabilities caused by an input edit with whether the explanation mentions the edited factor, rather than using binary flips only. Explanations from Llama-2 more often mention impactful factors, and this effect grows with model size. **Task caveat (added after Reviewer 2):** the abstract also says the association varies significantly by task, so the scale trend is not uniform across tasks.
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

### mayne2026positive — A Positive Case for Faithfulness: LLM Self-Explanations Help Predict Model Behavior (Mayne, Kang, Gould, Ramchandran, Mahdi, Siegel, 2026, ICML 2026 per arXiv comment)
URL: https://arxiv.org/abs/2602.02639   Verified: yes (opened arXiv abstract page)
Summary: The paper proposes Normalized Simulatability Gain (NSG). Across about 7k counterfactuals (health, business, ethics) and 18 models, self-explanations improve prediction of model behaviour by 11–37% NSG and beat explanations written by other models. However, 5–15% of self-explanations are highly misleading.
Relevance: A counterpoint for our discussion: self-explanations carry real information on average. Our question is whether the misleading tail concentrates in identity-driven flips.

## B. Faithfulness in fairness-critical decisions (closest to our RQ3)

### karvonen2025robustly — Robustly Improving LLM Fairness in Realistic Settings via Interpretability (Karvonen, Marks, 2025, arXiv preprint)
URL: https://arxiv.org/abs/2506.10922   Verified: yes (opened arXiv abstract page)
Summary: Anti-bias prompts work in toy settings but fail once realistic hiring context is added. Six models show up to 12% race/gender interview-rate gaps (favouring Black and female candidates), and the bias is "invisible even when inspecting the model's chain-of-thought". Affine concept editing on race/gender directions cuts the bias to <1–2.5%.
Relevance: A direct prior finding that hiring bias is not visible in CoT (US race/gender). It supports our hypothesis and shows that open models (Gemma, Mistral) are susceptible. They study mitigation, not a mention-rate metric or self-prediction.

### christian2026self — Self-Blinding and Counterfactual Self-Simulation Mitigate Biases and Sycophancy in Large Language Models (Christian, Mazor, 2026, arXiv preprint)
URL: https://arxiv.org/abs/2601.14553   Verified: yes (opened arXiv abstract page)
Summary (rewritten after Reviewer 2 from the full arXiv v1 text): Two models, **Qwen2.5-7B-Instruct (open-weight) and GPT-4.1**. The race/gender study adapts **65 Tamkin et al. (2023) yes/no decision scenarios** (loan, promotion, scholarship, etc.), with gender (2) × race (Asian, Black, Hispanic, white; 4) stated **explicitly** in a strict template (520 prompts), plus 65 "blinded" versions with race and gender removed and they/them pronouns. The outcome is the **next-token logit difference between "yes" and "no"** after a Tamkin-style prefill. Bias is the per-scenario **mean absolute difference (in logits) from the actual blinded run** (Default: 1.34 Qwen, 3.85 GPT). Interventions: "Don't discriminate" (2.48 / 4.85), "Ignore" (2.49 / 4.64), and **"If You Didn't Know"**: the prompt asks "What would your decision have been if you didn't know the gender or race of the person?", the response is prefilled with "...if I didn't know the gender or race of the person, my answer would have been “", and the resulting yes/no logit difference is compared with the true blinded run. This was the worst condition (5.46 Qwen, 9.24 GPT), and it pushed answers toward "yes". A multi-turn "Remove in context" redaction removed the significant group effects, but it still deviated from blinded runs (3.81 / 7.25). Giving models a tool to call a fresh-context copy of themselves on a redacted prompt ("self-blinding") led them to defer to the blinded answer and removed the bias. A second study does the same for sycophancy (60 dispute scenarios).
Relevance: **The closest prior work to our self-prediction probe (RQ3b), and closer than §2 previously admitted:** yes/no Tamkin-style decisions, a logit-difference metric, an open 7B model, and a counterfactual self-estimate scored against actual blinded behaviour. **What remains new for us:** (i) our probe is a *direct, per-pair verbal prediction* ("would your decision change if the name were X?") scored for *accuracy against our observed paired flip* (did the decision actually flip between the two names?). Christian & Mazor instead have the model *re-make* the decision under a counterfactual instruction and measure logit distance from the blinded run, aggregated over scenarios. They never ask the model whether its answer would change, and they never score a change/no-change prediction. (ii) Our counterfactual is a *swap* between two identities (name X vs name Y), not removal of the attribute ("blind" vs "informed"). (iii) Our signals are *implicit* Indian name markers (caste, religion, region via surnames and first names), not explicitly stated US race/gender categories. (iv) We test **English vs Devanagari Hindi**, whereas their study is English only. Consider reporting their logit-difference metric alongside ours for comparability.

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


## Name and surname list sources

- **Zaveri & Shah 2025, Appendix Table A14:** 150 surnames, 50 per group (OTHERS, SC, ST), each mapping to one group with more than 80% probability in SECC data. Study 5 also uses 270 surnames (90 per group) and 90 first names (45 male, 45 female). Source PDF: https://www.iimb.ac.in/sites/default/files/2025-08/WP%20No.%20724.pdf. Note that the categories are SC, ST and "OTHERS", with no OBC split, so OBC-coded surnames need another source.
- **Outkast (appeler/outkast):** https://github.com/appeler/outkast. A deterministic lookup of surname by state and birth year against an extract of SECC 2011. It returns SC, ST and Other counts and proportions, and cells with fewer than 100 records are withheld. MIT licence. Cited by Zaveri & Shah as "Laohaprapanon & Sood 2020". It is useful for validating that our surnames are strongly SC- or dominant-coded, though not OBC.
- **Pranaam (appeler/pranaam):** https://github.com/appeler/pranaam. Scores how Muslim-associated a name is, in English or Hindi script, trained on Bihar land records. MIT licence. Useful for checking that our Muslim and Hindu name variants are unambiguous. It does not separate Sikh or Christian names.
- **Naampy (appeler/naampy):** https://github.com/appeler/naampy. Gives the female share of a first name from Indian electoral rolls. MIT licence. Useful for checking that our male and female first names are unambiguous.
- **DECASTE (Vijayaraghavan et al. 2025):** surnames from the Wikipedia category of Indian surnames. Caste and varna were extracted by an LLM, checked manually, and cross-checked against official central OBC and SC/ST lists. First names came from public GitHub gists. The paper describes the method but does not clearly release the list, so `[UNVERIFIED]` whether it is available. The cross-check against government OBC lists is the best published recipe for OBC-coded surnames.
- **INDIC-BIAS identity groups (Nawale et al. 2025):** https://github.com/AI4Bharat/indic-bias. 85 vetted identity-group terms (caste, religion, region, tribe). These are group labels rather than personal names, but they are useful for hometowns and regions and for checking coverage.
- **Prior surname-to-caste practice:** Zaveri & Shah cite Shah (2024), "Caste Inequality in Medical Crowdfunding in India", *Journal of Development Studies* 60(11), DOI 10.1080/00220388.2024.2383438, as precedent for inferring caste from surnames. I did not open it, so it is `[UNVERIFIED]` and is not in the bib.

# Part D - Added after Reviewer 2 (phase 1)

Nine references from the "Missing references" table of `reviews/phase1_review.md`, each opened at its source on 2026-10-30. Eight are in `paper/refs.bib` (source file `lit/refs_added.bib`). Thorat & Attewell 2007 is in these notes only.

### sambasivan2021reimagining — Re-imagining Algorithmic Fairness in India and Beyond (Sambasivan, Arnesen, Hutchinson, Doshi & Prabhakaran, 2021, FAccT '21, pp. 315–328)
URL: https://arxiv.org/abs/2101.09995   DOI: 10.1145/3442188.3445896   Verified: yes (opened arXiv API record and Crossref record)
Summary: The paper argues that conventional algorithmic fairness is West-centric in its subgroups, values and methods. It draws on 36 qualitative interviews and a discourse analysis of algorithmic deployments in India. It finds that data are often unreliable for socio-economic reasons, that ML makers appear to follow double standards, and that AI evokes unquestioning aspiration. Localising model fairness alone can be "window dressing", so the authors give a roadmap for re-contextualising data and models and empowering oppressed communities.
Relevance: This is the canonical India-fairness framing for a FAccT/AIES audience. It motivates caste, religion and region as fairness axes and our choice of Indian allocation scenarios. Cite it in the introduction alongside bhatt2022recontextualizing.

### dammu2024uncultured — "They are uncultured": Unveiling Covert Harms and Social Threats in LLM Generated Conversations (Dammu, Jung, Singh, Choudhury & Mitra, 2024, EMNLP 2024, pp. 20339–20369)
URL: https://aclanthology.org/2024.emnlp-main.1134/   DOI: 10.18653/v1/2024.emnlp-main.1134   Verified: yes (opened ACL Anthology page and .bib)
Summary: The paper introduces CHAST (Covert Harms and Social Threats), seven metrics grounded in social science, and scores LLM-generated recruitment conversations with evaluation models aligned to human judgments. Seven of eight LLMs produced conversations containing covert harms, often in neutral-sounding language that existing detectors miss. Models expressed more extreme views about caste (non-Western) than about race (Western).
Relevance: This is direct prior work on caste in LLM hiring, including open models. It weakens our "first Indian-identity hiring audit" claim (Claim 1), so add it to the gap table. It differs from our study in measuring *generated conversational harm* rather than a paired yes/no allocation decision, and it does not study explanations, self-prediction or Hindi.

### gaddis2017black — How Black Are Lakisha and Jamal? Racial Perceptions from Names Used in Correspondence Audit Studies (Gaddis, 2017, Sociological Science 4:469–489)
URL: https://sociologicalscience.com/articles-v4-19-469/   DOI: 10.15195/v4.a19   Verified: yes (opened journal article page and its citation metadata; Crossref record)
Summary: A survey experiment asks respondents which race they associate with names used in audit studies, varying first names and whether last names are shown. Names more common among highly educated Black mothers (e.g. Jalen, Nia) are perceived as Black less often than names given by less-educated mothers (e.g. DaShawn, Tanisha). Audit findings are therefore likely to be sensitive to name selection, because names carry class as well as race.
Relevance: This grounds our name-signal validity concern. Indian caste and religion surnames are similarly entangled with region, language and class. It supports making the manipulation check (the model decodes caste, religion, region and gender from each name) mandatory, and conditioning RQ3 on names the model decodes correctly.

### wang2024answer — "My Answer is C": First-Token Probabilities Do Not Match Text Answers in Instruction-Tuned Language Models (Wang, Ma, Hu, Weber-Genzel, Röttger, Kreuter, Hovy & Plank, 2024, Findings of ACL 2024, pp. 7407–7416)
URL: https://aclanthology.org/2024.findings-acl.441/   arXiv: 2402.14499   DOI: 10.18653/v1/2024.findings-acl.441   Verified: yes (opened arXiv API record and ACL Anthology .bib)
Summary: The paper compares first-token log-probability evaluation of multiple-choice answers with the models' actual text output. It measures agreement on final option choice, refusal rate, choice distribution and robustness to prompt perturbation. The two are severely misaligned on all dimensions, with mismatch rates above 60%. Models heavily fine-tuned on conversational or safety data are most affected, and misalignment persists even with constrained prompts.
Relevance: This is a direct validity threat to reading P(Yes) from a single first token. It supports a pilot check of agreement between argmax P(Yes) and the greedy text answer for each model, with models below about 90% agreement flagged or dropped. (Key is distinct from wang2024large, the "not fair evaluators" paper.)

### sclar2024quantifying — Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I Learned to Start Worrying about Prompt Formatting (Sclar, Choi, Tsvetkov & Suhr, 2024, ICLR 2024)
URL: https://arxiv.org/abs/2310.11324   Verified: yes (opened arXiv API record, whose comment reads "ICLR 2024 Camera Ready version"; opened ICLR 2024 virtual poster page iclr.cc/virtual/2024/poster/18650)
Summary: Several open LLMs are extremely sensitive to meaning-preserving prompt-format changes in few-shot settings, with up to 76 accuracy points of difference for LLaMA-2-13B. The sensitivity persists with larger models, more few-shot examples and instruction tuning, and format performance correlates only weakly across models. The authors propose FormatSpread, which reports an interval of expected performance across plausible formats.
Relevance: Two templates are thin. Add format-only perturbations or a third template, and report bias as a band across formats rather than a point estimate. Note that the paper studies task accuracy rather than bias, so the transfer to bias metrics is our inference.

### selvam2023tail — The Tail Wagging the Dog: Dataset Construction Biases of Social Bias Benchmarks (Selvam, Dev, Khashabi, Khot & Chang, 2023, ACL 2023 short, pp. 1373–1386)
URL: https://aclanthology.org/2023.acl-short.118/   DOI: 10.18653/v1/2023.acl-short.118   Verified: yes (opened ACL Anthology page and .bib)
Summary: The paper asks how far social-bias benchmark scores reflect social bias rather than non-social choices made during dataset construction. It simulates alternative constructions of Winogender and BiasNLI using innocuous modifications such as paraphrasing and random sampling. These shallow changes have a surprisingly large effect on measured bias across models, and they can change model rankings.
Relevance: This supports reporting robustness across template and paraphrase variants, and treating cross-model bias rankings cautiously.

### siddique2011evidence — Evidence on Caste Based Discrimination (Siddique, 2011, Labour Economics 18(S1):S146–S159)
URL: https://ideas.repec.org/a/eee/labeco/v18y2011is1ps146-s159.html   DOI: 10.1016/j.labeco.2011.07.002   Verified: yes (opened RePEc/IDEAS page with abstract and citation_issue S1; Crossref record)
Summary: A correspondence study of caste discrimination in the Indian private sector. On average, low-caste applicants must send about 20% more resumes than high-caste applicants to get the same callback. Gaps are larger when the recruiter is male or Hindu, which suggests the gap is not purely statistical discrimination. Smaller firms favour high-caste applicants, while larger firms favour low-caste applicants.
Relevance: This is the main human caste-correspondence evidence, a positive finding that contrasts with banerjee2009labor's null for software jobs. Use it to motivate SC vs upper-caste surname pairs in the hiring scenario.

### kumar2019caste — Caste and Credit: A Woeful Tale? (Kumar & Venkatachalam, 2019, The Journal of Development Studies 55(8):1816–1833; online 2018)
URL: https://ideas.repec.org/a/taf/jdevst/v55y2019i8p1816-1833.html   DOI: 10.1080/00220388.2018.1425397   Verified: yes (opened RePEc/IDEAS page with abstract and Crossref record)
Summary: The paper studies caste-based differences in farmers' access to bank loans in rural India, analysing loan applications and approvals separately. It finds significant inter-caste differences in application rates, and evidence of discrimination against Scheduled Tribe borrowers at the approval stage. Taste-based discrimination persists after simulating unobserved credit histories, though it does not affect small farmers.
Relevance: This is human evidence of caste discrimination in *lending approval* and the grounding for our loan scenario. Note the setting is agricultural bank credit, and the clearest effect is for ST borrowers rather than SC.

### Thorat & Attewell (2007) — The Legacy of Social Exclusion: A Correspondence Study of Job Discrimination in India (Economic and Political Weekly 42(41):4141–4145)
URL: https://issuu.com/world.bank.publications/docs/9780821386897/291 (secondary: World Bank *Perspectives on Poverty in India* bibliography)   Verified: `[UNVERIFIED — NOT INCLUDED IN .bib]`
Summary: The article is reported as a correspondence study that sent resumes with Dalit, Muslim and upper-caste Hindu names to private-sector job ads. It was later reprinted as Ch. 1 of *Blocked by Caste* (Thorat & Newman eds., OUP). Rechecked on 2026-10-30: Crossref and OpenAlex searches returned no record, EPW article URLs returned 404, and JSTOR blocked automated access. The volume, issue and pages appear only in secondary bibliographies (World Bank, and Reviewer 2's search). Findings are also unverified.
Relevance: This is central human evidence (Dalit and Muslim name penalties in urban private-sector hiring). Someone with EPW or JSTOR access, or the OUP *Blocked by Caste* chapter, should confirm the details before it goes into refs.bib.
