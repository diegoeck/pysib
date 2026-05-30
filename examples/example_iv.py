"""IV example: instrumental variables vs ARX on a noisy ARX process."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import pysib

N = 1000
t = np.arange(N)
u = np.sign(np.sin(2 * np.pi * t / 100))  # square wave

# True ARX: y(t) = 0.9*y(t-1) + u(t-1) + e(t)
# Two independent experiments with the same input
y1 = lfilter([0, 1], [1, -0.9], u) + np.random.randn(N)
y2 = lfilter([0, 1], [1, -0.9], u) + np.random.randn(N)

theta_arx, m_arx = pysib.arx(u, y1, na=1, nb=1, nz=1)
theta_iv,  m_iv  = pysib.iv(u, y1, y2, na=1, nb=1, nz=1)
print("ARX:", theta_arx)
print("IV :", theta_iv)

yp = pysib.predict(u, y1, m_iv)
ys = pysib.simulate(u, m_iv)

plt.plot(t, y1, "b.-", label="Data")
plt.plot(t, yp, "g.-", label="Prediction (IV)")
plt.plot(t, ys, "r.-", label="Simulation (IV)")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("IV: A=" + str(m_iv["A"].round(3)) + " B=" + str(m_iv["B"].round(3)))
plt.show()
