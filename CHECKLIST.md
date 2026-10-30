# Before submission: what the human authors must do

## Must do (the paper is not honest or complete without these)
- [ ] **Validate the name lists.** Check every name in `design/name_pools_v1_used_in_run.csv`
      against `design/name_validation_v1.csv` (Outkast/Naampy results: 15 of 88 flagged).
      Pay special attention to:
      - the SC-coded surnames below a 0.8 SC share (e.g. Sonkar 0.67);
      - the "-preet" Sikh first names, which are gender-ambiguous on their own;
      - the Christian-coded names, which no model read as Christian.
      If you change names, only the affected prompts need re-running (outputs are cached).
- [ ] **Validate the Hindi translations** in `configs/templates.json`. They were machine-translated
      and nobody has checked them. Decide whether names should be written in Devanagari in Hindi
      prompts. They are currently in Latin script.
- [ ] **Hand-label the 200 explanations** in `annotation/labelling_sheet.csv`, following
      `annotation/README.md`. Two annotators label independently. Then compute Cohen's kappa
      (judge vs human, and human vs human) and fill `\TODO{kappa}` in the paper.
- [ ] **Re-check every number in the paper** against `results/key_numbers.md`. Each number in
      `paper/main.tex` has a `% src:` comment pointing at its source.
- [ ] **Re-check every citation** you keep. Open the paper and make sure our sentence matches
      what it says. `zaveri2025caste` is only partly verified (its PDF was blocked); re-open it
      before quoting its numbers.
- [ ] **Rewrite the paper in your own voice**, especially the Introduction, Discussion and
      Conclusion. Check the venue's policy on AI-assisted writing and disclose as it requires.
- [ ] Fill in the authors, affiliations, acknowledgements and release URL.
- [ ] **Ethics:** decide the release terms (gated access plus a usage statement are proposed),
      and confirm whether your institution needs any ethics sign-off for team annotation.

## Should do (strengthens the paper; cheap)
- [ ] Read `reviews/phase6_results_review.md` and the final draft review, and decide which
      remaining objections to address and which to acknowledge.
- [ ] Optional GPU follow-ups, each under 20 GPU-min (about 190 min of budget remain); see
      `IDEAS.md`:
      - Split region into name vs hometown.
      - Score every item with the full answer words, so English and Hindi use the same readout.
      - Re-run with team-validated names in Devanagari.
- [ ] Decide whether to keep the commit trailer "Co-Authored-By: Claude". Git history
      currently includes it.

## Formatting
- [ ] Confirm the venue's page limit and template. The draft uses IEEEtran conference, two-column.
- [ ] Recompile with `cd paper && tectonic -X compile main.tex`, or with XeLaTeX on Overleaf.
      Hindi needs a Devanagari font (Kohinoor Devanagari locally; Noto Sans Devanagari on Overleaf).
- [ ] Check that the figures are readable in grayscale print.
