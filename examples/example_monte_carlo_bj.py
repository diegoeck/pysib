"""Monte-Carlo simulation: BJ and BJ-filtered on a plant with colored noise.

Same third-order plant as the OE Monte Carlo examples, but the additive
disturbance is colored by a first-order noise model with one zero and one
pole, so the Box-Jenkins structure is the correct model class:

    y(t) = B/F u(t-1) + C/D e(t),
    C = 1 + 0.5 q^-1,  D = 1 - 0.7 q^-1.
"""
import numpy as np
from scipy.signal import lfilter
from pathlib import Path
import pysib

np.random.seed(0)

POLES = [0.9, 0.8, 0.7]
B_SIM = [0, 1]
F_SIM = np.poly(POLES)
C_SIM = [1.0, 0.1]
D_SIM = [1.0, -0.2]
NB = len(B_SIM) - 1
NC = len(C_SIM) - 1
ND = len(D_SIM) - 1
NF = len(F_SIM) - 1
NZ = 1

M = 100  # first exploratory runs; raise once the setup is settled
N = 1000
NOISE_STD = 30.0  # std of the white innovation e(t)

t = np.arange(N)
u = (np.sin(2 * np.pi * t / 18)
     + np.sin(2 * np.pi * t / 28)
     + np.sin(2 * np.pi * t / 61))

y0 = lfilter(B_SIM, F_SIM, u)

NTHETA = NB + NC + ND + NF
T_bj   = np.full((NTHETA, M), np.nan)
T_filt = np.full((NTHETA, M), np.nan)
snr_db = np.full(M, np.nan)

for run in range(M):
    e = NOISE_STD * np.random.normal(size=N)
    v = lfilter(C_SIM, D_SIM, e)
    y = y0 + v
    snr_db[run] = 10 * np.log10(np.var(y0) / np.var(v))

    theta_bj,   _ = pysib.bj(u, y, nb=NB, nc=NC, nd=ND, nf=NF, nz=NZ)
    theta_filt, _ = pysib.bj_filtered(u, y, nb=NB, nc=NC, nd=ND, nf=NF, nz=NZ)

    T_bj[:,   run] = theta_bj
    T_filt[:, run] = theta_filt
    print(f"run {run+1}/{M}")

print(f"mean SNR: {snr_db.mean():.1f} dB")

np.savez(Path(__file__).parent / "mc_results_bj.npz",
         T_bj=T_bj, T_filt=T_filt, snr_db=snr_db,
         B_SIM=B_SIM, C_SIM=C_SIM, D_SIM=D_SIM, F_SIM=F_SIM,
         NB=NB, NC=NC, ND=ND, NF=NF, NZ=NZ,
         M=M, N=N, NOISE_STD=NOISE_STD)
