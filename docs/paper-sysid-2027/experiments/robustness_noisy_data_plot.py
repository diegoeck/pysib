"""Load Monte Carlo results and generate statistics + parameter histogram."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

import pysib

ROOT = Path(__file__).parent

data = np.load(ROOT / "robustness_noisy_data.npz")
T_sm    = data["T_sm"]
T_oe    = data["T_oe"]
T_sippy = data["T_sippy"]
B_SIM = data["B_SIM"]
F_SIM = data["F_SIM"]
u      = data["u"]
y0     = data["y0"]
y_run0 = data["y_run0"]
NB    = int(data["NB"])
NF    = int(data["NF"])
NZ    = int(data["NZ"])
M     = int(data["M"])
N     = int(data["N"])
NOISE_STD = float(data["NOISE_STD"])


def make_model(theta):
    return {
        "A": np.array([1.0]),
        "B": np.concatenate((np.zeros(NZ), theta[:NB])),
        "C": np.array([1.0]),
        "D": np.array([1.0]),
        "F": np.concatenate(([1.0], theta[NB:])),
    }

# --- Simulation errors ---------------------------------------------------------

THRESHOLD = 0.05

errors_sm    = np.empty(M)
errors_oe    = np.empty(M)
errors_sippy = np.empty(M)

for i in range(M):
    errors_sm[i]    = np.linalg.norm(y0 - pysib.simulate(u, make_model(T_sm[:,    i]))) / np.linalg.norm(y0)
    errors_oe[i]    = np.linalg.norm(y0 - pysib.simulate(u, make_model(T_oe[:,    i]))) / np.linalg.norm(y0)
    errors_sippy[i] = np.linalg.norm(y0 - pysib.simulate(u, make_model(T_sippy[:, i]))) / np.linalg.norm(y0)

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

lines.append("\n## OE-structure estimates (SM, OE, and Sippy)\n")
lines.append("| method | parameter | mean | std |")
lines.append("|--------|-----------|------|-----|")
oe_labels = ["$b_1$", "$f_1$", "$f_2$", "$f_3$"]
for method_name, matrix in [("SM", T_sm), ("OE", T_oe), ("Sippy", T_sippy)]:
    for i, label in enumerate(oe_labels):
        mean = np.mean(matrix[i, :])
        std  = np.std(matrix[i, :], ddof=1)
        lines.append(f"| {method_name} | {label} | {mean:.8f} | {std:.8f} |")

lines.append("\n## Simulation errors\n")
lines.append("| method | mean error | std error | success rate (< 5%) |")
lines.append("|--------|------------|-----------|---------------------|")
for method_name, errs in [("SM", errors_sm), ("OE", errors_oe), ("Sippy", errors_sippy)]:
    lines.append(
        f"| {method_name} | {errs.mean():.6e} | {errs.std(ddof=1):.6e}"
        f" | {100*np.mean(errs < THRESHOLD):.1f}\\% |"
    )

with open(ROOT / "robustness_noisy_data_results.md", "w") as f:
    f.write("\n".join(lines))

print("robustness_noisy_data_results.md written")

# --- Figure --------------------------------------------------------------------

NB = T_sm.shape[0] - (len(F_SIM) - 1)
true_vals = [B_SIM[1]] + list(F_SIM[1:])
labels    = ["$b_1$"] + [f"$f_{i}$" for i in range(1, len(F_SIM))]

n_params = len(labels)
fig, axes = plt.subplots(2, 2, figsize=(8, 7))
axes = axes.flatten()

for ax, lbl, tv, idx in zip(axes, labels, true_vals, range(n_params)):
    all_vals = np.concatenate([T_sm[idx], T_oe[idx], T_sippy[idx]])
    lo   = np.nanmin(all_vals)
    hi   = np.nanmax(all_vals)
    spread = hi - lo
    if spread < abs(np.nanmean(all_vals)) * 1e-4 + 1e-6:
        mid = (lo + hi) / 2
        spread = max(abs(mid) * 0.1, 0.1)
        lo, hi = mid - spread / 2, mid + spread / 2
    bins = np.linspace(lo, hi, 20)
    w    = (bins[1] - bins[0]) / 3
    centers = (bins[:-1] + bins[1:]) / 2

    counts_sm,    _ = np.histogram(T_sm[idx],    bins=bins)
    counts_oe,    _ = np.histogram(T_oe[idx],    bins=bins)
    counts_sippy, _ = np.histogram(T_sippy[idx], bins=bins)

    ax.bar(centers - w, counts_sm,    width=w, color="steelblue",    alpha=0.85)
    ax.bar(centers,     counts_oe,    width=w, color="tomato",        alpha=0.85)
    ax.bar(centers + w, counts_sippy, width=w, color="mediumseagreen", alpha=0.85)
    ax.axvline(tv, color="k", linestyle="--", linewidth=1)
    ax.set_title(lbl)
    ax.set_xlabel("value")
    if idx % 2 == 0:
        ax.set_ylabel("count")

fig.suptitle(f"Robustness under noisy data (M={M}, N={N}, noise std={NOISE_STD})")
fig.tight_layout()
fig.legend(
    handles=[
        mpatches.Patch(facecolor="steelblue",      label="SM"),
        mpatches.Patch(facecolor="tomato",          label="OE"),
        mpatches.Patch(facecolor="mediumseagreen",  label="Sippy"),
    ],
    loc="lower center", ncol=3, frameon=False,
    bbox_to_anchor=(0.5, -0.02),
)
fig.subplots_adjust(bottom=0.18)
fig.savefig(ROOT / "robustness_noisy_data_parameters.pdf", bbox_inches="tight")
print("robustness_noisy_data_parameters.pdf written")

# --- Time-domain figure (run 0) ------------------------------------------------

yh_sm    = pysib.simulate(u, make_model(T_sm[:,    0]))
yh_oe    = pysib.simulate(u, make_model(T_oe[:,    0]))
yh_sippy = pysib.simulate(u, make_model(T_sippy[:, 0]))

t = np.arange(N)
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(t, y_run0,   color="gray",           linewidth=0.7, alpha=0.5,     label="Noisy")
ax2.plot(t, y0,       color="k",              linewidth=1.5, label="True")
ax2.plot(t, yh_sm,    color="steelblue",      linewidth=1,   label="SM",    linestyle="--")
ax2.plot(t, yh_oe,    color="tomato",         linewidth=1,   label="OE",    linestyle="--")
ax2.plot(t, yh_sippy, color="mediumseagreen", linewidth=1,   label="Sippy", linestyle="--")
ax2.set_xlabel("time step")
ax2.set_ylabel("output")
ax2.set_title(f"Simulated outputs — run 1 (noise std={NOISE_STD})")
ax2.legend(frameon=False)
fig2.tight_layout()
fig2.savefig(ROOT / "robustness_noisy_data_timeseries.pdf", bbox_inches="tight")
print("robustness_noisy_data_timeseries.pdf written")

# --- Error histogram + boxplot -------------------------------------------------

fig3, axes3 = plt.subplots(1, 2, figsize=(10, 4))

lo = min(errors_sm.min(), errors_oe.min(), errors_sippy.min())
hi = max(errors_sm.max(), errors_oe.max(), errors_sippy.max())
spread = hi - lo
if spread < 1e-10:
    mid = (lo + hi) / 2
    lo, hi = mid - 0.05, mid + 0.05
bins = np.linspace(lo, hi, 25)
w = (bins[1] - bins[0]) / 3
centers = (bins[:-1] + bins[1:]) / 2

counts_sm,    _ = np.histogram(errors_sm,    bins=bins)
counts_oe,    _ = np.histogram(errors_oe,    bins=bins)
counts_sippy, _ = np.histogram(errors_sippy, bins=bins)

ax = axes3[0]
ax.bar(centers - w, counts_sm,    width=w, color="steelblue",     alpha=0.85)
ax.bar(centers,     counts_oe,    width=w, color="tomato",         alpha=0.85)
ax.bar(centers + w, counts_sippy, width=w, color="mediumseagreen", alpha=0.85)
ax.axvline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax.set_title("Simulation error distribution")
ax.set_xlabel("relative simulation error")
ax.set_ylabel("count")

ax = axes3[1]
bp = ax.boxplot(
    [errors_sm, errors_oe, errors_sippy],
    tick_labels=["SM", "OE", "Sippy"],
    patch_artist=True,
    widths=0.5,
)
bp["boxes"][0].set_facecolor("steelblue")
bp["boxes"][1].set_facecolor("tomato")
bp["boxes"][2].set_facecolor("mediumseagreen")
ax.axhline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax.set_title("Simulation error spread")
ax.set_ylabel("relative simulation error")

fig3.suptitle(f"Robustness under noisy data (M={M}, N={N}, noise std={NOISE_STD})")
fig3.tight_layout()
fig3.legend(
    handles=[
        mpatches.Patch(facecolor="steelblue",     label="SM"),
        mpatches.Patch(facecolor="tomato",         label="OE"),
        mpatches.Patch(facecolor="mediumseagreen", label="Sippy"),
    ],
    loc="lower center", ncol=3, frameon=False,
    bbox_to_anchor=(0.5, -0.02),
)
fig3.subplots_adjust(bottom=0.18)
fig3.savefig(ROOT / "robustness_noisy_data_errors.pdf", bbox_inches="tight")
print("robustness_noisy_data_errors.pdf written")

# --- Separated error figures (histogram + boxplot) ---------------------------

# Histogram only
fig_h, ax_h = plt.subplots(figsize=(6, 4))
ax_h.bar(centers - w, counts_sm,    width=w, color="steelblue",     alpha=0.85)
ax_h.bar(centers,     counts_oe,    width=w, color="tomato",         alpha=0.85)
ax_h.bar(centers + w, counts_sippy, width=w, color="mediumseagreen", alpha=0.85)
ax_h.axvline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax_h.set_xlabel("relative simulation error")
ax_h.set_ylabel("count")
fig_h.legend(
    handles=[
        mpatches.Patch(facecolor="steelblue",     label="SM"),
        mpatches.Patch(facecolor="tomato",         label="OE"),
        mpatches.Patch(facecolor="mediumseagreen", label="Sippy"),
    ],
    loc="upper right", ncol=1, frameon=False,
)
fig_h.tight_layout()
fig_h.savefig(ROOT / "robustness_noisy_data_errors_hist.pdf", bbox_inches="tight")
print("robustness_noisy_data_errors_hist.pdf written")

# Boxplot only
fig_b, ax_b = plt.subplots(figsize=(4, 4))
bp2 = ax_b.boxplot(
    [errors_sm, errors_oe, errors_sippy],
    tick_labels=["SM", "OE", "Sippy"],
    patch_artist=True,
    widths=0.5,
)
bp2["boxes"][0].set_facecolor("steelblue")
bp2["boxes"][1].set_facecolor("tomato")
bp2["boxes"][2].set_facecolor("mediumseagreen")
ax_b.axhline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax_b.set_ylabel("relative simulation error")
fig_b.tight_layout()
fig_b.savefig(ROOT / "robustness_noisy_data_errors_box.pdf", bbox_inches="tight")
print("robustness_noisy_data_errors_box.pdf written")
