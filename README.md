# pysib — System Identification Toolbox

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20572074.svg)](https://doi.org/10.5281/zenodo.20572074)

**Slow is Better.** `pysib` is a Python toolbox for identifying discrete-time SISO dynamic systems from input/output data.

The package implements classical polynomial model structures used in system identification, with an emphasis on reliable model estimation rather than fast black-box routines.

Documentation: <https://pysib.net/>

## Install

```bash
pip install pysib
```

Requirements: Python >= 3.9, NumPy, SciPy, Matplotlib, and LAPACK (Accelerate on macOS, `liblapack` on Linux).

For development from a local checkout:

```bash
pip install -e .
```

## Quick Start

```python
import numpy as np
import pysib
from scipy.signal import lfilter

N = 1000
u = np.sin(np.arange(N) * 2 * np.pi / 100)
y = lfilter([0, 1], [1, -0.9], u) + 0.01 * np.random.randn(N)

# Estimate an ARX model by least squares
theta, model = pysib.arx(u, y, na=1, nb=1, nz=1)

# Estimate an Output Error model with the nonlinear optimizer
theta, model = pysib.oe(u, y, nb=1, nf=1, nz=1)

# Use the estimated model
yp = pysib.predict(u, y, model)
ys = pysib.simulate(u, model)
```

All estimators return `(theta, model)`, where `theta` is the estimated parameter vector and `model` is a dictionary with polynomial arrays `A`, `B`, `C`, `D`, and `F`.

## Included API

- Estimators: `arx`, `iv`, `correlation`, `sm`, `oe`, `armax`, `bj`, `oe_filtered`, `armax_filtered`, `bj_filtered`.
- Model use: `predict`, `simulate`.
- Utility: `plota`.

See <https://pysib.net/> for the complete documentation.

## Publications

- Documentation site: <https://pysib.net/>
- Software archive: <https://doi.org/10.5281/zenodo.20572074>
- User Manual: <https://pysib.net/manual/main.pdf>
- ACM TOMS Paper: <https://pysib.net/paper/main.pdf>

## Test

```bash
python3 -m pytest tests/ -v
```
