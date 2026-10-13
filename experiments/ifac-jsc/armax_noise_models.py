"""Local minima of the ARMAX criterion for different noise models (Reviewer 1, Comment 1).

For each noise polynomial C and disturbance variance, M = 100 records are
generated as in revision_cases.py (third-order plant, multisine input,
disturbance C/A e). A reference minimizer is obtained by a Levenberg-Marquardt
search of the ARMAX prediction-error criterion started at the true parameters;
an estimator is counted as trapped in a worse local minimum when its final cost
exceeds the reference cost (relative tolerance 1e-6).

The last block repeats the analysis on the data of the ARMAX case of
revision_cases.py, including the filtered estimator.
"""
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares
from scipy.signal import lfilter

import comparators as C
import revision_cases as R

ROOT = Path(__file__).parent
M = 100


def prediction_errors(A, B, Cn, u, y):
    return lfilter(A, Cn, y) - lfilter(B, Cn, u)


def reference(Cp, u, y):
    """ARMAX PEM minimizer found from the true parameters."""
    nc = len(Cp) - 1

    def resid(th):
        e = prediction_errors(np.r_[1, th[:3]], np.r_[0, th[3]], np.r_[1, th[4:4 + nc]], u, y)
        return e if np.all(np.isfinite(e)) else np.full_like(y, 1e10)
    th0 = np.r_[R.F3[1:], 1.0, np.asarray(Cp[1:], float)]
    th = least_squares(resid, th0, method="lm", xtol=1e-12, ftol=1e-12).x
    m = C._model(A=np.r_[1, th[:3]], B=np.r_[0, th[3]], C=np.r_[1, th[4:]])
    return m, np.mean(resid(th) ** 2)


def cost(m, u, y):
    e = prediction_errors(m["A"], m["B"], m["C"], u, y)
    return np.mean(e ** 2) if np.all(np.isfinite(e)) else np.inf


def study(Cp, var, seed, names):
    orders = dict(na=3, nb=1, nc=len(Cp) - 1, nz=1)
    meth = {k: v for k, v in C.methods("ARMAX", orders).items() if k in names}
    rng = np.random.default_rng(seed)
    u = R.MULTISINE
    y0 = lfilter(R.B3, R.F3, u)
    success = {k: 0 for k in ["reference"] + names}
    trapped = {k: 0 for k in names}
    snr = []
    for _ in range(M):
        v = R.colored(Cp, R.F3, rng, var=var)
        y = y0 + v
        snr.append(10 * np.log10(np.var(y0) / np.var(v)))
        mref, vref = reference(Cp, u, y)
        success["reference"] += C.simulation_error(mref, u, y0) < C.THRESHOLD
        for k, f in meth.items():
            m = f(u, y)
            success[k] += C.simulation_error(m, u, y0) < C.THRESHOLD
            trapped[k] += cost(m, u, y) > vref * (1 + 1e-6)
    return np.mean(snr), success, trapped


def main():
    warnings.filterwarnings("ignore")
    names = ["pysib", "pysid"]
    lines = ["# Local minima of the ARMAX criterion\n",
             "Success: relative simulation error below 5% (out of 100). Trapped: final cost",
             "above that of the reference minimizer found from the true parameters.\n",
             "| C roots | variance | SNR [dB] | reference success | pysib success / trapped | pysid success / trapped |",
             "|---|---|---|---|---|---|"]
    configs = [([-0.5], 900), ([-0.5], 10000), ([-0.9], 900), ([-0.9], 10000),
               ([0.9], 900), ([0.9], 10000), ([0.9 * np.exp(0.476j), 0.9 * np.exp(-0.476j)], 900),
               ([0.9 * np.exp(0.476j), 0.9 * np.exp(-0.476j)], 10000),
               ([0.9, -0.9], 900), ([-0.9, -0.8], 900), ([0.5, -0.5], 900), ([0.3, 0.2], 900),
               ([0.9, 0.8], 900), ([0.95, 0.7], 900)]
    for roots, var in configs:
        Cp = np.real(np.poly(roots))
        snr, s, t = study(Cp, var, 3, names)
        label = ", ".join(f"{z:.2f}" if abs(np.imag(z)) < 1e-12 else f"{z.real:.2f}{z.imag:+.2f}j"
                          for z in roots)
        lines.append(f"| {label} | {var} | {snr:.1f} | {s['reference']} | {s['pysib']} / {t['pysib']} "
                     f"| {s['pysid']} / {t['pysid']} |")
        print(lines[-1], file=sys.stderr, flush=True)

    # ARMAX case of revision_cases.py: same data (seed), filtered estimator included
    names = ["pysib", "pysib filtered", "pysid"]
    snr, s, t = study(np.poly([0.9, 0.8]), R.NOISE_VAR, list(R.CASES).index("armax"), names)
    lines += ["\n## ARMAX case of revision_cases.py\n",
              f"SNR {snr:.1f} dB, reference success {s['reference']}",
              "| method | success | trapped |", "|---|---|---|"]
    lines += [f"| {k} | {s[k]} | {t[k]} |" for k in names]
    (ROOT / "armax_noise_models_results.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
