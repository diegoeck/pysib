"""Monte Carlo simulation: OE vs OE filtered on non-convex problem."""

import numpy as np
from scipy.signal import lfilter
from pathlib import Path

import pysib
from sippy_unipi import system_identification

np.random.seed(0)

POLES = [0.9, 0.8, 0.7]
B_SIM = [0, 1]
F_SIM = np.poly(POLES)
NB = len(B_SIM) - 1
NF = len(F_SIM) - 1
NZ = 1

M = 100
N = 1000
NOISE_STD = 30

t = np.arange(N)
u = (np.sin(2 * np.pi * t / 18)
     + np.sin(2 * np.pi * t / 28)
     + np.sin(2 * np.pi * t / 61))

y0 = lfilter(B_SIM, F_SIM, u)

T_filt  = np.full((NB + NF, M), np.nan)
T_oe    = np.full((NB + NF, M), np.nan)
T_sippy = np.full((NB + NF, M), np.nan)
y_run0  = None

for run in range(M):
    v0 = NOISE_STD * np.random.normal(size=N)
    y = y0 + v0
    if run == 0:
        y_run0 = y

    theta_oe,   _ = pysib.oe(u, y, nb=NB, nf=NF, nz=NZ)
    theta_filt, _ = pysib.oe_filtered(u, y, nb=NB, nf=NF, nz=NZ)
    Id_OE = system_identification(y,u,"OE",IC="None",OE_orders=[NB,NF,0])
    
    T_oe[:,   run] = theta_oe
    T_filt[:, run] = theta_filt
    T_sippy[:, run] = np.concatenate([[Id_OE.NUMERATOR[0][0][0]], Id_OE.DENOMINATOR[0][0][1:4]])

    print(f"run {run+1}/{M}")

np.savez(Path(__file__).parent / "filtered_continuation_oe.npz",
         T_oe=T_oe, T_filt=T_filt, T_sippy=T_sippy,
         B_SIM=B_SIM, F_SIM=F_SIM,
         u=u, y0=y0, y_run0=y_run0,
         NB=NB, NF=NF, NZ=NZ,
         M=M, N=N, NOISE_STD=NOISE_STD)
