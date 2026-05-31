# Examples

The repository includes runnable Python examples under the `examples/` directory.

Each example generates data, estimates a model, and usually compares measured data with prediction and simulation results.

## Basic estimators

| Example | Description |
|:---|:---|
| [`example_arx.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_arx.py) | ARX estimation and prediction/simulation. |
| [`example_sm.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_sm.py) | Stieglitz-McBride estimation for an Output Error model. |
| [`example_oe.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_oe.py) | Output Error estimation with comparison to Stieglitz-McBride. |
| [`example_armax.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_armax.py) | ARMAX estimation. |
| [`example_bj.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_bj.py) | Box-Jenkins estimation. |

## Alternative ARX estimators

| Example | Description |
|:---|:---|
| [`example_iv.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_iv.py) | Instrumental-variable estimation using repeated experiments. |
| [`example_correlation.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_correlation.py) | Correlation-based ARX estimation. |

## Filtered estimators

| Example | Description |
|:---|:---|
| [`example_oe_filtered.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_oe_filtered.py) | Filtered continuation for OE. |
| [`example_armax_filtered.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_armax_filtered.py) | Filtered continuation for ARMAX. |
| [`example_bj_filtered.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_bj_filtered.py) | Filtered continuation for Box-Jenkins. |

## Monte-Carlo examples

| Example | Description |
|:---|:---|
| [`example_monte_carlo.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_monte_carlo.py) | Repeated OE estimation and parameter-spread plot. |
| [`example_monte_carlo_filtered_simple.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_monte_carlo_filtered_simple.py) | Simple Monte-Carlo experiment with filtered estimation. |
| [`example_monte_carlo_filtered_motor.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_monte_carlo_filtered_motor.py) | Filtered Monte-Carlo experiment using motor data. |
| [`example_monte_carlo_filtered_plot.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_monte_carlo_filtered_plot.py) | Plotting saved filtered Monte-Carlo results. |
| [`example_monte_carlo_filtered_motor_plot.py`](https://github.com/diegoeck/pysib/blob/main/examples/example_monte_carlo_filtered_motor_plot.py) | Plotting saved motor Monte-Carlo results. |

## Running examples

From a local checkout, install the package in editable mode:

```bash
pip install -e .
```

Then run an example with Python:

```bash
python examples/example_arx.py
```

Most examples use Matplotlib and open a plot window.
