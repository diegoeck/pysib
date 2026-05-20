"""Exact parameter recovery tests for all sib estimators (noise-free data)."""
import numpy as np
from scipy.signal import lfilter
import pysib


def _sin_input(N):
    """Generate a persistently exciting input signal."""
    return np.sin(np.arange(N) * 2 * np.pi / 17)


def test_arx_exact():
    """ARX: recover y(t) = 0.5*y(t-1) + u(t-1) with machine precision."""
    N = 500
    u = _sin_input(N)
    # y(t) = 0.5*y(t-1) + u(t-1)  =>  A = [1, -0.5], B = [0, 1], nz=1
    y = lfilter([0, 1], [1, -0.5], u)

    theta, m = pysib.arx(u, y, na=1, nb=1, nz=1)

    assert abs(theta[0] - (-0.5)) < 1e-10   # a1
    assert abs(theta[1] - 1.0) < 1e-10      # b1


def test_sm_exact():
    """SM: recover OE model y = u(t-1) / (1 - 0.7*z^-1)."""
    N = 500
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.7], u)

    theta, m = pysib.sm(u, y, nb=1, nf=1, nz=1)

    assert abs(theta[0] - 1.0) < 1e-6       # b1
    assert abs(theta[1] - (-0.7)) < 1e-6    # f1


def test_oe_exact():
    """OE: recover y = u(t-1) / (1 - 0.7*z^-1) with C optimizer."""
    N = 500
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.7], u)

    theta, m = pysib.oe(u, y, nb=1, nf=1, nz=1)

    assert abs(theta[0] - 1.0) < 1e-4       # b1
    assert abs(theta[1] - (-0.7)) < 1e-4    # f1


def test_armax_exact():
    """ARMAX with nc=0: recover y(t) = 0.5*y(t-1) + u(t-1)."""
    N = 500
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.5], u)

    theta, m = pysib.armax(u, y, na=1, nb=1, nc=0, nz=1)

    assert abs(theta[0] - (-0.5)) < 1e-4    # a1
    assert abs(theta[1] - 1.0) < 1e-4       # b1


def test_bj_exact():
    """BJ with nc=0,nd=0: recover y = u(t-1) / (1 - 0.7*z^-1)."""
    N = 500
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.7], u)

    theta, m = pysib.bj(u, y, nb=1, nc=0, nd=0, nf=1, nz=1)

    assert abs(theta[0] - 1.0) < 1e-4       # b1
    assert abs(theta[1] - (-0.7)) < 1e-4    # f1


def test_predict_simulate_shapes():
    """Predict and simulate return correct array lengths."""
    N = 100
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.5], u)
    _, m = pysib.arx(u, y, na=1, nb=1, nz=1)

    yp = pysib.predict(u, y, m)
    ys = pysib.simulate(u, m)

    assert len(yp) == N
    assert len(ys) == N


def test_polynomial_convention():
    """Model dict follows A,B,C,D,F convention with correct shapes."""
    N = 200
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.5], u)

    _, m = pysib.arx(u, y, na=2, nb=3, nz=2)
    assert len(m["A"]) == 3    # 1 + na
    assert len(m["B"]) == 5    # nz + nb
    assert len(m["C"]) == 1    # [1]
    assert len(m["D"]) == 1    # [1]
    assert len(m["F"]) == 1    # [1]
    assert m["A"][0] == 1.0
    assert m["C"][0] == 1.0
    assert m["D"][0] == 1.0
    assert m["F"][0] == 1.0


def test_filtered_basic():
    """Filtered variants run and return correct theta shape."""
    N =  200 
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.7], u)

    theta, m = pysib.oe_filtered(u, y, nb=1, nf=1, nz=1)
    assert len(theta) == 2

    theta, m = pysib.armax_filtered(u, y, na=1, nb=1, nc=0, nz=1)
    assert len(theta) == 2


def test_correlation_exact():
    """Correlation: recover y = 0.5*y(t-1) + u(t-1) exactly."""
    N = 500
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.5], u)

    theta, m = pysib.correlation(u, y, na=1, nb=1, nz=1, M=30)

    assert abs(theta[0] - (-0.5)) < 1e-6   # a1
    assert abs(theta[1] - 1.0) < 1e-6       # b1


def test_iv_noisy():
    """IV: consistent recovery with independent noise."""
    N = 500
    u = _sin_input(N)
    rng = np.random.RandomState(42)
    y_true = lfilter([0, 1], [1, -0.5], u)
    e1 = 0.01 * rng.randn(N)
    e2 = 0.01 * rng.randn(N)
    y1 = y_true + e1
    y2 = y_true + e2

    theta, m = pysib.iv(u, y1, y2, na=1, nb=1, nz=1)

    assert abs(theta[0] - (-0.5)) < 1e-2   # a1
    assert abs(theta[1] - 1.0) < 1e-2      # b1


def test_iv_exact():
    """IV: recover y = 0.5*y(t-1) + u(t-1) with noise-free repeated experiment."""
    N = 500
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.5], u)

    theta, m = pysib.iv(u, y, y, na=1, nb=1, nz=1)

    assert abs(theta[0] - (-0.5)) < 1e-10   # a1
    assert abs(theta[1] - 1.0) < 1e-10      # b1


def test_arx_noisy():
    """ARX: consistent with small noise."""
    N = 500
    u = _sin_input(N)
    rng = np.random.RandomState(42)
    y_true = lfilter([0, 1], [1, -0.5], u)
    y = y_true + 0.01 * rng.randn(N)

    theta, m = pysib.arx(u, y, na=1, nb=1, nz=1)

    assert abs(theta[0] - (-0.5)) < 1e-2   # a1
    assert abs(theta[1] - 1.0) < 1e-2      # b1


