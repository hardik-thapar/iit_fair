# Literature notes: India-centric and multilingual (Hindi) bias

Compiled 2026-10-30 by the Lit Reviewer. Every entry below was opened at the stated source. Venue and DOI metadata were cross-checked against ACL Anthology, arXiv comments or OpenAlex records. Fields that could not be confirmed are marked `[UNVERIFIED]`.

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

### rao2025invisible — Invisible Filters: Cultural Bias in Hiring Evaluations Using Large Language Models (Rao et al., 2025, AIES 2025)
URL: https://arxiv.org/abs/2508.16673 (DOI 10.1609/aies.v8i3.36703)   Verified: yes (opened arXiv; AIES DOI via OpenAlex)
Summary: LLMs scored 100 UK and 100 Indian interview transcripts. Indian transcripts scored lower even after anonymisation, and the gap tracks linguistic features. Controlled name swaps for gender, caste and region inside the Indian transcripts produced no significant score differences.
Relevance: This is very close prior work: an Indian hiring evaluation with caste and region name swaps. Its null result on names is important for us to engage with, and it supports our within-pair P(Yes) measure, control noise floor and borderline profiles. It does not test Hindi, loans or scholarships, and it does not examine explanations or self-prediction.

### zaveri2025caste — Caste And Occupational Identity In Large Language Models (Zaveri & Shah, 2025, IIMB Working Paper No. 724)
URL: https://www.iimb.ac.in/sites/default/files/2025-08/WP%20No.%20724.pdf   Verified: yes (opened full PDF from IIMB)
Summary: Five studies on ChatGPT (GPT-3.5 and GPT-4). (1) SC and ST surnames make up under 4% of LLM-generated occupational names, against more than 30% of the workforce. (2) Prompts that ask for diversity create caste–occupation association bias. (3) In a resume-shortlisting test with equal numbers of OTHERS, SC and ST surnames on 12 resumes for an engineering job, GPT-3.5 shortlisted OTHERS 84% of the time. Few-shot examples of past hires reduce this bias.
Relevance: This is the closest prior hiring audit using caste-coded surnames, and it found a strong effect, in contrast to Rao et al. It uses a list-ranking design, not paired single decisions, closed models only, English only, and hiring only. It does not examine explanations or self-prediction. Its surname list (Appendix Table A14: 150 surnames, more than 80% caste probability under SECC via Outkast) is directly reusable.

### naik2026sima — Sima AIunty: Caste Audit in LLM-Driven Matchmaking (Naik et al., 2026, arXiv preprint)
URL: https://arxiv.org/abs/2603.29288   Verified: yes (opened arXiv)
Summary: A controlled audit of real matrimonial profiles that varies caste (Brahmin, Kshatriya, Vaishya, Shudra, Dalit) and income across five model families, including BharatGPT. Same-caste matches are rated up to 25% higher than inter-caste matches, and inter-caste ratings follow the traditional hierarchy.
Relevance: It is a counterfactual caste audit of an LLM evaluation that includes an Indic model. The domain is matchmaking rather than allocation, it is English only, and it does not check explanations.

### nair2026rupeebias — RupeeBias: Auditing Demographic Bias in Indian Economic Guidance from Large Language Models (Nair et al., 2026, arXiv preprint)
URL: https://arxiv.org/abs/2609.31245   Verified: yes (opened arXiv abstract + HTML full text)
Summary: 39,150 single-attribute counterfactual prompts covering salary estimation, increments, counter-offers and service pricing, with 87 India-specific identifiers across caste, religion, region, gender, disability and urban/rural. Prompts are in English and Hinglish, and nine LLMs are tested, including Sarvam-105B. Outputs differ by 20.2% on average when only the identifier changes.
Relevance: This is the closest in design: a single-attribute counterfactual on Indian axes, with an Indian language variant and an Indic model. However, identity is given as an explicit self-label, not through names or surnames (the authors list this as a limitation). The outputs are numeric guidance, not accept/reject decisions. It uses Hinglish, not Devanagari Hindi, and does not analyse explanations.

### mahajan2026ifaab — The Indian Financial Automated Advice Bias (IFAAB) Dataset: Auditing Socioeconomic and Demographic Disparities in LLM-Generated Financial Advice in India (Mahajan, 2026, arXiv preprint)
URL: https://arxiv.org/abs/2610.38239   Verified: yes (opened arXiv; submitted 2026-10-28)
Summary: A counterfactual audit of 31,734 GPT-4o financial-advice responses for synthetic Indian personas that vary gender, caste, education, district and other traits. Male-labelled and General-category profiles receive higher projected resources than female and OBC, SC or ST profiles, and the advice content is gendered.
Relevance: A very recent India finance audit. It uses one closed model and free-text advice, not loan approval. How identity is signalled (names or labels) and what language is used are `[UNVERIFIED]`. It does not test explanation faithfulness.

### phutane2025ableist — ABLEIST: Intersectional Disability Bias in LLM-Generated Hiring Scenarios (Phutane et al., 2025, arXiv preprint; to appear at AIES 2026)
URL: https://arxiv.org/abs/2510.10998   Verified: yes (opened arXiv; venue from comments "To appear at AIES 2026")
Summary: An audit of six LLMs on 2,820 hiring scenarios that vary disability, gender, nationality and caste (Brahmin and Dalit) in an Indian recruitment setting. Eight metrics are grounded in disability studies. Harms are amplified for disabled candidates who are also caste- or gender-marginalised.
Relevance: It includes caste in LLM hiring, but it measures harms in generated conversation text, not accept/reject decisions, and it is English only. Whether caste is signalled by name is `[UNVERIFIED]`.

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

## Closest prior work to our study

