# pysib

System Identification Toolbox (Slow is Better)

## Description

Python toolbox for parameter identification of dynamic systems.
The focus is obtaining good models, not fast algorithms.

Implemented methods:

* Stieglitz-McBride
* Prediction Error Method with ARX structure
* Prediction Error Method with ARMAX structure
* Prediction Error Method with ARMAX structure — improved convergence (filtered)
* Prediction Error Method with OE structure
* Prediction Error Method with OE structure — improved convergence (filtered)
* Prediction Error Method with BJ structure
* Prediction Error Method with BJ structure — improved convergence (filtered)

## Install

```bash
pip install -e .
```

Requires: numpy, scipy. LAPACK (Accelerate on macOS, liblapack on Linux).

## Use

```python
import numpy as np
import pysib

N = 1000
u = np.sin(np.arange(N) * 2 * np.pi / 100)
G_num, G_den = [0, 1], [1, -0.9]
H_num, H_den = [1, 0], [1, -0.9]

# Generate data (simple ARX process)
from scipy.signal import lfilter
y = lfilter(G_num, G_den, u) + lfilter(H_num, H_den, np.random.randn(N))

theta, m = pysib.arx(u, y, na=1, nb=1, nz=1)
print(theta)

yp = pysib.predict(u, y, m)
ys = pysib.simulate(u, m)
```

### OE example

```python
u = np.sin(np.arange(100) * 2 * np.pi / 100)
y = lfilter([0, 1], [1, -0.9], u) + 0.01 * np.random.randn(100)

theta, m = pysib.oe(u, y, nb=1, nf=1, nz=1)
```

### API

| Function | Description |
|----------|-------------|
| `pysib.arx(u, y, na, nb, nz)` | ARX estimator (pure NumPy) |
| `pysib.sm(u, y, nb, nf, nz)` | Stieglitz-McBride |
| `pysib.oe(u, y, nb, nf, nz)` | Output Error (C optimizer) |
| `pysib.armax(u, y, na, nb, nc, nz)` | ARMAX (C optimizer) |
| `pysib.bj(u, y, nb, nc, nd, nf, nz)` | Box-Jenkins (C optimizer) |
| `pysib.oe_filtered(...)` | OE with filtered convergence |
| `pysib.armax_filtered(...)` | ARMAX with filtered convergence |
| `pysib.bj_filtered(...)` | BJ with filtered convergence |
| `pysib.predict(u, y, m)` | One-step-ahead prediction |
| `pysib.simulate(u, m)` | Noise-free simulation |

All estimators return `(theta, m)` where `m` is a dict with keys
`A, B, C, D, F` (1D numpy arrays representing polynomial coefficients).

## Test

```bash
python3 -m pytest tests/ -v
```
