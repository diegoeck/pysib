"""Monte-Carlo: run OE 30 times and plot parameter spread."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import pysib

M = 30
N = 100
T = np.full((2, M), np.nan)

for run in range(M):
    t = np.arange(N)
    u = np.sign(np.sin(2 * np.pi * t / 100))
    y = lfilter([0, 1], [1, -0.9], u) + 0.01 * np.random.randn(N)

    theta, _ = sib.oe(u, y, nb=1, nf=1, nz=1)
    T[:, run] = theta

T_sorted = sib.plota(T, a=0)
plt.title("OE Monte-Carlo (30 runs)")
plt.show()
