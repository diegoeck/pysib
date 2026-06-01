"""Load Monte Carlo results and generate statistics + parameter histogram."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

ROOT = Path(__file__).parent

data = np.load(ROOT / "robustness_noisy_data.npz")
T_arx = data["T_arx"]
T_sm  = data["T_sm"]
T_oe  = data["T_oe"]
B_SIM = data["B_SIM"]
F_SIM = data["F_SIM"]
M     = int(data["M"])
N     = int(data["N"])
NOISE_STD = float(data["NOISE_STD"])

# --- Markdown output -----------------------------------------------------------

lines = []
lines.append("# Robustness under noisy data\n")
lines.append(f"M = {M}, N = {N}, NOISE\\_STD = {NOISE_STD}\n")
lines.append("## True OE parameters\n")
lines.append("| parameter | value |")
lines.append("|-----------|-------|")
lines.append(f"| $b_1$ | {B_SIM[1]:.8f} |")
for i, value in enumerate(F_SIM[1:], start=1):
    lines.append(f"| $f_{i}$ | {value:.8f} |")

lines.append("\n## OE-structure estimates (SM and OE)\n")
lines.append("| method | parameter | mean | std |")
lines.append("|--------|-----------|------|-----|")
oe_labels = ["$b_1$", "$f_1$", "$f_2$"]
for method_name, matrix in [("SM", T_sm), ("OE", T_oe)]:
    for i, label in enumerate(oe_labels):
        mean = np.mean(matrix[i, :])
        std  = np.std(matrix[i, :], ddof=1)
        lines.append(f"| {method_name} | {label} | {mean:.8f} | {std:.8f} |")

lines.append("\n## ARX baseline parameters (not directly comparable to OE parameters)\n")
lines.append("| parameter | mean | std |")
lines.append("|-----------|------|-----|")
for i in range(T_arx.shape[0]):
    mean = np.mean(T_arx[i, :])
    std  = np.std(T_arx[i, :], ddof=1)
    lines.append(f"| $\\theta_{{{i+1}}}$ | {mean:.8f} | {std:.8f} |")

with open(ROOT / "robustness_noisy_data_results.md", "w") as f:
    f.write("\n".join(lines))

print("robustness_noisy_data_results.md written")

# --- Figure --------------------------------------------------------------------

true_vals = [B_SIM[1]] + list(F_SIM[1:])
labels    = ["$b_1$", "$f_1$", "$f_2$"]

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))

for ax, lbl, tv, idx in zip(axes, labels, true_vals, range(3)):
    all_vals = np.concatenate([T_sm[idx], T_oe[idx]])
    lo   = np.nanmin(all_vals)
    hi   = np.nanmax(all_vals)
    bins = np.linspace(lo, hi, 20)
    w    = (bins[1] - bins[0]) / 2
    centers = (bins[:-1] + bins[1:]) / 2

    counts_sm, _ = np.histogram(T_sm[idx], bins=bins)
    counts_oe, _ = np.histogram(T_oe[idx], bins=bins)

    ax.bar(centers - w / 2, counts_sm, width=w, color="steelblue", alpha=0.85)
    ax.bar(centers + w / 2, counts_oe, width=w, color="tomato",   alpha=0.85)
    ax.axvline(tv, color="k", linestyle="--", linewidth=1)
    ax.set_title(lbl)
    ax.set_xlabel("value")
    if idx == 0:
        ax.set_ylabel("count")

fig.legend(
    handles=[
        mpatches.Patch(facecolor="steelblue", label="SM"),
        mpatches.Patch(facecolor="tomato",   label="OE"),
    ],
    loc="upper center", ncol=2, frameon=False,
)
fig.suptitle(f"Robustness under noisy data (M={M}, N={N}, noise std={NOISE_STD})", y=1.02)
fig.tight_layout()
fig.savefig(ROOT / "robustness_noisy_data_parameters.pdf", bbox_inches="tight")
print("robustness_noisy_data_parameters.pdf written")
