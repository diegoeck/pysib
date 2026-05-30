"""ARMAX filtered example: compare filtered vs normal ARMAX convergence."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import pysib

N = 1000
t = np.arange(N)
u = np.sign(np.sin(2 * np.pi * t / 100))  # square wave

# True ARMAX:  y = u(t-1)/(1-0.9z^-1) + (1-0.5z^-1)/(1-0.9z^-1)*e(t)
y = (lfilter([0, 1], [1, -0.9], u)
   + lfilter([1, -0.5], [1, -0.9], np.random.randn(N)))

theta_armax, m_armax = pysib.armax(u, y, na=1, nb=1, nc=1, nz=1)
theta_filt,  m_filt  = pysib.armax_filtered(u, y, na=1, nb=1, nc=1, nz=1)
print("ARMAX         :", theta_armax)
print("ARMAX filtered:", theta_filt)

yp = pysib.predict(u, y, m_filt)
ys = pysib.simulate(u, m_filt)

plt.plot(t, y, "b.-", label="Data")
plt.plot(t, yp, "g.-", label="Prediction (filtered)")
plt.plot(t, ys, "r.-", label="Simulation (filtered)")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("ARMAX filtered: A=" + str(m_filt["A"].round(3)) +
          " B=" + str(m_filt["B"].round(3)) +
          " C=" + str(m_filt["C"].round(3)))
plt.show()