def test_sm_noisy():
    """SM: consistent with small noise."""
    N = 500
    u = _sin_input(N)
    rng = np.random.RandomState(42)
    y_true = lfilter([0, 1], [1, -0.7], u)
    y = y_true + 0.01 * rng.randn(N)

    theta, m = pysib.sm(u, y, nb=1, nf=1, nz=1)

    assert abs(theta[0] - 1.0) < 1e-2       # b1
    assert abs(theta[1] - (-0.7)) < 1e-2    # f1


def test_oe_noisy():
    """OE: consistent with small noise."""
    N = 500
    u = _sin_input(N)
    rng = np.random.RandomState(42)
    y_true = lfilter([0, 1], [1, -0.7], u)
    y = y_true + 0.01 * rng.randn(N)

    theta, m = pysib.oe(u, y, nb=1, nf=1, nz=1)

    assert abs(theta[0] - 1.0) < 1e-2       # b1
    assert abs(theta[1] - (-0.7)) < 1e-2    # f1


def test_armax_noisy():
    """ARMAX: consistent with small noise (nc=0)."""
    N = 500
    u = _sin_input(N)
    rng = np.random.RandomState(42)
    y_true = lfilter([0, 1], [1, -0.5], u)
    y = y_true + 0.01 * rng.randn(N)

    theta, m = pysib.armax(u, y, na=1, nb=1, nc=0, nz=1)

    assert abs(theta[0] - (-0.5)) < 1e-2    # a1
    assert abs(theta[1] - 1.0) < 1e-2       # b1


def test_bj_noisy():
    """BJ: consistent with small noise (nc=0, nd=0)."""
    N = 500
    u = _sin_input(N)
    rng = np.random.RandomState(42)
    y_true = lfilter([0, 1], [1, -0.7], u)
    y = y_true + 0.01 * rng.randn(N)

    theta, m = pysib.bj(u, y, nb=1, nc=0, nd=0, nf=1, nz=1)

    assert abs(theta[0] - 1.0) < 1e-2       # b1
    assert abs(theta[1] - (-0.7)) < 1e-2    # f1


def test_correlation_noisy():
    """Correlation: consistent with small noise."""
    N = 500
    u = _sin_input(N)
    rng = np.random.RandomState(42)
    y_true = lfilter([0, 1], [1, -0.5], u)
    y = y_true + 0.01 * rng.randn(N)

    theta, m = pysib.correlation(u, y, na=1, nb=1, nz=1, M=30)

    assert abs(theta[0] - (-0.5)) < 1e-2    # a1
    assert abs(theta[1] - 1.0) < 1e-2       # b1


def test_oe_filtered_exact():
    """OE filtered: recover y = u(t-1) / (1 - 0.7*z^-1)."""
    N = 500
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.7], u)

    theta, m = pysib.oe_filtered(u, y, nb=1, nf=1, nz=1)

    assert abs(theta[0] - 1.0) < 1e-4       # b1
    assert abs(theta[1] - (-0.7)) < 1e-4    # f1


def test_armax_filtered_exact():
    """ARMAX filtered: recover y(t) = 0.5*y(t-1) + u(t-1) with nc=0."""
    N = 500
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.5], u)

    theta, m = pysib.armax_filtered(u, y, na=1, nb=1, nc=0, nz=1)

    assert abs(theta[0] - (-0.5)) < 1e-4    # a1
    assert abs(theta[1] - 1.0) < 1e-4       # b1


def test_bj_filtered_exact():
    """BJ filtered: recover y = u(t-1) / (1 - 0.7*z^-1) with nc=0, nd=0."""
    N = 500
    u = _sin_input(N)
    y = lfilter([0, 1], [1, -0.7], u)

    theta, m = pysib.bj_filtered(u, y, nb=1, nc=0, nd=0, nf=1, nz=1)

    assert abs(theta[0] - 1.0) < 1e-4       # b1
    assert abs(theta[1] - (-0.7)) < 1e-4    # f1


def test_oe_filtered_noisy():
    """OE filtered: consistent with small noise."""
    N = 500
    u = _sin_input(N)
    rng = np.random.RandomState(42)
    y_true = lfilter([0, 1], [1, -0.7], u)
    y = y_true + 0.01 * rng.randn(N)

    theta, m = pysib.oe_filtered(u, y, nb=1, nf=1, nz=1)

    assert abs(theta[0] - 1.0) < 1e-2       # b1
    assert abs(theta[1] - (-0.7)) < 1e-2    # f1


def test_armax_filtered_noisy():
    """ARMAX filtered: consistent with small noise (nc=0)."""
    N = 500
    u = _sin_input(N)
    rng = np.random.RandomState(42)
    y_true = lfilter([0, 1], [1, -0.5], u)
    y = y_true + 0.01 * rng.randn(N)

    theta, m = pysib.armax_filtered(u, y, na=1, nb=1, nc=0, nz=1)

    assert abs(theta[0] - (-0.5)) < 1e-2    # a1
    assert abs(theta[1] - 1.0) < 1e-2       # b1


def test_bj_filtered_noisy():
    """BJ filtered: consistent with small noise (nc=0, nd=0)."""
    N = 500
    u = _sin_input(N)
    rng = np.random.RandomState(42)
    y_true = lfilter([0, 1], [1, -0.7], u)
    y = y_true + 0.01 * rng.randn(N)

    theta, m = pysib.bj_filtered(u, y, nb=1, nc=0, nd=0, nf=1, nz=1)

    assert abs(theta[0] - 1.0) < 1e-2       # b1
    assert abs(theta[1] - (-0.7)) < 1e-2    # f1
