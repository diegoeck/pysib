# Prediction and Simulation

After estimating a model, `pysib` provides two common ways to use it:

- `predict` computes a one-step-ahead prediction using the measured output.
- `simulate` computes the noise-free response to the input signal.

Both functions accept the `model` dictionary returned by any estimator.

## One-step-ahead prediction

Use `predict` when you want to compare the measured output with the model's one-step-ahead prediction:

```python
theta, model = pysib.arx(u, y, na=1, nb=1, nz=1)
yp = pysib.predict(u, y, model)
```

The prediction uses both the input signal `u` and the measured output signal `y`.

Conceptually, `predict` evaluates:

```text
yp(t) = y(t) + H(z)^(-1) (G(z) u(t) - y(t))
```

where `G(z)` is the input/output model and `H(z)` is the noise model implied by the polynomial structure.

Use one-step-ahead prediction to inspect how well the model predicts the next output sample given the measured history.

## Noise-free simulation

Use `simulate` when you want the deterministic response of the model to an input signal:

```python
theta, model = pysib.oe(u, y, nb=1, nf=1, nz=1)
ys = pysib.simulate(u, model)
```

The simulation uses only the input signal `u` and the estimated model. It does not use the measured output `y`.

Conceptually, `simulate` evaluates:

```text
ys(t) = G(z) u(t)
```

Use simulation to inspect the deterministic input/output dynamics estimated by the model.

## Comparing prediction and simulation

Prediction and simulation answer different questions.

| Function | Uses measured `y`? | Main purpose |
|:---|:---:|:---|
| `pysib.predict(u, y, model)` | yes | One-step-ahead prediction performance |
| `pysib.simulate(u, model)` | no | Noise-free input/output response |

For noisy data, prediction can look better than simulation because it uses the measured output history. Simulation is often stricter when evaluating the deterministic model.

## Plotting results

You can compare measured and modeled outputs with Matplotlib:

```python
import matplotlib.pyplot as plt

plt.plot(y, label="measured")
plt.plot(yp, label="predicted")
plt.plot(ys, label="simulated")
plt.legend()
plt.show()
```

For Monte-Carlo parameter plots, see `pysib.plota` in the API Reference.

## Model compatibility

Both `predict` and `simulate` depend on the shared model convention used by all estimators:

```python
model["A"]
model["B"]
model["C"]
model["D"]
model["F"]
```

This means the same prediction and simulation functions can be used with ARX, OE, ARMAX, Box-Jenkins, and filtered models.
