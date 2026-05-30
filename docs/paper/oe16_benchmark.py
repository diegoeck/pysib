import contextlib
import io

import numpy as np
from scipy.signal import lfilter

import pysib


N = 1000
M = 100
NB = 8
NF = 8
NZ = 0
NOISE_STD = 0.01
SUCCESS_THRESHOLD = 1e-1

B_TRUE = np.array([
    -0.2073,
    0.1815,
    1.352,
    -3.356,
    3.061,
    -1.045,
    -0.07957,
    0.0944,
])

F_TRUE = np.array([
    -6.549,
    19.2,
    -32.83,
    35.77,
    -25.39,
    11.45,
    -3.0,
    0.3491,
])

THETA_TRUE = np.concatenate((B_TRUE, F_TRUE))
MODEL_TRUE = {
    "A": np.array([1.0]),
    "B": B_TRUE,
    "C": np.array([1.0]),
    "D": np.array([1.0]),
    "F": np.concatenate(([1.0], F_TRUE)),
}


def _identify_silent(method, u, y):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        theta, model = method(u, y, NB, NF, NZ)
    return theta, model


def _metrics(theta, model, u, y_clean):
    param_error = np.linalg.norm(theta - THETA_TRUE) / np.linalg.norm(THETA_TRUE)
    y_sim = pysib.simulate(u, model)
    sim_rmse = np.sqrt(np.mean((y_sim - y_clean) ** 2))
    return param_error, sim_rmse


def _summary(values):
    values = np.asarray(values)
    return np.median(values), np.percentile(values, 90)


def main():
    rng = np.random.RandomState(42)
    results = {
        "OE": {"param_error": [], "sim_rmse": []},
        "OE filtered": {"param_error": [], "sim_rmse": []},
    }

    for _ in range(M):
        u = rng.randn(N)
        y_clean = lfilter(MODEL_TRUE["B"], MODEL_TRUE["F"], u)
        y = y_clean + NOISE_STD * rng.randn(N)

        theta_oe, model_oe = _identify_silent(pysib.oe, u, y)
        theta_filtered, model_filtered = _identify_silent(pysib.oe_filtered, u, y)

        for name, theta, model in (
            ("OE", theta_oe, model_oe),
            ("OE filtered", theta_filtered, model_filtered),
        ):
            param_error, sim_rmse = _metrics(theta, model, u, y_clean)
            results[name]["param_error"].append(param_error)
            results[name]["sim_rmse"].append(sim_rmse)

    print("method        median_param_error   p90_param_error   median_sim_rmse   success_rate")
    for name in ("OE", "OE filtered"):
        param = np.asarray(results[name]["param_error"])
        rmse = np.asarray(results[name]["sim_rmse"])
        median_param, p90_param = _summary(param)
        median_rmse, _ = _summary(rmse)
        success_rate = np.mean(param < SUCCESS_THRESHOLD)
        print(
            f"{name:<13} "
            f"{median_param:18.6e} "
            f"{p90_param:17.6e} "
            f"{median_rmse:17.6e} "
            f"{success_rate:12.2%}"
        )


if __name__ == "__main__":
    main()
