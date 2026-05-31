# Choosing an Estimator

`pysib` provides several estimators because different model structures and noise assumptions lead to different identification problems.

This page gives practical starting points. The best choice still depends on the data, input excitation, noise level, and model order.

## Quick recommendations

| Goal | Start with | Notes |
|:---|:---|:---|
| Fast baseline model | `pysib.arx` | Closed-form least-squares estimate. Good first check. |
| ARX with independent repeated experiment | `pysib.iv` | Uses a second output as instrument to reduce noise bias. |
| ARX with correlation criterion | `pysib.correlation` | Minimizes error/instrument correlations over selected lags. |
| Output Error model without nonlinear optimization | `pysib.sm` | Stieglitz-McBride iteration for OE structure. |
| Deterministic input/output dynamics | `pysib.oe` | Prediction-error estimate of an OE model. |
| Shared process/noise dynamics with moving-average noise | `pysib.armax` | Prediction-error estimate of an ARMAX model. |
| Separate process and noise dynamics | `pysib.bj` | Most flexible polynomial structure in the package. |
| Difficult nonlinear convergence | filtered variants | Try `oe_filtered`, `armax_filtered`, or `bj_filtered`. |

## Start simple

For most data sets, start with ARX:

```python
theta, model = pysib.arx(u, y, na=1, nb=1, nz=1)
```

ARX is fast and usually provides a useful baseline. It also helps check whether the input/output data, delay, and model orders are reasonable before using nonlinear estimators.

## When to use Output Error

Use an Output Error model when the main objective is the deterministic transfer from input to output:

```python
theta, model = pysib.oe(u, y, nb=1, nf=1, nz=1)
```

The OE structure models the process dynamics with `B/F` and treats the remaining error as additive output error. `pysib.sm` can be used as a non-C alternative for the same structure, while `pysib.oe` uses the C/LAPACK nonlinear optimizer.

## When to use ARMAX

Use ARMAX when the noise dynamics are important and can reasonably share the `A` polynomial with the deterministic dynamics:

```python
theta, model = pysib.armax(u, y, na=1, nb=1, nc=1, nz=1)
```

ARMAX estimates `A`, `B`, and `C`, giving a more detailed noise model than ARX while keeping a coupled process/noise denominator.

## When to use Box-Jenkins

Use Box-Jenkins when the process dynamics and noise dynamics should be modeled separately:

```python
theta, model = pysib.bj(u, y, nb=1, nc=1, nd=1, nf=1, nz=1)
```

Box-Jenkins estimates `B/F` for the deterministic path and `C/D` for the noise path. It is more flexible, but also has more parameters and a harder nonlinear optimization problem.

## Instrumental-variable and correlation estimators

`pysib.iv` and `pysib.correlation` estimate ARX-structure models using alternative criteria.

Use `iv` when you have two output records from repeated experiments with the same input and independent noise:

```python
theta, model = pysib.iv(u, y1, y2, na=1, nb=1, nz=1)
```

Use `correlation` when you want to estimate ARX parameters by minimizing correlations between prediction error and an instrument:

```python
theta, model = pysib.correlation(u, y, na=1, nb=1, nz=1, M=20)
```

If no external instrument is provided, `correlation` uses the input `u` as the instrument.

## Filtered variants

The filtered estimators apply a continuation strategy before the final nonlinear optimization:

```python
theta, model = pysib.oe_filtered(u, y, nb=1, nf=1, nz=1)
```

Filtered variants can help with convergence on difficult data sets, especially when the direct nonlinear estimate is sensitive to initialization.

Available filtered variants are:

- `pysib.oe_filtered`
- `pysib.armax_filtered`
- `pysib.bj_filtered`

## Practical workflow

1. Estimate a simple ARX model.
2. Check the delay `nz` and model orders.
3. Try OE if the deterministic input/output dynamics are the main target.
4. Try ARMAX or Box-Jenkins if noise modeling is important.
5. Try filtered variants if nonlinear convergence is poor.
6. Compare one-step predictions with `predict` and noise-free simulations with `simulate`.
