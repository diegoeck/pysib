import warnings

import numpy as np


def warn_if_unstable(m, keys, estimator, alternative=None):
    """
    Warn when a predictor polynomial of an estimated model is not stable.

    The one-step-ahead predictor requires the polynomials listed in `keys`
    (OE: F; ARMAX: C; BJ: C and F) to have all roots strictly inside the unit
    circle. The optimizer does not impose this, so it is checked on the
    returned model.

    Parameters
    ----------
    m : dict
        Model polynomials with keys A, B, C, D, F.
    keys : str or sequence of str
        Keys of the polynomials that must be stable.
    estimator : str
        Name of the estimator, used in the message.
    alternative : str, optional
        Estimator suggested in the message (e.g. the filtered variant).
    """
    unstable = []
    for key in keys:
        p = np.asarray(m[key], dtype=float)
        if not np.all(np.isfinite(p)):
            unstable.append(key)
        elif len(p) > 1 and np.max(np.abs(np.roots(p))) >= 1.0:
            unstable.append(key)

    if unstable:
        msg = (f"pysib.{estimator}: the estimated polynomial {' and '.join(unstable)} "
               "has roots on or outside the unit circle, so the model is not a valid "
               "(stable) predictor. This often indicates convergence to a poor local "
               "minimum")
        if alternative is not None:
            msg += f"; consider pysib.{alternative}"
        warnings.warn(msg + ".", RuntimeWarning, stacklevel=3)
