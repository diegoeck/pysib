"""Monte Carlo cases added in the revision (Reviewer 1, Comment 1).

usage: python revision_cases.py <case> [<case> ...]     (cases listed in CASES)

Each case compares pysib, pysib filtered, SIPPY and pysid (see comparators.py)
on M = 100 data records and writes revision_<case>.npz. The summary table is
produced by revision_summary.py.

Unless stated otherwise the plant is the third-order OE benchmark of the
article, the disturbance is scaled to variance 900 (the same as the white
noise of the nonconvex OE benchmark, sigma_v = 30), and a success is a
relative simulation error below 5%. In the ARMAX case the zeros of C (0.9 and
0.8) cancel two of the three poles of A, so that the disturbance reduces to
e/(1 - 0.7 q^-1) and the problem is close to an OE problem.
"""
import sys
from pathlib import Path

import numpy as np
from scipy.signal import lfilter, max_len_seq

import comparators as C

ROOT = Path(__file__).parent
M = 100
N = 1000
NOISE_VAR = 900.0

t = np.arange(N)
MULTISINE = (np.sin(2 * np.pi * t / 18)
             + np.sin(2 * np.pi * t / 28)
             + np.sin(2 * np.pi * t / 61))
B3 = np.array([0.0, 1.0])
F3 = np.poly([0.9, 0.8, 0.7])

# Eighth-order plant of pysib/examples/example_monte_carlo_filtered_motor.py: a power
# system with two synchronous generators connected to the grid (Anderson and Fouad, 1977)
B_MOTOR = np.array([0, -0.207296003971350, 0.181497963178803, 1.351706842960986,
                    -3.356365092407725, 3.060933791693723, -1.045306362058663,
                    -0.079573294502470, 0.094402155106696])
F_MOTOR = np.array([1.0, -6.548579438898973, 19.195844997585240, -32.827705701717321,
                    35.766237192312985, -25.388488121323718, 11.453950348112414,
                    -3.000061433673638, 0.349062252067493])


def colored(num, den, rng, var=NOISE_VAR):
    """Disturbance num/den e, with e scaled so that the disturbance variance is var."""
    h = lfilter(num, den, np.r_[1.0, np.zeros(4999)])
    e = np.sqrt(var / np.sum(h ** 2)) * rng.normal(size=N)
    return lfilter(num, den, e)


def multisine(rng):
    return MULTISINE


def prbs(rng):
    """Maximum-length PRBS (10 bits) from a random initial state, scaled so that the
    noise-free output of the benchmark plant has the same power as with the multisine."""
    state = rng.integers(0, 2, 10)
    state[rng.integers(10)] = 1
    s = 2.0 * max_len_seq(10, state=state, length=N)[0] - 1.0
    gain = np.std(lfilter(B3, F3, MULTISINE)) / np.std(lfilter(B3, F3, s))
    return gain * s


def white(rng):
    return rng.normal(size=N)


# name: (structure, orders, plant B, plant F, disturbance, input)
CASES = {
    "bj1": ("BJ", dict(nb=1, nc=1, nd=1, nf=3, nz=1), B3, F3,
            lambda rng: colored([1, 0.1], [1, -0.2], rng), multisine),
    "bj2": ("BJ", dict(nb=1, nc=2, nd=2, nf=3, nz=1), B3, F3,
            lambda rng: colored(np.poly([-0.1, 0.4]), np.poly([0.2, -0.5]), rng), multisine),
    "armax": ("ARMAX", dict(na=3, nb=1, nc=2, nz=1), B3, F3,
              lambda rng: colored(np.poly([0.9, 0.8]), F3, rng), multisine),
    "prbs": ("OE", dict(nb=1, nf=3, nz=1), B3, F3,
             lambda rng: np.sqrt(NOISE_VAR) * rng.normal(size=N), prbs),
    "motor": ("OE", dict(nb=8, nf=8, nz=1), B_MOTOR, F_MOTOR,
              lambda rng: 1e-4 * rng.normal(size=N), white),
}


def run_case(name, seed):
    structure, orders, B, F, disturbance, make_input = CASES[name]
    methods = C.methods(structure, orders)
    rng = np.random.default_rng(seed)

    shape = (len(methods), M)
    err, unst, fail, sec = (np.full(shape, np.nan), np.zeros(shape, bool),
                            np.zeros(shape, bool), np.full(shape, np.nan))
    snr = np.empty(M)
    for run in range(M):
        u = make_input(rng)
        y0 = lfilter(B, F, u)
        v = disturbance(rng)
        y = y0 + v
        snr[run] = 10 * np.log10(np.var(y0) / np.var(v))
        for i, f in enumerate(methods.values()):
            err[i, run], unst[i, run], fail[i, run], sec[i, run] = C.run_method(
                f, u, y, y0, structure)
        print(f"{name}: run {run + 1}/{M}", file=sys.stderr, flush=True)

    np.savez(ROOT / f"revision_{name}.npz", methods=list(methods), structure=structure,
             err=err, unstable=unst, failed=fail, seconds=sec, snr_db=snr,
             M=M, N=N, seed=seed)


if __name__ == "__main__":
    for name in sys.argv[1:]:
        run_case(name, seed=list(CASES).index(name))
