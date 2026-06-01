# AGENTS.md

## Repo Shape
- Python package `pysib` (pip-installable) at `src/pysib/`.
- `src/pysib/_c/` contains C extensions compiled via `setuptools.Extension` — one `.so` per algorithm (OE, ARMAX, BJ).
- `tests/test_basic.py` covers all public functions with pytest.
- ACM TOMS Algorithm article draft is in `docs/paper/` using `acmart` and BibTeX.
- Article publication support files are in `docs/paper/publication/`.
- User manual in LaTeX is in `docs/manual/`; article and manual go to `docs/` (not PyPI).

## Build & Install
- `pip install -e .` from the repo root compiles C extensions and installs the package.
- macOS links `-framework Accelerate`; Linux links `-llapack`. The `lapack.h` wrapper handles `ptrdiff_t` → `int` cast for `dposv`.
- Numpy headers are pulled via `numpy.get_include()` in `setup.py`.

## Focused Verification
- Run tests: `python3 -m pytest tests/ -v`
- Quick smoke: `python3 -c "import pysib; import numpy as np; u=np.sin(np.arange(80)/5); y=u+0.01*np.random.randn(80); pysib.oe(u,y,1,1,0); print('OK')"`
- Build site: GitHub Actions installs MkDocs and runs `python -m mkdocs build --strict`.
- Build article: `make` from `docs/paper/`.
- Build manual: `make` from `docs/manual/`.

## Documentation Strategy
- `docs/index.md` is the MkDocs landing page for `pysib.net`.
- The MkDocs site is intended to become the main user-facing documentation.
- Keep `README.md` concise and point users to the site; use PyPI metadata to link to the site when publishing.
- Do not reorganize `docs/manual/` or `docs/paper/` as part of the current site cleanup unless explicitly requested.

## Release Process
- Update the project changelog before creating a release tag.
- Update package version, documentation, and manual PDF before the final release commit when needed.
- Run focused tests/build checks before tagging.
- Create the release tag only after the final release commit.
- Publish PyPI artifacts and create the GitHub Release from the tag.
- Use the changelog entry as the basis for GitHub Release notes.

## Architecture
- `arx.py`, `sm.py`, `correlation.py`, `iv.py` → pure NumPy/SciPy (no C).
- `oe.py`, `armax.py`, `bj.py` → ARX initial guess + C optimizer via `_c._pysib_*_core.identify()`.
- `predict.py` → `predict()` and `simulate()` using `scipy.signal.lfilter`.
- `filtered.py` → frequency-sweep filtered variants calling the C optimizer at each step.
- C modules (`pysib_*_module.c`) embed `grad()` and a `py_identify()` NumPy wrapper (translated from the original `mexFunction`).
- `pysib_basic.c` and `pysib_optimize.c` are shared across extensions; `pysib_optimize.c` had `mexPrintf` → `printf` and `mexEvalString`/`utIsInterruptPending` removed.

## Model Convention (same as MATLAB)
- All estimators return `(theta, m)` where `m` is a dict with keys `A, B, C, D, F` (1D numpy arrays).
- `predict()` and `simulate()` depend on this convention.

## Editing Notes
- The C optimizer prints progress bars to stdout via `printf` — expect noisy output.
- `grad()` is defined separately in each `*_module.c` (different gradient formulas for OE/ARMAX/BJ).
- Each `*_module.c` compiles into its own `.so` to avoid symbol conflicts (duplicate global names).
