import numpy as np
import matplotlib.pyplot as plt


def plota(T, a):
    """
    Plot Monte-Carlo data ordered by parameter *a*.

    Torg = sib_plota(T, a)

    Parameters
    ----------
    T : ndarray, shape (n_params, n_runs)
        Monte-Carlo parameter estimates.
    a : int
        Row index to sort by (0-based; MATLAB version used 1-based).

    Returns
    -------
    Torg : ndarray
        Sorted parameter matrix (n_params, n_runs).
    """
    T = np.asarray(T)
    idx = np.argsort(T[a, :])
    Torg = T[:, idx]

    plt.plot(Torg.T)
    plt.xlim(0, Torg.shape[1] + 1)
    plt.xlabel("Monte-Carlo run")
    plt.ylabel("theta")

    return Torg
