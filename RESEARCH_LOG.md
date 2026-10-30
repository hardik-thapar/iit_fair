# Research log

## 2026-10-30 - Setup

**Done**
- Read the proposal (renamed to `PROPOSAL.md`). Scope: 3 scenarios x 50 base profiles,
  4 attributes + controls, English and Hindi, 2 templates, three passes (decision,
  explanation, self-prediction), RQ1-RQ4.
- Created repo layout, task list, GPU budget log.
- Checked the GPU server: SSH as root works, one MI300X VF (gfx942), 235 GB RAM,
  ~600 GB free disk. Existing `rocm` container has PyTorch 2.14 / ROCm 10.1 but no vLLM.
  Started `docker pull rocm/vllm:latest` (download only, no GPU time).
- No Hugging Face token on the server. Open models (e.g. Qwen) are fine; gated ones
  (Llama, Gemma) need a token from the team.

**Decided**
- Run inference inside the official `rocm/vllm` container rather than building vLLM
  from source, to save setup time and keep versions pinned to an image digest.
- GPU minutes are logged only for jobs that hold the GPU (model load + inference),
  not for downloads.

**Next**
- Phase 1 literature review.

## 2026-10-30 - Hugging Face access

- Team provided an HF token; stored on the server only at `/root/fairaudit/.env`
  (mode 600, never committed). Token is valid (fine-grained).
- Gated repos (Llama 3.x, Gemma 2/3) return 403: either licences not yet accepted on
  the account, or the fine-grained token lacks "read access to public gated repos".
  Open repos (Qwen) work. Waiting on the team to fix before model selection in Phase 3.

## 2026-10-30 - Model sourcing decision

