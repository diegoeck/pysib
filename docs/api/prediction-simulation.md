# Prediction and Simulation

This page summarizes the functions used after a model has been estimated.

Both functions accept the `model` dictionary returned by any `pysib` estimator.

## `pysib.predict`

```python
yp = pysib.predict(u, y, model)
```

Computes the one-step-ahead predicted output.

Conceptually:

```text
yp(t) = y(t) + H(z)^(-1) (G(z) u(t) - y(t))
```

Parameters:

- `u`: input signal.
- `y`: measured output signal.
- `model`: model dictionary with keys `A`, `B`, `C`, `D`, and `F`.

Returns:

- `yp`: predicted output array.

Use `predict` to evaluate one-step-ahead prediction performance using the measured output history.

## `pysib.simulate`

```python
ys = pysib.simulate(u, model)
```

Computes the noise-free simulated output.

Conceptually:

```text
ys(t) = G(z) u(t)
```

Parameters:

- `u`: input signal.
- `model`: model dictionary with keys `A`, `B`, `C`, `D`, and `F`.

Returns:

- `ys`: simulated output array.

Use `simulate` to evaluate the deterministic input/output response of an estimated model.

## Example

```python
theta, model = pysib.arx(u, y, na=1, nb=1, nz=1)

yp = pysib.predict(u, y, model)
ys = pysib.simulate(u, model)
```

`predict` uses `y`; `simulate` does not.
