# Model Structures

`pysib` estimates discrete-time polynomial input/output models for SISO systems.

The model structure determines how the input signal, output dynamics, and noise dynamics are represented. Different estimators in `pysib` target different structures.

## Polynomial convention

The polynomial arrays returned in `model` are stored in powers of the delay operator:

```text
A(z) = 1 + a1 z^-1 + ... + a_na z^-na
```

The same convention is used for `C`, `D`, and `F`. The `B` polynomial contains the input delay through leading zeros in `model["B"]`.

## ARX

The ARX structure is:

```text
       B(z)            1
y(t) = ---- u(t-nz) + ---- e(t)
       A(z)           A(z)
```

ARX uses the same polynomial `A` for the deterministic dynamics and the noise model. It is usually the simplest structure to estimate.

Available ARX estimators:

| Function | Method |
|:---|:---|
| `pysib.arx` | Least squares |
| `pysib.iv` | Instrumental variables |
| `pysib.correlation` | Correlation error minimization |

Use ARX as a simple first model or as an initial estimate for more detailed structures.

## Output Error

The Output Error structure is:

```text
       B(z)
y(t) = ---- u(t-nz) + e(t)
       F(z)
```

OE separates the deterministic input/output dynamics from the additive output error. It does not estimate a separate colored-noise model.

Available OE estimators:

| Function | Method |
|:---|:---|
| `pysib.sm` | Stieglitz-McBride iteration |
| `pysib.oe` | Prediction-error method with C/LAPACK optimizer |
| `pysib.oe_filtered` | Filtered continuation variant |

Use OE when the main goal is to estimate the deterministic transfer from input to output.

## ARMAX

The ARMAX structure is:

```text
       B(z)           C(z)
y(t) = ---- u(t-nz) + ---- e(t)
       A(z)           A(z)
```

ARMAX extends ARX with a moving-average noise polynomial `C`. The `A` polynomial still appears in both the deterministic and noise paths.

Available ARMAX estimators:

| Function | Method |
|:---|:---|
| `pysib.armax` | Prediction-error method with C/LAPACK optimizer |
| `pysib.armax_filtered` | Filtered continuation variant |

Use ARMAX when the noise dynamics matter but a shared `A` polynomial is acceptable.

## Box-Jenkins

The Box-Jenkins structure is:

```text
       B(z)           C(z)
y(t) = ---- u(t-nz) + ---- e(t)
       F(z)           D(z)
```

Box-Jenkins separates the deterministic dynamics from the noise dynamics. The deterministic path uses `B/F`, while the noise path uses `C/D`.

Available Box-Jenkins estimators:

| Function | Method |
|:---|:---|
| `pysib.bj` | Prediction-error method with C/LAPACK optimizer |
| `pysib.bj_filtered` | Filtered continuation variant |

Use Box-Jenkins when the process dynamics and noise dynamics should be modeled independently.

## Returned model polynomials

Every estimator returns a `model` dictionary with the same keys, even when a polynomial is not used by a specific structure.

| Structure | `A` | `B` | `C` | `D` | `F` |
|:---|:---|:---|:---|:---|:---|
| ARX | estimated | estimated | `[1]` | `[1]` | `[1]` |
| OE | `[1]` | estimated | `[1]` | `[1]` | estimated |
| ARMAX | estimated | estimated | estimated | `[1]` | `[1]` |
| Box-Jenkins | `[1]` | estimated | estimated | estimated | estimated |

This shared convention allows `predict` and `simulate` to work with models from all estimators.
