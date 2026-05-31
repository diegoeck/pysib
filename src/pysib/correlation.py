import numpy as np


def correlation(u, y, na, nb, nz, M=20, z=None):
    """
    theta, m = pysib.correlation(u, y, na, nb, nz, M=20, z=None)

    ARX identification by correlation error minimization.

    Minimizes ||r_ez(tau)||^2 over tau = 0 .. M-1, where
    r_ez(tau) is the cross-correlation between the prediction
    error e(t) and the instrument z(t-tau). If z is not provided,
    the input u is used as the instrument.

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
    nz : int
        Input delay in samples. The returned B polynomial includes nz leading zeros.
    M : int, optional
        Number of correlation lags (default 20).
    z : array_like, optional
        External instrument for cross-correlation. If None (default),
        the input u is used as the instrument.

    Returns
    -------
    theta : ndarray
        [a_1..a_na, b_1..b_nb].
    m : dict
        Model polynomials A, B, C, D, F.
    """
    u = np.asarray(u, dtype=float).ravel()
    y = np.asarray(y, dtype=float).ravel()
    N = len(u)

    # Use external instrument if provided, otherwise u is the instrument
    if z is not None:
        z = np.asarray(z, dtype=float).ravel()
        if len(z) != N:
            raise ValueError(
                f"instrument z has length {len(z)}, expected {N} "
                f"(same as u and y)"
            )
    else:
        z = u

    # Build regressor matrix phi (same as ARX)
    cols = []
    for i in range(1, na + 1):
        col = np.zeros(N)
        col[i:] = -y[:N - i]
        cols.append(col)
    for i in range(1 + nz, nb + nz + 1):
        col = np.zeros(N)
        col[i - 1:] = u[:N - i + 1]
        cols.append(col)
    phi = np.column_stack(cols)            # N x (na+nb)

    n_theta = na + nb
    R = np.zeros((M, n_theta))             # R[tau, k] = corr(z(t-tau), phi_k(t))
    r_zy = np.zeros(M)                     # r_zy[tau] = corr(z(t-tau), y(t))

    for tau in range(M):
        t0 = tau
        if N <= t0:
            break
        win = slice(t0, N)
        z_tau = z[:N - tau]
        r_zy[tau] = np.mean(z_tau * y[win])
        for k in range(n_theta):
            R[tau, k] = np.mean(z_tau * phi[win, k])

    # theta = (R.T @ R)^-1 @ R.T @ r_zy
    theta = np.linalg.lstsq(R, r_zy, rcond=None)[0]

    m = {
        "A": np.concatenate(([1.0], theta[:na])),
        "B": np.concatenate((np.zeros(nz), theta[na:])),
        "C": np.array([1.0]),
        "D": np.array([1.0]),
        "F": np.array([1.0]),
    }

    return theta, m
