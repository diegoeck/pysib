# AGENTS.md

## Repo Shape
- Python package `pysib` (pip-installable) at `src/pysib/`.
- `src/pysib/_c/` contains C extensions compiled via `setuptools.Extension` — one `.so` per algorithm (OE, ARMAX, BJ).
- `tests/test_basic.py` covers all public functions with pytest.

## Build & Install
- `pip install -e .` from the repo root compiles C extensions and installs the package.
- macOS links `-framework Accelerate`; Linux links `-llapack`. The `lapack.h` wrapper handles `ptrdiff_t` → `int` cast for `dposv`.
- Numpy headers are pulled via `numpy.get_include()` in `setup.py`.

## Focused Verification
- Run tests: `python3 -m pytest tests/ -v`
- Quick smoke: `python3 -c "import pysib; import numpy as np; u=np.sin(np.arange(80)/5); y=u+0.01*np.random.randn(80); pysib.oe(u,y,1,1,0); print('OK')"`

## Architecture
- `arx.py`, `sm.py` → pure NumPy/SciPy (no C).
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
