"""Correlation method: compare with ARX on an ARX process."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import pysib

N = 1000
t = np.arange(N)
u = np.sign(np.sin(2 * np.pi * t / 100))

# True ARX: y(t) = 0.9*y(t-1) + u(t-1) + e(t)
y = lfilter([0, 1], [1, -0.9], u) + np.random.randn(N)

theta_ls, m_ls = pysib.arx(u, y, na=1, nb=1, nz=1)
theta_corr, m_corr = pysib.correlation(u, y, na=1, nb=1, nz=1, M=30)

print("ARX        :", theta_ls)
print("Correlation:", theta_corr)

yp = pysib.predict(u, y, m_corr)
ys = pysib.simulate(u, m_corr)

plt.plot(t, y, "b.-", label="Data")
plt.plot(t, yp, "g.-", label="Prediction (correlation)")
plt.plot(t, ys, "r.-", label="Simulation (correlation)")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("Correlation method: B=" + str(m_corr["B"].round(3)) + " A=" + str(m_corr["A"].round(3)))
plt.show()
