"""Common estimator adapters and metrics for the revision experiments.

Every estimator is wrapped to return a model dictionary with keys A, B, C, D,
F (polynomials in q^-1, delay included in B), so that all methods are
evaluated by the same simulation-error and stability code.

Third-party packages
--------------------
* SIPPY (sippy_unipi 1.0.1), called through ``system_identification`` with
  its default options. SIPPY returns polynomials in positive powers of z with
  an implicit one-sample delay; they are converted to q^-1.
* pysid 0.1.1 (github.com/edumapurunga/pysid). Its ``solvers.ls`` passes 2-D
  columns to ``scipy.linalg.toeplitz``, which SciPy >= 1.17 treats as a batch;
  the shim below restores the 1-D behavior the package was written for. No
  other part of pysid is modified.
"""
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool

import numpy as np
import scipy.linalg
from scipy.signal import lfilter

import pysib

import pysid.identification.solvers as _pysid_solvers
from pysid.identification.pemethod import armax as _pysid_armax
from pysid.identification.pemethod import bj as _pysid_bj
from pysid.identification.pemethod import oe as _pysid_oe
from sippy_unipi import system_identification

_pysid_solvers.toeplitz = lambda c, r=None: scipy.linalg.toeplitz(
    np.ravel(c), None if r is None else np.ravel(r))

THRESHOLD = 0.05

# Polynomials that must be stable for the one-step-ahead predictor.
PREDICTOR_POLYS = {"OE": ("F",), "ARMAX": ("C",), "BJ": ("C", "F")}


def _model(A=(1.0,), B=(0.0,), C=(1.0,), D=(1.0,), F=(1.0,)):
    return {k: np.asarray(v, dtype=float) for k, v in
            zip("ABCDF", (A, B, C, D, F))}


def _from_z(num, den):
    """Convert num(z)/den(z) (positive powers, deg num < deg den) to q^-1."""
    num = np.ravel(num).astype(float)
    den = np.ravel(den).astype(float)
    return np.concatenate((np.zeros(len(den) - len(num)), num)), den


def _pysid_poly(p):
    return None if p is None else np.ravel(p[0, 0] if np.ndim(p) == 2 else p[0]).astype(float)


# --- estimators ----------------------------------------------------------------
# Each takes (structure orders, u, y) and returns a model dictionary.

def pysib_estimator(structure, filtered, orders):
    name = structure.lower() + ("_filtered" if filtered else "")
    f = getattr(pysib, name)

    def run(u, y):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            _, m = f(u, y, **orders)
        return m
    return run


def _sippy_fit(structure, orders, u, y):
    """Run SIPPY in the worker process; return (model, seconds spent in SIPPY)."""
    t0 = time.perf_counter()
    m = _sippy_model(structure, orders, u, y)
    return m, time.perf_counter() - t0


_sippy_pool = None


def sippy_estimator(structure, orders):
    """SIPPY runs in a separate process: its IPOPT/MUMPS back end occasionally
    crashes with a segmentation fault, which then counts as a failed run
    instead of stopping the experiment. The returned time is measured inside
    the worker, so it excludes the inter-process communication."""
    def run(u, y):
        global _sippy_pool
        if _sippy_pool is None:
            _sippy_pool = ProcessPoolExecutor(max_workers=1)
        try:
            return _sippy_pool.submit(_sippy_fit, structure, orders, u, y).result()
        except BrokenProcessPool:
            _sippy_pool = None
            raise RuntimeError("SIPPY worker process crashed")
    return run


