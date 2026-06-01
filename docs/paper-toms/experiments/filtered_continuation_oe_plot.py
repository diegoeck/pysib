"""Load Monte Carlo results and generate statistics + error histogram."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

ROOT = Path(__file__).parent

data = np.load(ROOT / "filtered_continuation_oe.npz")
T_oe   = data["T_oe"]
T_filt = data["T_filt"]
B_SIM  = data["B_SIM"]
F_SIM  = data["F_SIM"]
u      = data["u"]
y0     = data["y0"]
NB     = int(data["NB"])
NF     = int(data["NF"])
NZ     = int(data["NZ"])
M      = int(data["M"])
N      = int(data["N"])
NOISE_STD = float(data["NOISE_STD"])

THRESHOLD = 0.05


def make_model(theta):
    return {
        "A": np.array([1.0]),
        "B": np.concatenate((np.zeros(NZ), theta[:NB])),
        "C": np.array([1.0]),
        "D": np.array([1.0]),
        "F": np.concatenate(([1.0], theta[NB:])),
    }


import pysib

errors_oe   = np.empty(M)
errors_filt = np.empty(M)

for i in range(M):
    m_oe   = make_model(T_oe[:, i])
    m_filt = make_model(T_filt[:, i])

    yh_oe   = pysib.simulate(u, m_oe)
    yh_filt = pysib.simulate(u, m_filt)

    errors_oe[i]   = np.linalg.norm(y0 - yh_oe)   / np.linalg.norm(y0)
    errors_filt[i] = np.linalg.norm(y0 - yh_filt) / np.linalg.norm(y0)

print("Simulation errors computed")

# --- Markdown output -----------------------------------------------------------

success_oe   = np.mean(errors_oe   < THRESHOLD)
success_filt = np.mean(errors_filt < THRESHOLD)

lines = []
lines.append("# Effect of filtered continuation\n")
lines.append(f"M = {M}, N = {N}, NOISE\\_STD = {NOISE_STD}\n")

lines.append("| method | mean error | std error | success rate (< 5%) |")
lines.append("|--------|------------|-----------|---------------------|")
lines.append(
    f"| OE | {errors_oe.mean():.6e} | {errors_oe.std(ddof=1):.6e}"
    f" | {100*success_oe:.1f}\\% |"
)
lines.append(
    f"| OE filtered | {errors_filt.mean():.6e}"
    f" | {errors_filt.std(ddof=1):.6e} | {100*success_filt:.1f}\\% |"
)

with open(ROOT / "filtered_continuation_oe_results.md", "w") as f:
    f.write("\n".join(lines))

print("filtered_continuation_oe_results.md written")

# --- Figure --------------------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

lo = min(errors_oe.min(), errors_filt.min())
hi = max(errors_oe.max(), errors_filt.max())
bins = np.linspace(lo, hi, 25)
w = (bins[1] - bins[0]) / 2
centers = (bins[:-1] + bins[1:]) / 2

counts_oe,   _ = np.histogram(errors_oe,   bins=bins)
counts_filt, _ = np.histogram(errors_filt, bins=bins)

ax = axes[0]
ax.bar(centers - w/2, counts_oe,   width=w, color="steelblue", alpha=0.85)
ax.bar(centers + w/2, counts_filt, width=w, color="tomato",   alpha=0.85)
ax.axvline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax.set_title("Simulation error distribution")
ax.set_xlabel("relative simulation error")
ax.set_ylabel("count")

ax = axes[1]
bp = ax.boxplot(
    [errors_oe, errors_filt],
    labels=["OE", "OE filtered"],
    patch_artist=True,
    widths=0.5,
)
bp["boxes"][0].set_facecolor("steelblue")
bp["boxes"][1].set_facecolor("tomato")
ax.axhline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax.set_title("Simulation error spread")
ax.set_ylabel("relative simulation error")

fig.legend(
    handles=[
        mpatches.Patch(facecolor="steelblue", label="OE"),
        mpatches.Patch(facecolor="tomato",   label="OE filtered"),
    ],
    loc="upper center", ncol=2, frameon=False,
)
fig.suptitle(
    f"Effect of filtered continuation (M={M}, N={N}, noise std={NOISE_STD})",
    y=1.02,
)
fig.tight_layout()
fig.savefig(ROOT / "filtered_continuation_oe_errors.pdf", bbox_inches="tight")
print("filtered_continuation_oe_errors.pdf written")
