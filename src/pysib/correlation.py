import numpy as np


def correlation(u, y, na, nb, nz, M=20):
    """
    ARX identification by correlation error minimization.

    Minimizes ||r_{eu}(tau)||^2 over tau = 0 .. M-2, where
    r_{eu}(tau) is the cross-correlation between the prediction
    error e(t) and the input u(t-tau).

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
        Input delay.
    M : int, optional
        Number of correlation lags (default 20).

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
    R = np.zeros((M, n_theta))             # R[tau, k] = corr(u(t-tau), phi_k(t))
    r_uy = np.zeros(M)                     # r_uy[tau] = corr(u(t-tau), y(t))

    for tau in range(M):
        t0 = tau
        if N <= t0:
            break
        win = slice(t0, N)
        u_tau = u[:N - tau]
        r_uy[tau] = np.mean(u_tau * y[win])
        for k in range(n_theta):
            R[tau, k] = np.mean(u_tau * phi[win, k])

    # θ = (RᵀR)⁻¹ Rᵀ r_uy
    theta = np.linalg.lstsq(R, r_uy, rcond=None)[0]

    m = {
        "A": np.concatenate(([1.0], theta[:na])),
        "B": np.concatenate((np.zeros(nz), theta[na:])),
        "C": np.array([1.0]),
        "D": np.array([1.0]),
        "F": np.array([1.0]),
    }

    return theta, m
