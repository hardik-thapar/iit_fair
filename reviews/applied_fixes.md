# Applied fixes to paper/main.tex (from verify_A-D)

Abstract / intro (A)
- Self-prediction "uninformative" -> "cannot be distinguished from chance near the threshold; over all pairs two models exceed chance but margin predicts far better" (abstract, intro, RQ3b heading/text, discussion, conclusion).
- "caste not decoded nor acted on" -> English-only, no Holm-significant primary shift, one model differs from its control; "non-perception" softened to "best read as / most plausible".
- "strongly" -> "up to 9.7 pp"; abstract: signal definition (name; region name+hometown), "0 of 576 explained flips, judged by an LLM", "15% (OBC) and 26% (SC)", "every model-attribute mean".
- Karvonen citation corrected; caste/religion-from-surnames claim split from citation; "Closest to our work"; "To our knowledge" for related-work novelty; rao/zaveri "closed models"; Christian & Mazor and Lanham wording; title "Move" -> "Nudge". "Findings in brief" paragraph removed (duplicated abstract; space).

Methods (B)
- Added: token caps, no-system-message wording, English-only Decision parser and unparsed->No, attribute-specific keyword detector, multiple-choice manipulation check with option counts and order, positive-control profile bootstrap (5,000, no correction), p-value definition, pooled binomial + clustered bootstrap across scenarios, drop-one-name scope, flagged-name exclusion rule, AUROC CI details, language test Holm.
- Fixed: self-prediction mass threshold wording, FC counts (no English item), Ministral in run-time readout note, agreement definition, name-position alignment scope, South/NE caste coding "intended", 33 names with unrun checks, Hindi translation scope, 9 failed launches, 25% sample covers all variants, reason-first rationale sentence removed.
- Kappa: sentence now says human validation has not been done; \TODO{kappa} kept.

Results (C)
- OBC excess "driven mainly" -> "partly" (raw +0.54 pp); "0% in every condition" -> "every name-coded condition"; "no information" -> "never mention ... cannot be used to detect"; RQ3b null scoped to near-threshold; Christian claim made English-specific; Qwen3-8B forced-choice caveat; option-split "broadly similar" with largest gap; Sarvam-M Sikh added to lost cells; South "no consistent direction" with Qwen3-32B exception; control swaps "similar to or slightly above"; "bands small" -> "few flips"; Fig. 1 caption clarified.

End / format (D)
- Granite: "every explanation" -> 118 of 1,350 mention the background line (computed from raw explicit_explain.jsonl, src comment added); "decoded only" claim -> "neither necessary nor sufficient" (Sikh, South/Qwen3-32B); keyword agreement and missing-explanation counts made exact; human-input statement revised (LLM-assisted drafting); "scholarship and loan" -> removed; App. B thresholds and Zaveri/Shah check added; SC CI added; limitations: comparability of positive control and single judge; conclusion "several models (Qwen3 family)".

Not applied / notes
- Optional items skipped: subsection renames, extra-results appendix, keyword-list shortening, Table 2 Sarvam-M .04/.05 rounding (needs 4-dp check), "sign test p=0.07" in abstract kept only in text.
- Page budget: paper was 11 pages; to reach 10, figures narrowed (0.5 textwidth), refs set at 6.5pt, appendices \scriptsize, several sentences tightened (noise-floor merged, related work and discussion shortened). PDF has 10 pages (mdls may report a stale 11).
