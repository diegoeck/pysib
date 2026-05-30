"""ARX example: estimate y = B/A*u + 1/A*e from data."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import pysib

N = 1000
t = np.arange(N)
u = np.sign(np.sin(2 * np.pi * t / 100))  # square wave

# True model:  y(t) = 0.9*y(t-1) + u(t-1) + e(t)
G_num, G_den = [0, 1], [1, -0.9]
H_num, H_den = [1], [1, -0.9]
y = lfilter(G_num, G_den, u) + lfilter(H_num, H_den, np.random.randn(N))

theta, m = pysib.arx(u, y, na=1, nb=1, nz=1)
print("theta:", theta)

yp = pysib.predict(u, y, m)
ys = pysib.simulate(u, m)

plt.plot(t, y, "b.-", label="Data")
plt.plot(t, yp, "g.-", label="Prediction")
plt.plot(t, ys, "r.-", label="Simulation")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("ARX: " + str(m))
plt.show()
