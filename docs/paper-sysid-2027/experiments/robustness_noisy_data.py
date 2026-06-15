"""Monte Carlo robustness experiment for noisy OE data."""

import numpy as np
from pathlib import Path
from scipy.signal import lfilter

import pysib
from sippy_unipi import system_identification



np.random.seed(0)

M = 100
N = 1000
NOISE_STD = 1

POLES = [0.9, 0.8, 0.7]
B_SIM = [0, 1]
F_SIM = np.poly(POLES)

NB = 1
NF = 3
NZ = 1

T_sm = np.full((NB + NF, M), np.nan)
T_oe = np.full((NB + NF, M), np.nan)
T_sippy = np.full((NB + NF, M), np.nan)

t = np.arange(N)
u = (np.sin(2 * np.pi * t / 17)
     + 0.7 * np.sin(2 * np.pi * t / 43)
     + 0.4 * np.sin(2 * np.pi * t / 97))
y0 = lfilter(B_SIM, F_SIM, u)
y_run0 = None

for run in range(M):
    y = y0 + NOISE_STD * np.random.randn(N)
    if run == 0:
        y_run0 = y

    theta_sm, _ = pysib.sm(u, y, nb=NB, nf=NF, nz=NZ)
    theta_oe, _ = pysib.oe(u, y, nb=NB, nf=NF, nz=NZ)
    Id_OE = system_identification(y,u,"OE",IC="None",OE_orders=[NB,NF,0])

    T_sm[:, run] = theta_sm
    T_oe[:, run] = theta_oe
    T_sippy[:, run] = np.concatenate([[Id_OE.NUMERATOR[0][0][0]], Id_OE.DENOMINATOR[0][0][1:4]])
    print(f"run {run+1}/{M}")

np.savez(Path(__file__).parent / "robustness_noisy_data.npz",
         T_sm=T_sm, T_oe=T_oe, T_sippy=T_sippy,
         B_SIM=B_SIM, F_SIM=F_SIM,
         u=u, y0=y0, y_run0=y_run0,
         NB=NB, NF=NF, NZ=NZ,
         M=M, N=N, NOISE_STD=NOISE_STD)
