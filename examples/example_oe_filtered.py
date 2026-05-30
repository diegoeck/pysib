"""OE filtered example: compare filtered vs normal OE convergence."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import pysib

N = 100
t = np.arange(N)
u = np.sign(np.sin(2 * np.pi * t / 100))  # square wave

y = lfilter([0, 1], [1, -0.9], u) + 0.1 * np.random.randn(N)

theta_oe, m_oe = pysib.oe(u, y, nb=1, nf=1, nz=1)
theta_filt, m_filt = pysib.oe_filtered(u, y, nb=1, nf=1, nz=1)

print("OE         theta:", theta_oe)
print("OE filtered theta:", theta_filt)

yp = pysib.predict(u, y, m_filt)
ys = pysib.simulate(u, m_filt)

plt.plot(t, y, "b.-", label="Data")
plt.plot(t, yp, "g.-", label="Prediction (filtered)")
plt.plot(t, ys, "r.-", label="Simulation (filtered)")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.title("OE filtered: B=" + str(m_filt["B"].round(3)) +
          " F=" + str(m_filt["F"].round(3)))
plt.show()
