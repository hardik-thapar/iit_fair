# Do LLMs Tell the Truth About Their Bias?

Paired counterfactual audit of open-weight LLMs on Indian high-stakes decisions
(job shortlisting, loan approval, scholarship award), in English and Hindi.
See `PROPOSAL.md` for scope.

## Layout

| Path | What |
| --- | --- |
| `PROPOSAL.md` | Research proposal (source of truth for scope) |
| `RESEARCH_LOG.md` | Dated log of what was done and decided |
| `TASKS.md` | Current task list |
| `IDEAS.md` | Out-of-scope ideas parked for later |
| `lit/` | Literature notes and gap analysis |
| `design/` | Experiment spec |
| `src/`, `tests/`, `configs/` | Pipeline code, tests, run configs |
| `data/` | Generated benchmark (name lists, templates, prompts) |
| `results/` | Metric summaries; `results/raw/` holds model outputs |
| `logs/gpu_budget.csv` | Every GPU job and its minutes |
| `annotation/` | Human labelling sheets |
| `paper/` | LaTeX draft and `refs.bib` |

## Compute

One AMD MI300X (192 GB) with vLLM on ROCm. Total budget 5 GPU-hours, target ≤ 4.

## Reproducing

```bash
python -m venv .venv && .venv/bin/pip install numpy pandas scipy matplotlib
.venv/bin/python -m src.make_benchmark        # builds data/benchmark/ (byte-identical, seeded)
# on a ROCm/CUDA box with Docker and the pinned vLLM image (see scripts/gpu_queue.sh):
scripts/gpu_queue.sh configs/queue_full.txt     # decision, manipulation, self-prediction, explanation passes
scripts/gpu_queue.sh configs/queue_rescore.txt  # full-candidate scoring + long explanations + judge
scripts/gpu_queue.sh configs/queue_explicit.txt # explicit-label positive control + judge
.venv/bin/python -m src.analysis && .venv/bin/python -m src.analysis_extra && .venv/bin/python -m src.analysis_explicit
.venv/bin/python -m src.key_numbers             # results/key_numbers.md: every number in the paper with its source
cd paper && tectonic -X compile main.tex
```

Models and exact revisions: `configs/models.json`. GPU log: `logs/gpu_budget.csv` (131.6 GPU-minutes total).
Raw model outputs (`results/raw/`) are not in this repository.

## Usage statement

This repository studies how language models treat *name-coded* identity signals (gender, religion,
caste-coded surnames, region) in synthetic Indian application scenarios. Names and surnames are used
only as signals; nothing here is a claim about any group or individual. The name lists are drafts
that had not been fully validated at run time (see `design/name_validation_v1.csv`). Please do not use
these materials to build systems that infer caste or religion from names, or to rank, screen or
profile real people. Report aggregate results only.
