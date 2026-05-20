import numpy as np
from scipy.signal import lfilter

from .arx import arx


def sm(u, y, nb, nf, nz):
    """
    [theta, m] = sib_sm(u, y, nb, nf, nz)

    Stieglitz-McBride method for OE structure.

             B(z)
      y(t) = ---- u(t-nz) + e(t)
             F(z)

    Parameters
    ----------
    u : array_like
        Input signal.
    y : array_like
        Output signal.
    nb : int
        Number of parameters in B(z).
    nf : int
        Number of parameters in F(z) = 1 + f_1 z^-1 + ... + f_nf z^-nf.
    nz : int
        Input delay.

    Returns
    -------
    theta : ndarray
        [b_1 ... b_nb  f_1 ... f_nf]
    m : dict
        Model polynomials with keys A, B, C, D, F.
    """
    u = np.asarray(u, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    theta1, _ = arx(u, y, nf, nb, nz)

    for _ in range(100):
        F_den = np.concatenate(([1.0], theta1[:nf]))
        uf = lfilter([1.0], F_den, u)
        yf = lfilter([1.0], F_den, y)
        theta1, _ = arx(uf, yf, nf, nb, nz)

    # Reorder: ARX returns [f_1..f_nf, b_1..b_nb], we want [b_1..b_nb, f_1..f_nf]
    theta = np.concatenate((theta1[nf:], theta1[:nf]))

    m = {
        "A": np.array([1.0]),
        "B": np.concatenate((np.zeros(nz), theta1[nf:])),
        "C": np.array([1.0]),
        "D": np.array([1.0]),
        "F": np.concatenate(([1.0], theta1[:nf])),
    }

    return theta, m
