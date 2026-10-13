"""Iterations, computing time and success versus data length (Reviewer 2, Comments 2-3).

Nonconvex OE benchmark (third-order plant, multisine input, white noise with
sigma_v = 30) for N = 500 ... 10000, M = 20 records per length. For pysib oe
the number of iterations actually used by each optimizer phase is read from
the progress lines printed by the C core: one "G:" line per outer iteration of
the gradient phase (at most 100) and one "N:" line every 10 Gauss-Newton
iterations (at most 1000).
"""
import ctypes
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
from scipy.signal import lfilter

import comparators as C

ROOT = Path(__file__).parent
LENGTHS = [500, 1000, 2000, 5000, 10000]
M = 20
NOISE_STD = 30.0
ORDERS = dict(nb=1, nf=3, nz=1)
B3 = np.array([0.0, 1.0])
F3 = np.poly([0.9, 0.8, 0.7])

_libc = ctypes.CDLL(None)
_tmp = tempfile.NamedTemporaryFile(delete=False).name


def pysib_oe_counting(u, y):
    """Run pysib.oe; return (model, gradient outer iterations, Gauss-Newton iterations)."""
    _libc.fflush(None)  # do not count output left in the buffer by earlier calls
    fd = os.dup(1)
    out = os.open(_tmp, os.O_WRONLY | os.O_TRUNC | os.O_CREAT)
    os.dup2(out, 1)
    try:
        m = C.pysib_estimator("OE", False, ORDERS)(u, y)
    finally:
        _libc.fflush(None)
        os.dup2(fd, 1)
        os.close(out)
        os.close(fd)
    lines = open(_tmp).read().splitlines()
    return (m, sum(l.startswith("G:") for l in lines),
            10 * sum(l.startswith("N:") for l in lines))


def main():
    methods = C.methods("OE", ORDERS)
    names = list(methods)
    rng = np.random.default_rng(10)
    shape = (len(LENGTHS), len(names), M)
    err, sec = np.full(shape, np.nan), np.full(shape, np.nan)
    it_grad, it_gn = np.zeros((len(LENGTHS), M), int), np.zeros((len(LENGTHS), M), int)

    for a, n in enumerate(LENGTHS):
        t = np.arange(n)
        u = np.sin(2 * np.pi * t / 18) + np.sin(2 * np.pi * t / 28) + np.sin(2 * np.pi * t / 61)
        y0 = lfilter(B3, F3, u)
        for run in range(M):
            y = y0 + NOISE_STD * rng.normal(size=n)
            for i, name in enumerate(names):
                if name == "pysib":
                    (m, it_grad[a, run], it_gn[a, run]), sec[a, i, run] = C.timed(
                        pysib_oe_counting, u, y)
                    err[a, i, run] = C.simulation_error(m, u, y0)
                else:
                    err[a, i, run], _, _, sec[a, i, run] = C.run_method(
                        methods[name], u, y, y0, "OE")
            print(f"N={n}: run {run + 1}/{M}", file=sys.stderr, flush=True)

    np.savez(ROOT / "scaling_n.npz", lengths=LENGTHS, methods=names, err=err, seconds=sec,
             it_grad=it_grad, it_gn=it_gn, M=M, NOISE_STD=NOISE_STD)

    lines = ["# Scaling with the data length (nonconvex OE benchmark)\n",
             f"M = {M} records per length, sigma_v = {NOISE_STD}\n",
             "| N | gradient-phase outer iterations (of 100) | Gauss-Newton iterations (of 1000) |"
             + "".join(f" {k}: success / median time [s] |" for k in names),
             "|---|---|---|" + "---|" * len(names)]
    for a, n in enumerate(LENGTHS):
        row = (f"| {n} | {it_grad[a].min()}-{it_grad[a].max()} (median {int(np.median(it_grad[a]))})"
               f" | {it_gn[a].min()}-{it_gn[a].max()} (median {int(np.median(it_gn[a]))}) |")
        for i in range(len(names)):
            row += f" {100 * np.mean(err[a, i] < C.THRESHOLD):.0f}% / {np.median(sec[a, i]):.3f} |"
        lines.append(row)
    (ROOT / "scaling_n_results.md").write_text("\n".join(lines) + "\n")
    print("scaling_n_results.md written", file=sys.stderr)


if __name__ == "__main__":
    main()
