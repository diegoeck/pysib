"""BJ filtered example: compare filtered vs normal BJ convergence."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import pysib

N = 1000
t = np.arange(N)
u = np.sign(np.sin(2 * np.pi * t / 100))  # square wave

# True BJ:  y = u(t-1)/(1-0.9z^-1) + (1-0.5z^-1)/(1-1.5z^-1+0.7z^-2)*e(t)
y = (lfilter([0, 1], [1, -0.9], u)
   + lfilter([1, -0.5], [1, -1.5, 0.7], 0.05 * np.random.randn(N)))

theta_bj,   m_bj   = pysib.bj(u, y, nb=1, nc=1, nd=2, nf=1, nz=1)
theta_filt, m_filt = pysib.bj_filtered(u, y, nb=1, nc=1, nd=2, nf=1, nz=1)
print("BJ         :", theta_bj)
print("BJ filtered:", theta_filt)

yp = pysib.predict(u, y, m_filt)
ys = pysib.simulate(u, m_filt)

plt.plot(t, y, "b.-", label="Data")
plt.plot(t, yp, "g.-", label="Prediction (filtered)")
plt.plot(t, ys, "r.-", label="Simulation (filtered)")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("BJ filtered: B=" + str(m_filt["B"].round(3)) +
          " C=" + str(m_filt["C"].round(3)) +
          " D=" + str(m_filt["D"].round(3)) +
          " F=" + str(m_filt["F"].round(3)))
plt.show()
