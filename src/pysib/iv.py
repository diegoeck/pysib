import numpy as np


def iv(u, y1, y2, na, nb, nz):
    """
    theta, m = pysib.iv(u, y1, y2, na, nb, nz)

    Instrumental variable (IV) method for ARX structure, using
    regressors from a second experiment as instruments.

    The input u is the same in both experiments; y1 and y2 are
    the outputs from the first and second experiments respectively.
    Because y2 shares the input-driven component with y1 but has
    independent noise, the regressor matrix of y2 serves as a
    valid instrument matrix Z.

    Solves theta = (Z.T @ Phi1)^-1 @ Z.T @ y1, where:
      - Phi1 = regressor matrix built from u and y1
      - Z   = regressor matrix built from u and y2

    Parameters
    ----------
    u : array_like
        Input signal (same in both experiments).
    y1 : array_like
        Output signal from the first experiment.
    y2 : array_like
        Output signal from the second experiment.
    na : int
        Number of A parameters.
    nb : int
        Number of B parameters.
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
    y1 = np.asarray(y1, dtype=float).ravel()
    y2 = np.asarray(y2, dtype=float).ravel()
    N = len(u)

    if len(y1) != N or len(y2) != N:
        raise ValueError(
            f"length mismatch: u={N}, y1={len(y1)}, y2={len(y2)}"
        )

    # Build phi1 (regressors from first experiment)
    cols1 = []
    for i in range(1, na + 1):
        col = np.zeros(N)
        col[i:] = -y1[:N - i]
        cols1.append(col)
    for i in range(1 + nz, nb + nz + 1):
        col = np.zeros(N)
        col[i - 1:] = u[:N - i + 1]
        cols1.append(col)
    phi1 = np.column_stack(cols1)

    # Build Z = phi2 (regressors from second experiment)
    cols2 = []
    for i in range(1, na + 1):
        col = np.zeros(N)
        col[i:] = -y2[:N - i]
        cols2.append(col)
    for i in range(1 + nz, nb + nz + 1):
        col = np.zeros(N)
        col[i - 1:] = u[:N - i + 1]
        cols2.append(col)
    Z = np.column_stack(cols2)

    # Remove initial zero rows
    skip = max(na, nb + nz - 1)
    phi1 = phi1[skip:]
    Z = Z[skip:]
    y1 = y1[skip:]

    # theta = (Z.T @ Phi1)^-1 @ Z.T @ y1 (via least squares for robustness)
    A = Z.T @ phi1
    b = Z.T @ y1
    theta = np.linalg.lstsq(A, b, rcond=None)[0]

    m = {
        "A": np.concatenate(([1.0], theta[:na])),
        "B": np.concatenate((np.zeros(nz), theta[na:])),
        "C": np.array([1.0]),
        "D": np.array([1.0]),
        "F": np.array([1.0]),
    }

    return theta, m
