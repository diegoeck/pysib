# Estimators

This page summarizes the estimator functions exposed by `pysib`.

All estimators return:

```python
theta, model = estimator(...)
```

where `theta` is the estimated parameter vector and `model` is a dictionary with polynomial arrays `A`, `B`, `C`, `D`, and `F`.

## ARX estimators

### `pysib.arx`

```python
theta, model = pysib.arx(u, y, na, nb, nz)
```

Least-squares estimator for the ARX structure.

Parameters:

- `u`: input signal.
- `y`: output signal.
- `na`: number of estimated `A` parameters.
- `nb`: number of estimated `B` parameters.
- `nz`: input delay.

Returns `theta = [a1, ..., a_na, b1, ..., b_nb]`.

### `pysib.iv`

```python
theta, model = pysib.iv(u, y1, y2, na, nb, nz)
```

Instrumental-variable estimator for the ARX structure using two repeated experiments.

Parameters:

- `u`: input signal, shared by both experiments.
- `y1`: output signal from the first experiment.
- `y2`: output signal from the second experiment.
- `na`: number of estimated `A` parameters.
- `nb`: number of estimated `B` parameters.
- `nz`: input delay.

Returns `theta = [a1, ..., a_na, b1, ..., b_nb]`.

### `pysib.correlation`

```python
theta, model = pysib.correlation(u, y, na, nb, nz, M=20, z=None)
```

ARX estimator based on correlation error minimization.

Parameters:

- `u`: input signal.
- `y`: output signal.
- `na`: number of estimated `A` parameters.
- `nb`: number of estimated `B` parameters.
- `nz`: input delay.
- `M`: number of correlation lags.
- `z`: optional external instrument. If omitted, `u` is used.

Returns `theta = [a1, ..., a_na, b1, ..., b_nb]`.

## Output Error estimators

### `pysib.sm`

```python
theta, model = pysib.sm(u, y, nb, nf, nz)
```

Stieglitz-McBride estimator for the Output Error structure.

Parameters:

- `u`: input signal.
- `y`: output signal.
- `nb`: number of estimated `B` parameters.
- `nf`: number of estimated `F` parameters.
- `nz`: input delay.

Returns `theta = [b1, ..., b_nb, f1, ..., f_nf]`.

### `pysib.oe`

```python
theta, model = pysib.oe(u, y, nb, nf, nz)
```

Prediction-error estimator for the Output Error structure using the C/LAPACK nonlinear optimizer.

Parameters:

- `u`: input signal.
- `y`: output signal.
- `nb`: number of estimated `B` parameters.
- `nf`: number of estimated `F` parameters.
- `nz`: input delay.

Returns `theta = [b1, ..., b_nb, f1, ..., f_nf]`.

### `pysib.oe_filtered`

```python
theta, model = pysib.oe_filtered(u, y, nb, nf, nz)
```

Filtered continuation variant of the Output Error estimator.

Parameters and return layout are the same as `pysib.oe`.

## ARMAX estimators

### `pysib.armax`

```python
theta, model = pysib.armax(u, y, na, nb, nc, nz)
```

Prediction-error estimator for the ARMAX structure using the C/LAPACK nonlinear optimizer.

Parameters:

- `u`: input signal.
- `y`: output signal.
- `na`: number of estimated `A` parameters.
- `nb`: number of estimated `B` parameters.
- `nc`: number of estimated `C` parameters.
- `nz`: input delay.

Returns `theta = [a1, ..., a_na, b1, ..., b_nb, c1, ..., c_nc]`.

### `pysib.armax_filtered`

```python
theta, model = pysib.armax_filtered(u, y, na, nb, nc, nz)
```

Filtered continuation variant of the ARMAX estimator.

Parameters and return layout are the same as `pysib.armax`.

## Box-Jenkins estimators

### `pysib.bj`

```python
theta, model = pysib.bj(u, y, nb, nc, nd, nf, nz)
```

Prediction-error estimator for the Box-Jenkins structure using the C/LAPACK nonlinear optimizer.

Parameters:

- `u`: input signal.
- `y`: output signal.
- `nb`: number of estimated `B` parameters.
- `nc`: number of estimated `C` parameters.
- `nd`: number of estimated `D` parameters.
- `nf`: number of estimated `F` parameters.
- `nz`: input delay.

Returns `theta = [b1, ..., b_nb, c1, ..., c_nc, d1, ..., d_nd, f1, ..., f_nf]`.

### `pysib.bj_filtered`

```python
theta, model = pysib.bj_filtered(u, y, nb, nc, nd, nf, nz)
```

Filtered continuation variant of the Box-Jenkins estimator.

Parameters and return layout are the same as `pysib.bj`.
