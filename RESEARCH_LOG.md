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
