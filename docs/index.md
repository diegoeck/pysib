# pysib — System Identification Toolbox

**Slow is Better.** `pysib` is a Python toolbox for identifying discrete-time SISO dynamic systems from input/output data.

The package implements classical polynomial model structures used in system identification, with an emphasis on reliable model estimation rather than fast black-box routines.

## Install

```bash
pip install pysib
```

Requirements: Python >= 3.9, NumPy, SciPy, Matplotlib, and LAPACK (Accelerate on macOS, `liblapack` on Linux).

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

## What is included

### Estimators

| Model structure | Function | Method |
|:---|:---|:---|
| ARX | `pysib.arx` | Least squares |
| ARX | `pysib.iv` | Instrumental variables |
| ARX | `pysib.correlation` | Correlation error minimization |
| OE | `pysib.sm` | Stieglitz-McBride |
| OE | `pysib.oe` | Prediction-error method |
| ARMAX | `pysib.armax` | Prediction-error method |
| Box-Jenkins | `pysib.bj` | Prediction-error method |
| OE | `pysib.oe_filtered` | Filtered continuation |
| ARMAX | `pysib.armax_filtered` | Filtered continuation |
| Box-Jenkins | `pysib.bj_filtered` | Filtered continuation |

### Prediction, simulation, and plotting

| Function | Purpose |
|:---|:---|
| `pysib.predict` | One-step-ahead prediction from an estimated model |
| `pysib.simulate` | Noise-free simulation from an estimated model |
| `pysib.plota` | Plot Monte-Carlo parameter estimates |

## Documentation

- [Installation](installation.md): install from PyPI or from a development checkout.
- [Quick Start](quickstart.md): estimate a first model and use it for prediction and simulation.
- [Basic Concepts](basic-concepts.md): signals, polynomial conventions, delays, and returned models.
- [Model Structures](model-structures.md): ARX, OE, ARMAX, and Box-Jenkins structures.
- [Choosing an Estimator](choosing-an-estimator.md): practical guidance for selecting an estimator.
- [API Reference](api/estimators.md): estimator signatures, parameters, and return conventions.
- [Examples](examples.md): runnable examples included in the repository.

## Publications

- [User Manual](manual/main.pdf)
- [ACM TOMS Paper](paper/main.pdf)

## About

`pysib` is open-source software released under the MIT license and developed at Universidade Federal do Rio Grande do Sul, Brazil.

[:fontawesome-brands-github: GitHub](https://github.com/diegoeck/pysib) · [:material-school: User Manual](manual/main.pdf) · [:material-book-open-variant: Paper](paper/main.pdf)
