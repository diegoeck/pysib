import numpy as np


def arx(u, y, na, nb, nz):
    """
    theta, m = pysib.arx(u, y, na, nb, nz)

    Least-squares estimator for the ARX structure.

             B(z)            1
      y(t) = ---- u(t-nz) + ---- e(t)
             A(z)           A(z)

    Parameters
    ----------
    u : array_like
        Input signal.
    y : array_like
        Output signal.
    na : int
        Number of parameters in A(z) = 1 + a_1 z^-1 + ... + a_na z^-na.
    nb : int
        Number of parameters in B(z) = b_1 + b_2 z^-1 + ... + b_nb z^(1-nb).
    nz : int
        Input delay in samples. The returned B polynomial includes nz leading zeros.

    Returns
    -------
    theta : ndarray
        [a_1 ... a_na  b_1 ... b_nb]
    m : dict
        Model polynomials with keys A, B, C, D, F.
    """
    u = np.asarray(u, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    N = len(u)

    cols = []

    # A polynomial terms: -y(t-1), -y(t-2), ..., -y(t-na)
    for i in range(1, na + 1):
        col = np.zeros(N)
        col[i:] = -y[:N - i]
        cols.append(col)

    # B polynomial terms: u(t-nz-1), u(t-nz-2), ..., u(t-nz-nb)
    for i in range(1 + nz, nb + nz + 1):
        col = np.zeros(N)
        col[i - 1:] = u[:N - i + 1]
        cols.append(col)

    phi = np.column_stack(cols)

    # Remove initial zero rows
    skip = max(na, nb + nz - 1)
    theta, _, _, _ = np.linalg.lstsq(phi[skip:], y[skip:], rcond=None)

    m = {
        "A": np.concatenate(([1.0], theta[:na])),
        "B": np.concatenate((np.zeros(nz), theta[na:])),
        "C": np.array([1.0]),
        "D": np.array([1.0]),
        "F": np.array([1.0]),
    }

    return theta, m