**Checked**
- Llama/Gemma licence requests submitted by the team; approval may take days.
- Third-party mirrors (unsloth/*) of Llama 3.1 8B, 3.2 3B, 3.3 70B and Gemma 2 9B have
  weight files whose SHA-256 hashes match the official repos exactly. However, the
  tokenizer/config files are not guaranteed identical and the uploader is not the
  model's creator.

**Decided (team instruction)**
- Use only models downloaded from the creating organisation's own official repo.
  No third-party mirrors.
- Official repos reachable now (no gating): Qwen (Alibaba), Mistral AI, Microsoft Phi,
  IBM Granite, AI2 OLMo, Sarvam AI (Indic). Not reachable: ai4bharat/Airavata,
  CohereLabs/aya-expanse (gated).
- Plan: the three-size family for RQ4 will be Qwen (official, ungated, offers many
  sizes). Llama/Gemma are added later only if approval arrives before the Phase 4
  pilot; the design does not depend on them. Exact model versions are picked in
  Phase 3 ("latest stable at start of experiments").

## 2026-10-30 - Phase 1 literature review done

**Done**
- Three Lit Reviewer passes (decision audits + counterfactual fairness; India + Hindi bias;
  faithfulness + LLM-as-judge). Merged into `lit/notes.md` (57 papers) and
  `paper/refs.bib` (57 entries). Every title machine-checked against arXiv / Crossref /
  ACL Anthology / publisher page (`lit/ref_check.csv`); 56 ok, 1 partial (zaveri2025caste:
  exists per OpenAlex, PDF blocked on recheck).
- Read the closest paper (arcuschin2026biases, "Biases in the Blind Spot", ICML 2026)
  myself: abstract, intro, method; keyword-searched the rest. Confirmed it has no caste,
  India, Hindi, self-prediction or logprob P(Yes).
- Wrote `lit/gap_analysis.md`.

**Decided**
- Exact study not done by anyone we found -> no stop. But the proposal's claim "no study
  measures decision bias and explanation faithfulness together" is false for Western
  markers (arcuschin2026biases, matton2025walk). Novelty restated as Indian name-coded
  markers + Hindi + self-prediction + scale. RQs unchanged; framing change goes to the
  humans at checkpoint (a).
- Borrow: McNemar + verbalisation rate on discordant pairs (arcuschin2026biases),
  CCT (siegel2024probabilities), Yes/No probability (tamkin2023evaluating), kappa-based
  judge validation.
- Add a manipulation check (can the model infer the attribute from the name?) because
  rao2025invisible's null result could mean "fair" or "did not notice".

**Infra**
- vLLM image ready: `rocm/vllm@sha256:e0ea9a10b729...` (vLLM 0.29.1.dev0, torch 2.13
  ROCm 10.1, transformers 5.18); GPU visible inside the container. No GPU job run yet.

**Next**
- Reviewer 2 on Phase 1; Methodologist drafts `design/spec.md` (running in parallel).

## 2026-10-30 - Phase 2 spec, reviews, and the first full GPU run

**Spec and reviews**
- Methodologist wrote `design/spec.md`, `design/name_pools.csv` (11 cells x 8 names),
  `design/templates_en.md`. Reviewer 2 reviewed it (`reviews/phase2_spec_review.md`, 8 major
  issues). Lead decisions on all 8 were sent back; the v2 rewrite was interrupted by a usage
  limit and is NOT finished. The run below uses spec v1 plus these v2 changes that were
  already decided: reason-first explanations, manipulation check with "Indian?" and SES items,
  self-prediction conditions N and A.
- Lit Reviewer added 9 references from the phase 1 review (65 verified entries now) and
  corrected christian2026self, banerjee2009labor, siegel2024probabilities, arcuschin2026biases.

**Human checkpoints (a) and (b) were waived by the team** (instruction in chat, 2026-10-30:
"set up tasks for gpu ... so that work starts on the gpu" while the team was away). So:
- Name lists are the Methodologist's unvalidated v1 draft (32 rows flagged
  `[NEEDS HUMAN CHECK]`; Outkast/Naampy/Pranaam not yet run).
- Hindi templates were machine-translated by the lead (`configs/templates.json`), unvalidated.
- Names and hometowns stay in Latin script inside Hindi prompts (no transliteration yet).
- Because every output is cached by prompt hash, correcting a name or a translation later only
  re-runs the affected prompts.

**Models** (official repos only; exact revisions in `configs/models.json`)
- Qwen3 4B/8B/14B/32B (RQ4 family; thinking disabled), Granite 3.3 8B, OLMo 3 7B,
  Ministral 8B (2410), Sarvam-M 24B (Indic). Judge: Mistral-Small-24B-Instruct-2501.
- Ministral-3-8B-2512 and Mistral-Small-3.2 failed to load: this vLLM image's transformers lacks
  `PixtralRotaryEmbedding`. Replaced with Mistral's text-only official models.

**Run 1** (`configs/queue_full.txt`, 60.4 GPU-min incl. smoke tests and pilot, all exit 0)
- 6,600 decision prompts, 2,112 manipulation prompts, 12,000 self-prediction prompts and
  ~2,100 explanations per model; judge over all explanations.
- Health check (`src/pilot_check.py`): English decisions clean (Yes+No mass >= 0.9 on all,
  argmax vs generated text 98.7-100%). Problems, all in Hindi prompts: Granite (50% of
  decisions) and Sarvam-M (36%) put mass on "हाँ" split into byte pieces, so first-token mass
  misses it; Hindi explanations hit the 256-token cap (Qwen3-8B 637, Qwen3-32B 560, Granite 977).
- Fix (run 2, `src/rescore.py`): score full answer strings Yes/No/हाँ/हां/नहीं (with and
  without a leading space) via prompt logprobs for all decision and self-prediction prompts in
  both languages (spec §6.3 fallback, now the primary readout for consistency), and regenerate
  truncated explanations with max_tokens=768. Then judge the new explanations.

**Early look (not analysis; no CIs yet):** flip rates of identity swaps are close to the
same-group control rates for most models (about 0.3-4.5%); mean ΔP(Yes) is within about
±0.02 everywhere. Borderline reference P(Yes) varies by model (0.37-0.77).
