# Basic Concepts

This page introduces the conventions used throughout `pysib`.

## Signals

Most functions work with two measured signals:

- `u`: input signal.
- `y`: output signal.

Signals are converted internally to one-dimensional NumPy arrays.

## Estimated models

All estimators return two values:

```python
theta, model = pysib.arx(u, y, na=1, nb=1, nz=1)
```

The `theta` array contains the estimated parameters. The `model` dictionary contains the polynomial representation used by `predict` and `simulate`.

Every model dictionary has the same keys:

```python
model["A"]
model["B"]
model["C"]
model["D"]
model["F"]
```

Each value is a one-dimensional NumPy array of polynomial coefficients.

## Model structures

`pysib` implements classical polynomial input/output model structures.

### ARX

```text
       B(z)            1
y(t) = ---- u(t-nz) + ---- e(t)
       A(z)           A(z)
```

### Output Error

```text
       B(z)
y(t) = ---- u(t-nz) + e(t)
       F(z)
```

### ARMAX

```text
       B(z)           C(z)
y(t) = ---- u(t-nz) + ---- e(t)
       A(z)           A(z)
```

### Box-Jenkins

```text
       B(z)           C(z)
y(t) = ---- u(t-nz) + ---- e(t)
       F(z)           D(z)
```

## Order parameters

Estimator arguments specify how many parameters are estimated in each polynomial:

- `na`: number of estimated `A` parameters.
- `nb`: number of estimated `B` parameters.
- `nc`: number of estimated `C` parameters.
- `nd`: number of estimated `D` parameters.
- `nf`: number of estimated `F` parameters.
- `nz`: input delay in samples.

For example, `na=2` estimates two parameters after the leading `1` in `A(z)`.

## Input delay convention

The returned `model["B"]` array includes `nz` leading zeros before the estimated `B` coefficients:

```python
model["B"] = [0, ..., 0, b1, ..., b_nb]
```

This convention lets `predict` and `simulate` use the polynomial arrays directly with `scipy.signal.lfilter`.

## Prediction and simulation

`predict` and `simulate` use the same model dictionary but answer different questions.

- `predict(u, y, model)` computes a one-step-ahead prediction using the measured output `y`.
- `simulate(u, model)` computes the noise-free model response to the input signal `u`.

Use `predict` to evaluate one-step prediction performance. Use `simulate` to inspect the deterministic input/output response of the estimated model.
