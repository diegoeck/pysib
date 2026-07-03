#!/usr/bin/env bash
# Assemble the ACM TOMS / CALGO software component for pysib.
#
# Copies files from the repository into release-artifacts/calgo/ and produces
# pysib-calgo.zip with the layout required by the TOMS Algorithms guidelines:
#
#   userManual.pdf
#   userManual/     LaTeX sources able to regenerate userManual.pdf
#   Python/         package sources (verbatim), tests, examples, drivers
#   Doc/            LICENSE, CITATION
#
# The pip package sources are copied verbatim; nothing in the repository is
# modified by this script.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/release-artifacts/calgo"
STAGE="$OUT/stage"
ZIP="$OUT/pysib-calgo.zip"
# Paper sources live outside the public repository; override with PYSIB_PAPERS.
PAPERS="${PYSIB_PAPERS:-$ROOT/../pysib-papers}"
EXP="$PAPERS/paper-toms/experiments"

rm -rf "$OUT"
mkdir -p "$STAGE"

# --- userManual.pdf + userManual/ -------------------------------------------
cp "$ROOT/docs/manual/main.pdf" "$STAGE/userManual.pdf"
mkdir -p "$STAGE/userManual"
cp "$ROOT/docs/manual/main.tex" "$ROOT/docs/manual/Makefile" "$STAGE/userManual/"
cp -R "$ROOT/docs/manual/api" "$STAGE/userManual/api"

# --- Python/ ------------------------------------------------------------------
mkdir -p "$STAGE/Python"
cp "$ROOT/pyproject.toml" "$ROOT/setup.py" "$ROOT/MANIFEST.in" \
   "$ROOT/README.md" "$STAGE/Python/"
cp -R "$ROOT/src" "$STAGE/Python/src"
cp -R "$ROOT/tests" "$STAGE/Python/tests"
cp -R "$ROOT/examples" "$STAGE/Python/examples"

# Drivers replicating all results in the manuscript, with expected outputs.
mkdir -p "$STAGE/Python/drivers/expected_output"
cp "$EXP/robustness_noisy_data.py" \
   "$EXP/robustness_noisy_data_plot.py" \
   "$EXP/filtered_continuation_oe.py" \
   "$EXP/filtered_continuation_oe_plot.py" \
   "$STAGE/Python/drivers/"
cp "$EXP/robustness_noisy_data_results.md" \
   "$EXP/filtered_continuation_oe_results.md" \
   "$STAGE/Python/drivers/expected_output/"

cat > "$STAGE/Python/drivers/README.md" <<'EOF'
# Drivers for the numerical results of the manuscript

These drivers replicate all numerical results presented in the article.
They require no interactive input.

1. Install the package (builds the C extensions):

       pip install ..

2. Run the Monte Carlo simulations (Section 5.1 and Section 5.2):

       python robustness_noisy_data.py
       python filtered_continuation_oe.py

3. Generate the statistics tables and the figures of the article:

       python robustness_noisy_data_plot.py
       python filtered_continuation_oe_plot.py

Each plot script writes a `*_results.md` file with the statistics reported
in the article (Tables 5 and 6) and a `*.pdf` figure (Figures 1 and 2).
Compare the generated `*_results.md` files with the reference copies in
`expected_output/`.  All drivers use a fixed pseudo-random seed, so the
outputs are reproducible bit-for-bit on the same NumPy version.
EOF

# --- Doc/ -----------------------------------------------------------------
mkdir -p "$STAGE/Doc"
cp "$ROOT/LICENSE" "$STAGE/Doc/"
cp "$ROOT/CITATION.cff" "$STAGE/Doc/"

# --- Strip VCS metadata, caches, and compiled artifacts (CALGO checklist) ---
find "$STAGE" \( -name "__pycache__" -o -name ".git*" -o -name ".DS_Store" \
    -o -name "*.so" -o -name "*.o" -o -name "*.a" -o -name "*.pyc" \
    -o -name "*.egg-info" \
    -o -name "*.aux" -o -name "*.log" -o -name "*.out" \
    -o -name "*.bbl" -o -name "*.blg" -o -name "*.fls" \
    -o -name "*.fdb_latexmk" -o -name "*.synctex.gz" \) \
    -prune -exec rm -rf {} +

# --- Zip --------------------------------------------------------------------
(cd "$STAGE" && zip -qr "$ZIP" .)
echo "CALGO package written to: $ZIP"
echo
echo "Top-level contents:"
ls -1 "$STAGE"
echo
unzip -l "$ZIP" | tail -2
