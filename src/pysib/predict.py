from scipy.signal import lfilter
import numpy as np


def predict(u, y, m):
    """
    yp = pysib.predict(u, y, m)

    One-step-ahead prediction.

    yp(t) = y(t) + H(z)^(-1) ( G(z)*u(t) - y(t) )

    Parameters
    ----------
    u : array_like
        Input signal.
    y : array_like
        Output signal.
    m : dict
        Model with keys A, B, C, D, F (1D arrays).

    Returns
    -------
    yp : ndarray
        Predicted output.
    """
    u = np.asarray(u, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()

    yf = lfilter(m["B"], m["A"], u)
    yf = lfilter([1.0], m["F"], yf) - y
    yf = lfilter(m["D"], m["C"], yf)
    yp = y + lfilter(m["A"], [1.0], yf)

    return yp


def simulate(u, m):
    """
    ys = pysib.simulate(u, m)

    Simulate model output (noise-free).

    ys(t) = G(z) * u(t)

    Parameters
    ----------
    u : array_like
        Input signal.
    m : dict
        Model with keys A, B, C, D, F (1D arrays).

    Returns
    -------
    ys : ndarray
        Simulated output.
    """
    u = np.asarray(u, dtype=float).ravel()

    ys = lfilter(m["B"], m["A"], u)
    ys = lfilter([1.0], m["F"], ys)

    return ys
