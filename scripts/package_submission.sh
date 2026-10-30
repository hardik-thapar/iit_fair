#!/bin/bash
# Build a self-contained submission folder + zip (Overleaf-ready) from paper/main.tex.
set -e
cd "$(dirname "$0")/.."
rm -rf submission && mkdir -p submission/figures
# clean copy: local figure paths, no internal source comments
sed 's#\.\./figures/#figures/#g' paper/main.tex \
  | sed -E '/^[[:space:]]*% ?src:/d; s/[[:space:]]*% ?src:.*$//' > submission/main.tex
cp paper/refs.bib submission/
for f in $(grep -o 'figures/[A-Za-z0-9_]*\.pdf' submission/main.tex | sort -u); do cp "$f" submission/figures/; done
cat > submission/README.txt <<'TXT'
Compile with XeLaTeX (Hindi text needs a Devanagari font) or tectonic:
  tectonic -X compile main.tex
On Overleaf: Menu > Compiler > XeLaTeX. If "Kohinoor Devanagari" is not installed there,
change it in main.tex to "Noto Sans Devanagari".
Files: main.tex (IEEEtran conference), refs.bib, figures/*.pdf, main.pdf (compiled draft).
TXT
(cd submission && tectonic -X compile main.tex >/dev/null 2>&1 && rm -f main.aux main.log main.out main.bbl main.blg)
rm -f submission.zip && (cd submission && zip -qr ../submission.zip .)
echo "submission/ and submission.zip ready"; ls submission submission/figures
