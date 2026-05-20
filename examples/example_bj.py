"""BJ example: estimate y = B/F*u + C/D*e from data."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import pysib

N = 1000
t = np.arange(N)
u = np.sign(np.sin(2 * np.pi * t / 100))  # square wave

# True BJ model:
#   y = u(t-1) / (1-0.9*z^-1)  +  (1-0.5*z^-1)/(1-1.5*z^-1+0.7*z^-2) * e(t)
G_num, G_den = [0, 1], [1, -0.9]
H_num, H_den = [1, -0.5], [1, -1.5, 0.7]
e = 0.05 * np.random.randn(N)
y = lfilter(G_num, G_den, u) + lfilter(H_num, H_den, e)

theta, m = sib.bj(u, y, nb=1, nc=1, nd=2, nf=1, nz=1)
print("theta:", theta)

yp = sib.predict(u, y, m)
ys = sib.simulate(u, m)

plt.plot(t, y, "b.-", label="Data")
plt.plot(t, yp, "g.-", label="Prediction")
plt.plot(t, ys, "r.-", label="Simulation")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("BJ: B=" + str(m["B"].round(3)) + " C=" + str(m["C"].round(3)) +
          " D=" + str(m["D"].round(3)) + " F=" + str(m["F"].round(3)))
plt.show()
