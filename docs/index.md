# pysib — System Identification Toolbox

**System Identification Toolbox.** `pysib` is a Python toolbox for identifying discrete-time SISO dynamic systems from input/output data.

The package implements classical polynomial model structures used in system identification, with an emphasis on reliable model estimation rather than fast black-box routines.

## Slow is Better

The name **SIB** works twice: it stands for **S**ystem **I**dentification tool**B**ox, and also for **S**low **I**s **B**etter — the philosophy behind every algorithm in this package.

Just as *slow food* values careful preparation over fast food, `pysib` favours deliberate, incremental optimization over aggressive, high-risk steps. The nonlinear estimators take thousands of small, cautious steps: each iteration improves the model only slightly, and only if the fit actually gets better. It sounds slow — and it is — but the result is a level of reliability and precision that aggressive optimizers rarely achieve.

And slow does not mean inefficient. The solvers are implemented in C at a very low level, with gradients and Gauss–Newton Hessians built from hand-coded sensitivity filters. The small steps are cheap, so many iterations still run fast. You get the best of both worlds: a search strategy that prioritizes quality, on an engine that recovers performance through low-level code.

`pysib` implements classical polynomial model structures for parametric identification of discrete-time single-input single-output (SISO) dynamic systems from input/output data. The toolbox covers ARX, ARMAX, Output-Error (OE), and Box-Jenkins (BJ) structures using prediction-error minimization, together with auxiliary estimators (instrumental variables, Stieglitz–McBride, correlation) and filtered continuation schemes that reshape the cost function to escape local minima.

## Features

- Polynomial model structures: ARX, ARMAX, OE (Output-Error), BJ (Box-Jenkins)
- Prediction-error minimization with linear and nonlinear optimizers
- Auxiliary estimators: instrumental variables, correlation error minimization, Stieglitz–McBride
- Filtered continuation schemes for avoiding local minima
- One-step-ahead prediction and open-loop simulation from any estimated model
- Monte Carlo diagnostic plots (`plota`)
- Cross-platform binary wheels for macOS arm64 and Linux x86_64

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

- [Software archive](https://doi.org/10.5281/zenodo.20572074)
- [User Manual](manual/main.pdf)
- [ACM TOMS Paper](paper-toms/main.pdf)
- [IFAC SYSID Paper](paper-sysid/main.pdf)

## About

`pysib` is open-source software released under the MIT license and developed at Universidade Federal do Rio Grande do Sul, Brazil.

The toolbox is designed for users who need transparent, classical system-identification methods in Python, with documentation, examples, and companion papers describing the algorithms.

[:fontawesome-brands-github: GitHub](https://github.com/diegoeck/pysib) · [:material-school: User Manual](manual/main.pdf) · [:material-book-open-variant: TOMS Paper](paper-toms/main.pdf) · [:material-file-document: SYSID Paper](paper-sysid/main.pdf)
