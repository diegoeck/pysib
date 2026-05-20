import numpy as np

from .arx import arx
from ._c._pysib_armax_core import identify as _armax_identify


def armax(u, y, na, nb, nc, nz):
    """
    [theta, m] = sib_armax(u, y, na, nb, nc, nz)

    Prediction error method with ARMAX structure.

             B(z)           C(z)
      y(t) = ---- u(t-nz) + ---- e(t)
             A(z)           A(z)

    Parameters
    ----------
    u : array_like
        Input signal.
    y : array_like
        Output signal.
    na : int
        Number of parameters in A(z).
    nb : int
        Number of parameters in B(z).
    nc : int
        Number of parameters in C(z).
    nz : int
        Input delay.

    Returns
    -------
    theta : ndarray
        [a_1..a_na, b_1..b_nb, c_1..c_nc]
    m : dict
        Model polynomials with keys A, B, C, D, F.
    """
    u = np.asarray(u, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    theta0, _ = arx(u, y, na, nb, nz)
    theta1 = np.concatenate((theta0, np.zeros(nc)))

    theta2 = _armax_identify(u, y, theta1, na, nb, nc, nz)

    m = {
        "A": np.concatenate(([1.0], theta2[:na])),
        "B": np.concatenate((np.zeros(nz), theta2[na:na + nb])),
        "C": np.concatenate(([1.0], theta2[na + nb:])),
        "D": np.array([1.0]),
        "F": np.array([1.0]),
    }

    return theta2, m