def _sippy_model(structure, orders, u, y):
    """Call SIPPY with its default options and convert the result to q^-1."""
    nz = orders["nz"]
    if structure == "OE":
        s = system_identification(y, u, "OE", IC="None",
                                  OE_orders=[orders["nb"], orders["nf"], nz - 1])
        B, F = _from_z(s.NUMERATOR[0][0], s.DENOMINATOR[0][0])
        return _model(B=B, F=F)
    if structure == "ARMAX":
        s = system_identification(y, u, "ARMAX", IC="None",
                                  ARMAX_orders=[orders["na"], orders["nb"],
                                                orders["nc"], nz - 1])
        B, A = _from_z(s.NUMERATOR[0][0], s.DENOMINATOR[0][0])
        C, _ = _from_z(s.NUMERATOR_H[0][0], s.DENOMINATOR_H[0][0])
        return _model(A=A, B=B, C=C)
    if structure == "BJ":
        s = system_identification(y, u, "BJ", IC="None",
                                  BJ_orders=[orders["nb"], orders["nc"], orders["nd"],
                                             orders["nf"], nz - 1])
        B, F = _from_z(s.NUMERATOR[0][0], s.DENOMINATOR[0][0])
        C, D = _from_z(s.NUMERATOR_H[0][0], s.DENOMINATOR_H[0][0])
        return _model(B=B, C=C, D=D, F=F)
    raise ValueError(structure)


def pysid_estimator(structure, orders):
    # pysid uses the degree of B (number of coefficients minus one)
    nbd, nz = orders["nb"] - 1, orders["nz"]

    def run(u, y):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if structure == "OE":
                m = _pysid_oe(nbd, orders["nf"], nz, u[:, None], y[:, None])
            elif structure == "ARMAX":
                m = _pysid_armax(orders["na"], nbd, orders["nc"], nz, u[:, None], y[:, None])
            elif structure == "BJ":
                m = _pysid_bj(nbd, orders["nc"], orders["nd"], orders["nf"], nz,
                              u[:, None], y[:, None])
            else:
                raise ValueError(structure)
        polys = {k: _pysid_poly(getattr(m, k)) for k in "ABCDF"}
        return _model(**{k: v for k, v in polys.items() if v is not None})
    return run


def methods(structure, orders):
    """The four methods compared in every experiment, in table order."""
    return {
        "pysib": pysib_estimator(structure, False, orders),
        "pysib filtered": pysib_estimator(structure, True, orders),
        "SIPPY": sippy_estimator(structure, orders),
        "pysid": pysid_estimator(structure, orders),
    }


# --- metrics -------------------------------------------------------------------

def simulate(m, u):
    """Noise-free simulation B/(A F) u of a model dictionary."""
    return lfilter(m["B"], np.convolve(m["A"], m["F"]), u)


def simulation_error(m, u, y0):
    ys = simulate(m, u)
    if not np.all(np.isfinite(ys)):
        return np.inf
    return np.linalg.norm(y0 - ys) / np.linalg.norm(y0)


def unstable(m, structure):
    """True if a predictor polynomial has a root on or outside the unit circle."""
    for k in PREDICTOR_POLYS[structure]:
        p = m[k]
        if not np.all(np.isfinite(p)):
            return True
        if len(p) > 1 and np.max(np.abs(np.roots(p))) >= 1.0:
            return True
    return False


def timed(f, *args, **kwargs):
    """Return (f(*args, **kwargs), elapsed seconds)."""
    t0 = time.perf_counter()
    out = f(*args, **kwargs)
    return out, time.perf_counter() - t0


def oe_theta(m, nb, nz):
    """[b_1..b_nb, f_1..f_nf] of an OE model dictionary."""
    return np.concatenate((m["B"][nz:nz + nb], m["F"][1:]))


def run_method(f, u, y, y0, structure):
    """Run one estimator; return (simulation error, unstable, failed, seconds)."""
    t0 = time.perf_counter()
    try:
        m = f(u, y)
    except Exception:
        return np.inf, False, True, time.perf_counter() - t0
    dt = time.perf_counter() - t0
    if isinstance(m, tuple):  # (model, seconds measured by the estimator itself)
        m, dt = m
    return simulation_error(m, u, y0), unstable(m, structure), False, dt


def summarize(err, unst, fail, sec):
    """Row of the summary table for one method (arrays over Monte Carlo runs)."""
    ok = np.isfinite(err)
    return {
        "success": 100 * np.mean(err < THRESHOLD),
        "median_error": np.median(err) if ok.any() else np.nan,
        "mean_error": np.mean(err[ok]) if ok.any() else np.nan,
        "unstable": int(np.sum(unst)),
        "failed": int(np.sum(fail)),
        "time": np.median(sec),
    }
