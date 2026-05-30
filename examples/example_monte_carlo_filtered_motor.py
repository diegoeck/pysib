"""Monte-Carlo simulation (motor system): save OE and OE-filtered results to disk."""
import numpy as np
from scipy.signal import lfilter
from pathlib import Path
import pysib

B_SIM = np.array([
    0,
    -0.207296003971350,
     0.181497963178803,
     1.351706842960986,
    -3.356365092407725,
     3.060933791693723,
    -1.045306362058663,
    -0.079573294502470,
     0.094402155106696,
])

F_SIM = np.array([
    1.0,
    -6.548579438898973,
    19.195844997585240,
   -32.827705701717321,
    35.766237192312985,
   -25.388488121323718,
    11.453950348112414,
    -3.000061433673638,
     0.349062252067493,
])

NB = len(B_SIM) - 1
NF = len(F_SIM) - 1
NZ = 1

M = 10
N = 1000

u = np.random.normal(size=N)

T_filt = np.full((NB + NF, M), np.nan)
T_oe   = np.full((NB + NF, M), np.nan)
for run in range(M):
    y = lfilter(B_SIM, F_SIM, u) + 0.0001 * np.random.normal(size=N)

    theta_oe,   _ = pysib.oe(u, y, nb=NB, nf=NF, nz=NZ)
    theta_filt, _ = pysib.oe_filtered(u, y, nb=NB, nf=NF, nz=NZ)

    T_oe[:,   run] = theta_oe
    T_filt[:, run] = theta_filt
    print(f"run {run+1}/{M}")

np.savez(Path(__file__).parent / "mc_results_motor.npz",
         T_oe=T_oe, T_filt=T_filt,
         B_SIM=B_SIM, F_SIM=F_SIM,
         NB=NB, NF=NF, NZ=NZ, M=M, N=N)
