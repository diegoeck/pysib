# Quick Start

The basic `pysib` workflow is:

1. prepare an input signal `u` and an output signal `y`;
2. estimate a model from the data;
3. use the model for prediction or simulation.

## Estimate an ARX model

This example generates data from a simple discrete-time system and estimates an ARX model.

```python
import numpy as np
import pysib
from scipy.signal import lfilter

N = 1000
u = np.sin(np.arange(N) * 2 * np.pi / 100)
y = lfilter([0, 1], [1, -0.9], u) + 0.01 * np.random.randn(N)

theta, model = pysib.arx(u, y, na=1, nb=1, nz=1)

yp = pysib.predict(u, y, model)
ys = pysib.simulate(u, model)
```

The main arguments are:

- `u`: input signal.
- `y`: output signal.
- `na`: order of the `A` polynomial.
- `nb`: number of estimated `B` coefficients.
- `nz`: input delay in samples.

The estimator returns:

- `theta`: estimated parameter vector.
- `model`: dictionary with polynomial arrays `A`, `B`, `C`, `D`, and `F`.

The `predict` function computes a one-step-ahead prediction. The `simulate` function computes the noise-free model response to the input signal.

## Try a nonlinear estimator

The same data can also be used with an Output Error model:

```python
theta, model = pysib.oe(u, y, nb=1, nf=1, nz=1)
```

The `oe`, `armax`, `bj`, and filtered estimators use the C/LAPACK nonlinear optimizer.

## Next steps

The following sections of this documentation will describe model structures, estimator selection, and the full API reference.
