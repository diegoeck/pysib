"""SM example: Stieglitz-McBride vs OE on an OE process."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import pysib

N = 100
t = np.arange(N)
u = np.sign(np.sin(2 * np.pi * t / 100))  # square wave

# True OE model:  y(t) = u(t-1) / (1 - 0.9*z^-1) + e(t)
y = lfilter([0, 1], [1, -0.9], u) + 0.01 * np.random.randn(N)

theta_sm, m_sm = pysib.sm(u, y, nb=1, nf=1, nz=1)
theta_oe, m_oe = pysib.oe(u, y, nb=1, nf=1, nz=1)
print("SM theta:", theta_sm)
print("OE theta:", theta_oe)

yp = pysib.predict(u, y, m_sm)
ys = pysib.simulate(u, m_sm)

plt.plot(t, y, "b.-", label="Data")
plt.plot(t, yp, "g.-", label="Prediction (SM)")
plt.plot(t, ys, "r.-", label="Simulation (SM)")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("SM: B=" + str(m_sm["B"].round(3)) + " F=" + str(m_sm["F"].round(3)))
plt.show()
