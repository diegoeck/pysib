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

# (label, parameter matrix, seconds per call, color)
METHODS = [
    ("SM",    data["T_sm"],    data["SEC_sm"],    "steelblue"),
    ("OE",    data["T_oe"],    data["SEC_oe"],    "tomato"),
    ("SIPPY", data["T_sippy"], data["SEC_sippy"], "mediumseagreen"),
    ("pysid", data["T_pysid"], data["SEC_pysid"], "orchid"),
]


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

errors = {
    name: np.array([np.linalg.norm(y0 - pysib.simulate(u, make_model(T[:, i])))
                    / np.linalg.norm(y0) for i in range(M)])
    for name, T, _, _ in METHODS
}

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

lines.append("\n## OE-structure estimates\n")
lines.append("| method | parameter | mean | std |")
lines.append("|--------|-----------|------|-----|")
oe_labels = ["$b_1$", "$f_1$", "$f_2$", "$f_3$"]
for name, T, _, _ in METHODS:
    for i, label in enumerate(oe_labels):
        lines.append(f"| {name} | {label} | {np.mean(T[i, :]):.8f} | {np.std(T[i, :], ddof=1):.8f} |")

lines.append("\n## Simulation errors and computing time\n")
lines.append("| method | mean error | std error | success rate (< 5%) | unstable F | largest root modulus | median time per call [s] |")
lines.append("|--------|------------|-----------|---------------------|------------|----------------------|--------------------------|")
for name, T, sec, _ in METHODS:
    errs = errors[name]
    roots = np.array([np.max(np.abs(np.roots(np.r_[1.0, T[NB:, i]]))) for i in range(M)])
    lines.append(
        f"| {name} | {errs.mean():.6e} | {errs.std(ddof=1):.6e}"
        f" | {100*np.mean(errs < THRESHOLD):.1f}\\% | {int(np.sum(roots >= 1))}"
        f" | {roots.max():.4f} | {np.median(sec):.4f} |"
    )

with open(ROOT / "robustness_noisy_data_results.md", "w") as f:
    f.write("\n".join(lines))

print("robustness_noisy_data_results.md written")

legend = [mpatches.Patch(facecolor=c, label=name) for name, _, _, c in METHODS]
K = len(METHODS)


def grouped_bars(ax, series, bins):
    """Side-by-side histogram bars, one group per bin."""
    w = (bins[1] - bins[0]) / K
    centers = (bins[:-1] + bins[1:]) / 2
    for k, (values, color) in enumerate(series):
        counts, _ = np.histogram(values, bins=bins)
        ax.bar(centers + (k - (K - 1) / 2) * w, counts, width=w, color=color, alpha=0.85)

# --- Figure --------------------------------------------------------------------

true_vals = [B_SIM[1]] + list(F_SIM[1:])
labels    = ["$b_1$"] + [f"$f_{i}$" for i in range(1, len(F_SIM))]

fig, axes = plt.subplots(2, 2, figsize=(8, 7))
axes = axes.flatten()

for idx, (ax, lbl, tv) in enumerate(zip(axes, labels, true_vals)):
    all_vals = np.concatenate([T[idx] for _, T, _, _ in METHODS])
    lo   = np.nanmin(all_vals)
    hi   = np.nanmax(all_vals)
    spread = hi - lo
    if spread < abs(np.nanmean(all_vals)) * 1e-4 + 1e-6:
        mid = (lo + hi) / 2
        spread = max(abs(mid) * 0.1, 0.1)
        lo, hi = mid - spread / 2, mid + spread / 2
    grouped_bars(ax, [(T[idx], c) for _, T, _, c in METHODS], np.linspace(lo, hi, 20))
    ax.axvline(tv, color="k", linestyle="--", linewidth=1)
    ax.set_title(lbl)
    ax.set_xlabel("value")
    if idx % 2 == 0:
        ax.set_ylabel("count")

