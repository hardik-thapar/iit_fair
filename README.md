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
