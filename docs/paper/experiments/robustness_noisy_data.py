"""Monte Carlo robustness experiment for noisy OE data."""

import numpy as np
from pathlib import Path
from scipy.signal import lfilter

import pysib


np.random.seed(0)

M = 500
N = 500
NOISE_STD = 0.1

B_SIM = [0, 1]
F_SIM = np.poly([0.75, 0.35])

NA = 2
NB = 1
NF = 2
NZ = 1

T_arx = np.full((NA + NB, M), np.nan)
T_sm = np.full((NB + NF, M), np.nan)
T_oe = np.full((NB + NF, M), np.nan)

t = np.arange(N)
u = (np.sin(2 * np.pi * t / 17)
     + 0.7 * np.sin(2 * np.pi * t / 43)
     + 0.4 * np.sin(2 * np.pi * t / 97))
y0 = lfilter(B_SIM, F_SIM, u)

for run in range(M):
    y = y0 + NOISE_STD * np.random.randn(N)

    theta_arx, _ = pysib.arx(u, y, na=NA, nb=NB, nz=NZ)
    theta_sm, _ = pysib.sm(u, y, nb=NB, nf=NF, nz=NZ)
    theta_oe, _ = pysib.oe(u, y, nb=NB, nf=NF, nz=NZ)

    T_arx[:, run] = theta_arx
    T_sm[:, run] = theta_sm
    T_oe[:, run] = theta_oe

    print(f"run {run+1}/{M}")

np.savez(Path(__file__).parent / "robustness_noisy_data.npz",
         T_arx=T_arx, T_sm=T_sm, T_oe=T_oe,
         B_SIM=B_SIM, F_SIM=F_SIM,
         NA=NA, NB=NB, NF=NF, NZ=NZ,
         M=M, N=N, NOISE_STD=NOISE_STD)
