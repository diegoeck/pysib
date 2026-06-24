import numpy as np
from scipy.signal import lfilter

from .arx import arx
from ._c._pysib_oe_core import identify as _oe_identify
from ._c._pysib_armax_core import identify as _armax_identify
from ._c._pysib_bj_core import identify as _bj_identify


def _filtered_continuation_poles():
    tau = np.array([0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]) * 40
    return np.exp(np.log(0.05) / tau)


def _lowpass_filter(u, y, pole):
    b = [1 - pole]
    a = [1, -pole]
    return lfilter(b, a, u), lfilter(b, a, y)


def oe_filtered(u, y, nb, nf, nz):
    """
    theta, m = pysib.oe_filtered(u, y, nb, nf, nz)

    Filtered continuation variant of the Output Error estimator.

    Parameters
    ----------
    u : array_like
        Input signal.
    y : array_like
        Output signal.
    nb : int
        Number of B parameters.
    nf : int
        Number of F parameters.
    nz : int
        Input delay in samples. The returned B polynomial includes nz leading zeros.

    Returns
    -------
    theta : ndarray
        [b_1..b_nb, f_1..f_nf]
    m : dict
        Model with keys A, B, C, D, F.
    """
    u = np.asarray(u, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    poles = _filtered_continuation_poles()

    # Initial filter and ARX
    uf, yf = _lowpass_filter(u, y, poles[0])
    theta0, _ = arx(uf, yf, nf, nb, nz)
    theta1 = np.concatenate((theta0[nf:], theta0[:nf]))
    
    for pole in poles:
        uf, yf = _lowpass_filter(u, y, pole)
        theta2 = _oe_identify(uf, yf, theta1, nb, nf, nz)
        theta1 = theta2

    theta2 = _oe_identify(u, y, theta1, nb, nf, nz)

    m = {
        "A": np.array([1.0]),
        "B": np.concatenate((np.zeros(nz), theta2[:nb])),
        "C": np.array([1.0]),
        "D": np.array([1.0]),
        "F": np.concatenate(([1.0], theta2[nb:])),
    }
    return theta2, m


def armax_filtered(u, y, na, nb, nc, nz):
    """
    theta, m = pysib.armax_filtered(u, y, na, nb, nc, nz)

    Filtered continuation variant of the ARMAX estimator.

    Parameters
    ----------
    u : array_like
        Input signal.
    y : array_like
        Output signal.
    na : int
        Number of A parameters.
    nb : int
        Number of B parameters.
    nc : int
        Number of C parameters.
    nz : int
        Input delay in samples. The returned B polynomial includes nz leading zeros.

    Returns
    -------
    theta : ndarray
        [a_1..a_na, b_1..b_nb, c_1..c_nc]
    m : dict
        Model with keys A, B, C, D, F.
    """
    u = np.asarray(u, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    poles = _filtered_continuation_poles()

    uf, yf = _lowpass_filter(u, y, poles[0])
    theta0, _ = arx(uf, yf, na, nb, nz)
    theta1 = np.concatenate((theta0, np.zeros(nc)))

    for pole in poles:
        uf, yf = _lowpass_filter(u, y, pole)
        theta2 = _armax_identify(uf, yf, theta1, na, nb, nc, nz)
        theta1 = theta2

    theta2 = _armax_identify(u, y, theta1, na, nb, nc, nz)

    m = {
        "A": np.concatenate(([1.0], theta2[:na])),
        "B": np.concatenate((np.zeros(nz), theta2[na:na + nb])),
        "C": np.concatenate(([1.0], theta2[na + nb:])),
        "D": np.array([1.0]),
        "F": np.array([1.0]),
    }
    return theta2, m


def bj_filtered(u, y, nb, nc, nd, nf, nz):
    """
    theta, m = pysib.bj_filtered(u, y, nb, nc, nd, nf, nz)

    Filtered continuation variant of the Box-Jenkins estimator.

    Parameters
    ----------
    u : array_like
        Input signal.
    y : array_like
        Output signal.
    nb : int
        Number of B parameters.
    nc : int
        Number of C parameters.
    nd : int
        Number of D parameters.
    nf : int
        Number of F parameters.
    nz : int
        Input delay in samples. The returned B polynomial includes nz leading zeros.

    Returns
    -------
    theta : ndarray
        [b_1..b_nb, c_1..c_nc, d_1..d_nd, f_1..f_nf]
    m : dict
        Model with keys A, B, C, D, F.
    """
    u = np.asarray(u, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    poles = _filtered_continuation_poles()

    uf, yf = _lowpass_filter(u, y, poles[0])
    theta0, _ = arx(uf, yf, nf, nb, nz)

    b_part = theta0[nf:]
    if nd > nf:
        d_part = np.concatenate((theta0[:nf], np.zeros(nd - nf)))
    else:
        d_part = theta0[:nd]

    theta1 = np.concatenate((b_part, np.zeros(nc), d_part, theta0[:nf]))

    for pole in poles:
        uf, yf = _lowpass_filter(u, y, pole)
        theta2 = _bj_identify(uf, yf, theta1, nb, nc, nd, nf, nz)
        theta1 = theta2

    theta2 = _bj_identify(u, y, theta1, nb, nc, nd, nf, nz)

    m = {
        "A": np.array([1.0]),
        "B": np.concatenate((np.zeros(nz), theta2[:nb])),
        "C": np.concatenate(([1.0], theta2[nb:nb + nc])),
        "D": np.concatenate(([1.0], theta2[nb + nc:nb + nc + nd])),
        "F": np.concatenate(([1.0], theta2[nb + nc + nd:])),
    }
    return theta2, m
