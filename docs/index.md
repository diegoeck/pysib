# pysib — System Identification Toolbox

**Slow is Better.** A Python toolbox for parameter identification of discrete-time SISO dynamic systems using classical polynomial input–output model structures.

## Install

```bash
pip install pysib
```

Requires Python ≥ 3.9, NumPy, SciPy, and LAPACK (Accelerate on macOS, `liblapack` on Linux).

## Quick Start

```python
import numpy as np
import pysib
from scipy.signal import lfilter

u = np.sin(np.arange(1000) * 2 * np.pi / 100)
y = lfilter([0, 1], [1, -0.9], u) + 0.01 * np.random.randn(1000)

# ARX — closed form, no optimisation
theta, model = pysib.arx(u, y, na=1, nb=1, nz=1)

# Output Error — C/LAPACK nonlinear optimiser
theta, model = pysib.oe(u, y, nb=1, nf=1, nz=1)

# Predictions and simulations
yp = pysib.predict(u, y, model)
ys = pysib.simulate(u, model)
```

## Implemented Estimators

| Model Structure | Estimator | Type |
|:---|:---|:---|
| ARX | `pysib.arx` | Least squares (NumPy) |
| ARX | `pysib.iv` | Instrumental variables (NumPy) |
| ARX | `pysib.correlation` | Correlation error minimisation (NumPy) |
| OE | `pysib.sm` | Stieglitz–McBride (NumPy) |
| OE | `pysib.oe` | Prediction-error method (C/LAPACK) |
| ARMAX | `pysib.armax` | Prediction-error method (C/LAPACK) |
| Box–Jenkins | `pysib.bj` | Prediction-error method (C/LAPACK) |
| OE | `pysib.oe_filtered` | Filtered continuation (C/LAPACK) |
| ARMAX | `pysib.armax_filtered` | Filtered continuation (C/LAPACK) |
| Box–Jenkins | `pysib.bj_filtered` | Filtered continuation (C/LAPACK) |

All estimators return `(theta, model)` where `model` is a dictionary with keys `A`, `B`, `C`, `D`, `F`.

## About

pysib is open-source (MIT) and developed at Universidade Federal do Rio Grande do Sul, Brazil.

[:fontawesome-brands-github: GitHub](https://github.com/diegoeck/pysib) · [:material-book-open-variant: Paper (ACM TOMS)]() · [:material-school: User Manual](manual/main.pdf)