fig.suptitle(f"Robustness under noisy data (M={M}, N={N}, noise std={NOISE_STD})")
fig.tight_layout()
fig.legend(handles=legend, loc="lower center", ncol=K, frameon=False,
           bbox_to_anchor=(0.5, -0.02))
fig.subplots_adjust(bottom=0.18)
fig.savefig(ROOT / "robustness_noisy_data_parameters.pdf", bbox_inches="tight")
print("robustness_noisy_data_parameters.pdf written")

# --- Time-domain figure (run 0) ------------------------------------------------

t = np.arange(N)
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(t, y_run0, color="gray", linewidth=0.7, alpha=0.5, label="Noisy")
ax2.plot(t, y0,     color="k",    linewidth=1.5, label="True")
for name, T, _, color in METHODS:
    ax2.plot(t, pysib.simulate(u, make_model(T[:, 0])), color=color, linewidth=1,
             label=name, linestyle="--")
ax2.set_xlabel("time step")
ax2.set_ylabel("output")
ax2.set_title(f"Simulated outputs — run 1 (noise std={NOISE_STD})")
ax2.legend(frameon=False)
fig2.tight_layout()
fig2.savefig(ROOT / "robustness_noisy_data_timeseries.pdf", bbox_inches="tight")
print("robustness_noisy_data_timeseries.pdf written")

# --- Error histogram + boxplot -------------------------------------------------

lo = min(e.min() for e in errors.values())
hi = max(e.max() for e in errors.values())
if hi - lo < 1e-10:
    mid = (lo + hi) / 2
    lo, hi = mid - 0.05, mid + 0.05
bins = np.linspace(lo, hi, 25)
series = [(errors[name], c) for name, _, _, c in METHODS]


def boxplot(ax):
    bp = ax.boxplot([errors[name] for name, _, _, _ in METHODS],
                    tick_labels=[name for name, _, _, _ in METHODS],
                    patch_artist=True, widths=0.5)
    for box, (_, _, _, c) in zip(bp["boxes"], METHODS):
        box.set_facecolor(c)
    ax.axhline(THRESHOLD, color="k", linestyle="--", linewidth=1)


fig3, axes3 = plt.subplots(1, 2, figsize=(10, 4))
grouped_bars(axes3[0], series, bins)
axes3[0].axvline(THRESHOLD, color="k", linestyle="--", linewidth=1)
axes3[0].set_title("Simulation error distribution")
axes3[0].set_xlabel("relative simulation error")
axes3[0].set_ylabel("count")
boxplot(axes3[1])
axes3[1].set_title("Simulation error spread")
axes3[1].set_ylabel("relative simulation error")
fig3.suptitle(f"Robustness under noisy data (M={M}, N={N}, noise std={NOISE_STD})")
fig3.tight_layout()
fig3.legend(handles=legend, loc="lower center", ncol=K, frameon=False,
            bbox_to_anchor=(0.5, -0.02))
fig3.subplots_adjust(bottom=0.18)
fig3.savefig(ROOT / "robustness_noisy_data_errors.pdf", bbox_inches="tight")
print("robustness_noisy_data_errors.pdf written")

# --- Separated error figures (histogram + boxplot) ---------------------------

fig_h, ax_h = plt.subplots(figsize=(6, 4))
grouped_bars(ax_h, series, bins)
ax_h.axvline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax_h.set_xlabel("relative simulation error")
ax_h.set_ylabel("count")
fig_h.legend(handles=legend, loc="upper right", ncol=1, frameon=False)
fig_h.tight_layout()
fig_h.savefig(ROOT / "robustness_noisy_data_errors_hist.pdf", bbox_inches="tight")
print("robustness_noisy_data_errors_hist.pdf written")

fig_b, ax_b = plt.subplots(figsize=(4, 4))
boxplot(ax_b)
ax_b.set_ylabel("relative simulation error")
fig_b.tight_layout()
fig_b.savefig(ROOT / "robustness_noisy_data_errors_box.pdf", bbox_inches="tight")
print("robustness_noisy_data_errors_box.pdf written")
