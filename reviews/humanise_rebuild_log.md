# Humanise rebuild log (paper/main.tex)
Built from humanised prose inside main_prehumanise.tex structure; tables/figures/appendix/preamble unchanged.

Factual fixes:
1. Author-year citations (Intro, Related Work, raw keys such as arcuschin2025chain; chen2025reasoning) converted to \cite{key} using prehumanise keys; IEEE numeric phrasing.
2. Bertrand & Mullainathan: US correspondence study (not India). Banerjee et al. 2009: hiring/labour-market call-backs in Delhi (not credit); Siddique 2011: caste discrimination in hiring; kumar2019caste restored for credit.
3. "Armstrong and Marks (2024)" removed; armstrong2024silicon cited by key only; "Zaveri et al." -> "Zaveri and Shah" (only cited by key).
4. Counterfactual fairness: edits to demographic (protected) attributes, not "non-demographic"; Seshadri non-demographic-edit sentence restored.
5. Self-prediction prompt now verbatim from configs/templates.json (selfpred N, en).
6. RQ1: "Plus 4 more" -> "The other six" (six listed cells).
7. RQ3b: similar/slightly-higher statement attached to identity predicted-change rate vs control-swap predicted-change rate (Qwen3-8B 14.5% both; Granite 13.4% vs 8.1%); actual flip rates 0.8-2.7% stated separately.
8. RQ2: "weak equivalence" because +-2 pp bound is as large as the largest RQ1 effect.
9. "Boostrap" typo fixed.
10. Karvonen & Marks: reports race/gender bias not visible in CoT (humanised version misdescribed).
11. Abstract trimmed to ~215 words; all required facts kept. Telegraphic fragments joined into sentences throughout Methods/Results/Discussion/Ethics/Conclusion.
12. % src comments, \TODO{kappa}, \TODO{release URL}, author TODOs retained.
