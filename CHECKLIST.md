# Submission checklist

**Submission files:** `submission/` (zipped as `submission.zip`, ready for Overleaf):
`main.tex` (IEEEtran conference, 10 pages), `refs.bib`, `figures/`, `main.pdf`.
Rebuild with `scripts/package_submission.sh` after any edit to `paper/main.tex`.

## Done
- [x] Name lists reviewed by the authors (automated Outkast/Naampy check: 15 of 88 flagged;
      results reported with and without them).
- [x] Hindi translations reviewed by the authors.
- [x] Every number in `paper/main.tex` traced to `results/key_numbers.md` / `results/*.csv`
      (`% src:` comments in the repo copy).
- [x] Every citation checked against `paper/refs.bib` and `lit/notes.md`.
- [x] Authors, affiliations and code URL filled in. No placeholders left in the PDF.
- [x] Release terms: code public on GitHub; benchmark prompts and raw outputs on request.
- [x] Formatting: IEEEtran conference, two-column, 10 pages (limit 6-11), XeLaTeX/tectonic.

## Judge validation (human labels)
The 200-item labelling sheet (`annotation/labelling_sheet.csv`) has not been filled in, so the
paper states that the mention judge was **not** validated against human labels and relies on the
keyword check and the explicit-label positive control instead. If you label the sheet later,
run the kappa computation and add the number to the Measurement paragraph.

## Before you press submit
- [ ] Make the GitHub repository public (the paper links to it).
- [ ] Check the venue's policy on AI-assisted writing and tools, and add a disclosure if required.
- [ ] Confirm the venue's page limit and template once more.
- [ ] On Overleaf set the compiler to XeLaTeX; if "Kohinoor Devanagari" is missing there, use
      "Noto Sans Devanagari" in the preamble.
