import numpy as np

from .arx import arx
from ._c._pysib_bj_core import identify as _bj_identify


def bj(u, y, nb, nc, nd, nf, nz):
    """
    [theta, m] = sib_bj(u, y, nb, nc, nd, nf, nz)

    Prediction error method with BJ structure.

             B(z)           C(z)
      y(t) = ---- u(t-nz) + ---- e(t)
             F(z)           D(z)

    Parameters
    ----------
    u : array_like
        Input signal.
    y : array_like
        Output signal.
    nb : int
        Number of parameters in B(z).
    nc : int
        Number of parameters in C(z).
    nd : int
        Number of parameters in D(z).
    nf : int
        Number of parameters in F(z).
    nz : int
        Input delay.

    Returns
    -------
    theta : ndarray
        [b_1..b_nb, c_1..c_nc, d_1..d_nd, f_1..f_nf]
    m : dict
        Model polynomials with keys A, B, C, D, F.
    """
    u = np.asarray(u, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    # ARX initial guess: returns [f_1..f_nf, b_1..b_nb]
    theta0, _ = arx(u, y, nf, nb, nz)

    # Build initial BJ theta: [b, c, d, f]
    b_part = theta0[nf:]
    f_part = theta0[:nf]

    if nd > nf:
        d_part = np.concatenate((theta0[:nf], np.zeros(nd - nf)))
    else:
        d_part = theta0[:nd]

    c_part = np.zeros(nc)
    theta1 = np.concatenate((b_part, c_part, d_part, f_part))

    theta2 = _bj_identify(u, y, theta1, nb, nc, nd, nf, nz)

    m = {
        "A": np.array([1.0]),
        "B": np.concatenate((np.zeros(nz), theta2[:nb])),
        "C": np.concatenate(([1.0], theta2[nb:nb + nc])),
        "D": np.concatenate(([1.0], theta2[nb + nc:nb + nc + nd])),
        "F": np.concatenate(([1.0], theta2[nb + nc + nd:])),
    }

    return theta2, m
