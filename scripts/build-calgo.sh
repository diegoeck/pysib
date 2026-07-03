#!/usr/bin/env bash
# Assemble the ACM TOMS / CALGO software component for pysib.
#
# Copies files from the repository into release-artifacts/calgo/ and produces
# pysib-calgo.zip with the layout required by the TOMS Algorithms guidelines:
#
#   userManual.pdf
#   userManual/     LaTeX sources able to regenerate userManual.pdf
#   Python/         package sources (verbatim), tests, examples, drivers
#   Doc/            README, LICENSE, CITATION
#
# The package sources are copied into a staging directory; generated caches and
# compiled artifacts are stripped there.  Nothing in the repository is modified
# by this script.
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
find "$STAGE/Python/examples" -name "*.pdf" -delete
find "$STAGE/Python/examples" -name "*.npz" -delete
find "$STAGE/Python/examples" -name "*_results.md" -delete

# Drivers replicating all results in the manuscript, with expected outputs.
mkdir -p "$STAGE/Python/drivers/expected_output"
cp "$EXP/robustness_noisy_data.py" \
   "$EXP/robustness_noisy_data_plot.py" \
   "$EXP/filtered_continuation_oe.py" \
   "$EXP/filtered_continuation_oe_plot.py" \
   "$EXP/filtered_continuation_bj.py" \
   "$EXP/filtered_continuation_bj_plot.py" \
   "$STAGE/Python/drivers/"
cp "$EXP/robustness_noisy_data.npz" \
   "$EXP/filtered_continuation_oe.npz" \
   "$EXP/filtered_continuation_bj.npz" \
   "$STAGE/Python/drivers/"
cp "$EXP/robustness_noisy_data_results.md" \
   "$EXP/filtered_continuation_oe_results.md" \
   "$EXP/filtered_continuation_bj_results.md" \
   "$STAGE/Python/drivers/expected_output/"

cat > "$STAGE/Python/drivers/README.md" <<'EOF'
# Drivers for the numerical results of the manuscript

These drivers replicate all numerical results presented in the article.
They require no interactive input.

1. Install the package (builds the C extensions):

       pip install ..

2. To regenerate the Monte Carlo data from scratch (Sections 5.1--5.3),
   run:

       python robustness_noisy_data.py
       python filtered_continuation_oe.py
       python filtered_continuation_bj.py

   This step can take some time.  The artifact also includes the `.npz`
   data files used for the manuscript, so the next step can be run
   immediately.

3. Generate the statistics tables and the figures of the article:

       python robustness_noisy_data_plot.py
       python filtered_continuation_oe_plot.py
       python filtered_continuation_bj_plot.py

Each plot script writes a `*_results.md` file with the statistics reported
in the article and one or more `*.pdf` figures.
Compare the generated `*_results.md` files with the reference copies in
`expected_output/`.  All drivers use a fixed pseudo-random seed, so the
outputs are reproducible bit-for-bit on the same NumPy version.
EOF

# --- Doc/ -----------------------------------------------------------------
mkdir -p "$STAGE/Doc"
cp "$ROOT/LICENSE" "$STAGE/Doc/"
cp "$ROOT/CITATION.cff" "$STAGE/Doc/"
cat > "$STAGE/Doc/README.md" <<'EOF'
# pysib CALGO software artifact

This archive accompanies the ACM TOMS Algorithm manuscript for `pysib`.

Top-level contents:

- `userManual.pdf`: user manual for the package.
- `userManual/`: LaTeX source used to build the user manual.
- `Python/`: installable Python package, tests, examples, and article drivers.
- `Doc/`: license, citation metadata, and this overview.

To build and test the package, enter `Python/` and install it:

    pip install .
    python -m pytest tests/ -v

The article experiments are in `Python/drivers/`.  That directory contains
the scripts, the `.npz` data files used by the manuscript, expected Markdown
outputs, and a README with exact reproduction instructions.

Regular usage examples are in `Python/examples/`.
EOF

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