1. **Zaveri & Shah 2025 (IIMB WP 724)**
   - **Overlap:** an LLM resume-shortlisting audit with caste-coded surnames (OTHERS, SC, ST surnames mapped through SECC and Outkast). It finds strong dominant-caste preference (84% of shortlisted candidates).
   - **Not done:**
     - Paired single-applicant decisions and logit-based P(Yes)
     - Open-weight models (ChatGPT only)
     - Loan and scholarship scenarios
     - Religion, region and gender as separate swaps
     - Hindi
     - Explanation-mention analysis or self-prediction
     - A within-group control noise floor
   - **Status:** a working paper, not peer-reviewed.
2. **Rao et al. 2025, "Invisible Filters" (AIES 2025)**
   - **Overlap:** a counterfactual Indian hiring evaluation with gender, caste and region name swaps. It finds no significant name effect.
   - **Not done:**
     - Loan and scholarship
     - Religion as a separate axis (`[UNVERIFIED]`)
     - Hindi
     - Explanation faithfulness or self-prediction
     - Logit-level confidence
   - **Implication:** their null result means we must report effect sizes against our control noise floor and should expect small effects on non-borderline profiles.
3. **Nair et al. 2026, RupeeBias (arXiv, September 2026)**
   - **Overlap:** a single-attribute counterfactual audit on Indian axes (caste, religion, region, gender) across nine LLMs, including Sarvam, with English and Hinglish variants.
   - **Not done:**
     - Names or surnames as signals (they use explicit labels)
     - Accept/reject decisions (their outputs are salaries and prices)
     - Devanagari Hindi
     - Explanation or self-prediction analysis
   - **Implication:** this is the biggest threat to a "first Indian counterfactual audit" claim. Our novelty must rest on implicit name signals, binary allocation decisions, Hindi, and explanation faithfulness.
4. **Nawale et al. 2025, FairI Tales / INDIC-BIAS (ACL 2025)**
   - **Overlap:** a "judgment" task over Indian identities across 14 LLMs. It notes that asking models to rationalise does not reduce bias.
   - **Not done:**
     - Paired applications with name swaps
     - High-stakes allocation scenarios
     - A Hindi versus English comparison
     - Testing whether explanations disclose the bias
5. **Mahajan 2026, IFAAB (arXiv, 28 October 2026)**
   - **Overlap:** a counterfactual audit of GPT-4o financial advice for Indian personas, varying caste and gender.
   - **Not done:**
     - Loan approval decisions
     - Open-weight models
     - Hindi (`[UNVERIFIED]`)
     - Explanation faithfulness

**Novelty assessment:** I found no paper that combines (a) paired accept/reject decisions with (b) Indian name and surname signals, (c) an English versus Devanagari Hindi comparison, and (d) checks of explanation mention and self-prediction. Components (a)+(b) exist for hiring only (Zaveri & Shah; Rao et al., with conflicting results). Part of (c) exists in RupeeBias (Hinglish, explicit labels) and BharatBBQ (QA). I found no India-specific work on (d). Searches covered caste hiring, Indian-name resume screening, LLM loan approval in India, Hindi versus English decisions, caste-surname counterfactuals, and scholarship or admissions. The searches were thorough but not exhaustive, so the paper should say "to our knowledge".

## Name and surname list sources

- **Zaveri & Shah 2025, Appendix Table A14:** 150 surnames, 50 per group (OTHERS, SC, ST), each mapping to one group with more than 80% probability in SECC data. Study 5 also uses 270 surnames (90 per group) and 90 first names (45 male, 45 female). Source PDF: https://www.iimb.ac.in/sites/default/files/2025-08/WP%20No.%20724.pdf. Note that the categories are SC, ST and "OTHERS", with no OBC split, so OBC-coded surnames need another source.
- **Outkast (appeler/outkast):** https://github.com/appeler/outkast. A deterministic lookup of surname by state and birth year against an extract of SECC 2011. It returns SC, ST and Other counts and proportions, and cells with fewer than 100 records are withheld. MIT licence. Cited by Zaveri & Shah as "Laohaprapanon & Sood 2020". It is useful for validating that our surnames are strongly SC- or dominant-coded, though not OBC.
- **Pranaam (appeler/pranaam):** https://github.com/appeler/pranaam. Scores how Muslim-associated a name is, in English or Hindi script, trained on Bihar land records. MIT licence. Useful for checking that our Muslim and Hindu name variants are unambiguous. It does not separate Sikh or Christian names.
- **Naampy (appeler/naampy):** https://github.com/appeler/naampy. Gives the female share of a first name from Indian electoral rolls. MIT licence. Useful for checking that our male and female first names are unambiguous.
- **DECASTE (Vijayaraghavan et al. 2025):** surnames from the Wikipedia category of Indian surnames. Caste and varna were extracted by an LLM, checked manually, and cross-checked against official central OBC and SC/ST lists. First names came from public GitHub gists. The paper describes the method but does not clearly release the list, so `[UNVERIFIED]` whether it is available. The cross-check against government OBC lists is the best published recipe for OBC-coded surnames.
- **INDIC-BIAS identity groups (Nawale et al. 2025):** https://github.com/AI4Bharat/indic-bias. 85 vetted identity-group terms (caste, religion, region, tribe). These are group labels rather than personal names, but they are useful for hometowns and regions and for checking coverage.
- **Prior surname-to-caste practice:** Zaveri & Shah cite Shah (2024), "Caste Inequality in Medical Crowdfunding in India", *Journal of Development Studies* 60(11), DOI 10.1080/00220388.2024.2383438, as precedent for inferring caste from surnames. I did not open it, so it is `[UNVERIFIED]` and is not in the bib.
