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
