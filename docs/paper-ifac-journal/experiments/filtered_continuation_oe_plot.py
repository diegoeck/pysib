"""Load Monte Carlo results and generate statistics + error histogram."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

ROOT = Path(__file__).parent

data = np.load(ROOT / "filtered_continuation_oe.npz")
T_oe    = data["T_oe"]
T_filt  = data["T_filt"]
T_sippy = data["T_sippy"]
B_SIM  = data["B_SIM"]
F_SIM  = data["F_SIM"]
u      = data["u"]
y0     = data["y0"]
y_run0 = data["y_run0"]
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

errors_oe    = np.empty(M)
errors_filt  = np.empty(M)
# errors_sippy = np.empty(M)

for i in range(M):
    m_oe    = make_model(T_oe[:, i])
    m_filt  = make_model(T_filt[:, i])
    # m_sippy = make_model(T_sippy[:, i])

    yh_oe    = pysib.simulate(u, m_oe)
    yh_filt  = pysib.simulate(u, m_filt)
    # yh_sippy = pysib.simulate(u, m_sippy)

    errors_oe[i]    = np.linalg.norm(y0 - yh_oe)    / np.linalg.norm(y0)
    errors_filt[i]  = np.linalg.norm(y0 - yh_filt)  / np.linalg.norm(y0)
    # errors_sippy[i] = np.linalg.norm(y0 - yh_sippy) / np.linalg.norm(y0)

print("Simulation errors computed")

# --- Markdown output -----------------------------------------------------------

success_oe    = np.mean(errors_oe    < THRESHOLD)
success_filt  = np.mean(errors_filt  < THRESHOLD)
# success_sippy = np.mean(errors_sippy < THRESHOLD)

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
# lines.append(
#     f"| Sippy | {errors_sippy.mean():.6e}"
#     f" | {errors_sippy.std(ddof=1):.6e} | {100*success_sippy:.1f}\\% |"
# )

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
# counts_sippy, _ = np.histogram(errors_sippy, bins=bins)

ax = axes[0]
ax.bar(centers - w/2, counts_oe,   width=w, color="steelblue", alpha=0.85)
ax.bar(centers + w/2, counts_filt, width=w, color="tomato",     alpha=0.85)
# ax.bar(centers + w, counts_sippy, width=w, color="mediumseagreen", alpha=0.85)
ax.axvline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax.set_title("Simulation error distribution")
ax.set_xlabel("relative simulation error")
ax.set_ylabel("count")

ax = axes[1]
bp = ax.boxplot(
    [errors_oe, errors_filt],
    tick_labels=["OE", "OE filtered"],
    patch_artist=True,
    widths=0.5,
)
bp["boxes"][0].set_facecolor("steelblue")
bp["boxes"][1].set_facecolor("tomato")
# bp["boxes"][2].set_facecolor("mediumseagreen")
ax.axhline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax.set_title("Simulation error spread")
ax.set_ylabel("relative simulation error")

fig.suptitle(
    f"Effect of filtered continuation (M={M}, N={N}, noise std={NOISE_STD})",
)
fig.tight_layout()
fig.legend(
    handles=[
        mpatches.Patch(facecolor="steelblue", label="OE"),
        mpatches.Patch(facecolor="tomato",     label="OE filtered"),
        # mpatches.Patch(facecolor="mediumseagreen", label="Sippy"),
    ],
    loc="lower center", ncol=2, frameon=False,
    bbox_to_anchor=(0.5, -0.02),
)
fig.subplots_adjust(bottom=0.18)
fig.savefig(ROOT / "filtered_continuation_oe_errors.pdf", bbox_inches="tight")
print("filtered_continuation_oe_errors.pdf written")

# --- Separated error figures (histogram + boxplot) ---------------------------

# Histogram only
fig_h, ax_h = plt.subplots(figsize=(6, 4))
ax_h.bar(centers - w/2, counts_oe,   width=w, color="steelblue", alpha=0.85)
ax_h.bar(centers + w/2, counts_filt, width=w, color="tomato",     alpha=0.85)
ax_h.axvline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax_h.set_xlabel("relative simulation error")
ax_h.set_ylabel("count")
fig_h.legend(
    handles=[
        mpatches.Patch(facecolor="steelblue", label="OE"),
        mpatches.Patch(facecolor="tomato",     label="OE filtered"),
    ],
    loc="upper right", ncol=1, frameon=False,
)
fig_h.tight_layout()
fig_h.savefig(ROOT / "filtered_continuation_oe_errors_hist.pdf", bbox_inches="tight")
print("filtered_continuation_oe_errors_hist.pdf written")

# Boxplot only
fig_b, ax_b = plt.subplots(figsize=(4, 4))
bp2 = ax_b.boxplot(
    [errors_oe, errors_filt],
    tick_labels=["OE", "OE filtered"],
    patch_artist=True,
    widths=0.5,
)
bp2["boxes"][0].set_facecolor("steelblue")
bp2["boxes"][1].set_facecolor("tomato")
ax_b.axhline(THRESHOLD, color="k", linestyle="--", linewidth=1)
ax_b.set_ylabel("relative simulation error")
fig_b.tight_layout()
fig_b.savefig(ROOT / "filtered_continuation_oe_errors_box.pdf", bbox_inches="tight")
print("filtered_continuation_oe_errors_box.pdf written")

# --- Parameter histogram -------------------------------------------------------

NB_hist   = T_oe.shape[0] - (len(F_SIM) - 1)
true_vals = [B_SIM[1]] + list(F_SIM[1:])
labels    = ["$b_1$"] + [f"$f_{i}$" for i in range(1, len(F_SIM))]

n_params = len(labels)
fig2, axes2 = plt.subplots(2, 2, figsize=(8, 7))
axes2 = axes2.flatten()

for ax, lbl, tv, idx in zip(axes2, labels, true_vals, range(n_params)):
    all_vals = np.concatenate([T_oe[idx], T_filt[idx]])
    # all_vals = np.concatenate([T_oe[idx], T_filt[idx], T_sippy[idx]])
    lo   = np.nanmin(all_vals)
    hi   = np.nanmax(all_vals)
    spread = hi - lo
    if spread < abs(np.nanmean(all_vals)) * 1e-4 + 1e-6:
        mid = (lo + hi) / 2
        spread = max(abs(mid) * 0.1, 0.1)
        lo, hi = mid - spread / 2, mid + spread / 2
    bins = np.linspace(lo, hi, 20)
    w    = (bins[1] - bins[0]) / 2
    centers = (bins[:-1] + bins[1:]) / 2

    counts_oe,   _ = np.histogram(T_oe[idx],   bins=bins)
    counts_filt, _ = np.histogram(T_filt[idx], bins=bins)
    # counts_sippy, _ = np.histogram(T_sippy[idx], bins=bins)

    ax.bar(centers - w/2, counts_oe,   width=w, color="steelblue", alpha=0.85)
    ax.bar(centers + w/2, counts_filt, width=w, color="tomato",     alpha=0.85)
    # ax.bar(centers + w, counts_sippy, width=w, color="mediumseagreen", alpha=0.85)
    ax.axvline(tv, color="k", linestyle="--", linewidth=1)
    ax.set_title(lbl)
    ax.set_xlabel("value")
    if idx % 2 == 0:
        ax.set_ylabel("count")

fig2.suptitle(f"Effect of filtered continuation (M={M}, N={N}, noise std={NOISE_STD})")
fig2.tight_layout()
fig2.legend(
    handles=[
        mpatches.Patch(facecolor="steelblue", label="OE"),
        mpatches.Patch(facecolor="tomato",     label="OE filtered"),
        # mpatches.Patch(facecolor="mediumseagreen", label="Sippy"),
    ],
    loc="lower center", ncol=2, frameon=False,
    bbox_to_anchor=(0.5, -0.02),
)
fig2.subplots_adjust(bottom=0.18)
fig2.savefig(ROOT / "filtered_continuation_oe_parameters.pdf", bbox_inches="tight")
print("filtered_continuation_oe_parameters.pdf written")

# --- Time-domain figure (run 0) ------------------------------------------------

yh_oe   = pysib.simulate(u, make_model(T_oe[:,   0]))
yh_filt = pysib.simulate(u, make_model(T_filt[:, 0]))
# yh_sippy = pysib.simulate(u, make_model(T_sippy[:, 0]))

t = np.arange(N)
fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(t, y_run0,  color="gray",      linewidth=0.7, alpha=0.5,  label="Noisy")
ax3.plot(t, y0,      color="k",         linewidth=1.5,             label="True")
ax3.plot(t, yh_oe,   color="steelblue", linewidth=1,   linestyle="--", label="OE")
ax3.plot(t, yh_filt, color="tomato",    linewidth=1,   linestyle="--", label="OE filtered")
# ax3.plot(t, yh_sippy, color="mediumseagreen", linewidth=1, linestyle="--", label="Sippy")
ax3.set_xlabel("time step")
ax3.set_ylabel("output")
ax3.set_title(f"Simulated outputs — run 1 (noise std={NOISE_STD})")
ax3.legend(frameon=False)
fig3.tight_layout()
fig3.savefig(ROOT / "filtered_continuation_oe_timeseries.pdf", bbox_inches="tight")
print("filtered_continuation_oe_timeseries.pdf written")
