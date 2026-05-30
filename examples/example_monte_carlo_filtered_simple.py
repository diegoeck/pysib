"""Monte-Carlo simulation: save OE and OE-filtered results to disk."""
import numpy as np
from scipy.signal import lfilter
from pathlib import Path
import pysib

POLES = [0.9, 0.8, 0.7]
B_SIM = [0, 1]
F_SIM = np.poly(POLES)
NB = len(B_SIM) - 1
NF = len(F_SIM) - 1
NZ = 1

M = 100
N = 1000

t = np.arange(N)
u = (np.sin(2 * np.pi * t / 18)
   + np.sin(2 * np.pi * t / 28)
   + np.sin(2 * np.pi * t / 61))

y0 = lfilter(B_SIM, F_SIM, u) 


T_filt = np.full((NB + NF, M), np.nan)
T_oe   = np.full((NB + NF, M), np.nan)
for run in range(M):
    v0 = 30 * np.random.normal(size=N)
    y = y0 + v0

    theta_oe,   _ = pysib.oe(u, y, nb=NB, nf=NF, nz=NZ)
    theta_filt, _ = pysib.oe_filtered(u, y, nb=NB, nf=NF, nz=NZ)

    T_oe[:,   run] = theta_oe
    T_filt[:, run] = theta_filt
    print(f"run {run+1}/{M}")

np.savez(Path(__file__).parent / "mc_results.npz",
         T_oe=T_oe, T_filt=T_filt,
         B_SIM=B_SIM, F_SIM=F_SIM,
         NB=NB, NF=NF, NZ=NZ, M=M, N=N)




