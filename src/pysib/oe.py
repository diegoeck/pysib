import numpy as np

from .arx import arx
from ._c._pysib_oe_core import identify as _oe_identify


def oe(u, y, nb, nf, nz):
    """
    theta, m = pysib.oe(u, y, nb, nf, nz)

    Prediction-error estimator for the Output Error structure.

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
        Input delay in samples. The returned B polynomial includes nz leading zeros.

    Returns
    -------
    theta : ndarray
        [b_1 ... b_nb  f_1 ... f_nf]
    m : dict
        Model polynomials with keys A, B, C, D, F.
    """
    u = np.asarray(u, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    # ARX initial guess: ARX returns [f_1..f_nf, b_1..b_nb]
    theta0, _ = arx(u, y, nf, nb, nz)
    # Reorder to [b_1..b_nb, f_1..f_nf]
    theta1 = np.concatenate((theta0[nf:], theta0[:nf]))

    # C optimizer
    theta2 = _oe_identify(u, y, theta1, nb, nf, nz)

    m = {
        "A": np.array([1.0]),
        "B": np.concatenate((np.zeros(nz), theta2[:nb])),
        "C": np.array([1.0]),
        "D": np.array([1.0]),
        "F": np.concatenate(([1.0], theta2[nb:])),
    }

    return theta2, m
