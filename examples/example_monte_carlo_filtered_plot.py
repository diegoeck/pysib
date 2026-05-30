"""Monte-Carlo plots: load results from mc_results.npz and plot."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import pysib

data  = np.load(Path(__file__).parent / "mc_results.npz")
T_oe   = data["T_oe"]
T_filt = data["T_filt"]
B_SIM  = data["B_SIM"]
F_SIM  = data["F_SIM"]
NB     = int(data["NB"])
NF     = int(data["NF"])
M      = int(data["M"])

true_vals = [B_SIM[1]] + list(F_SIM[1:])
labels    = ["b"] + [f"f{i+1}" for i in range(NF)]

# --- plota (spread) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
plt.sca(ax1); pysib.plota(T_oe,   a=0); ax1.set_title("OE (standard)")
plt.sca(ax2); pysib.plota(T_filt, a=0); ax2.set_title("OE filtered")
fig.suptitle(f"Monte-Carlo ({M} runs)")
plt.tight_layout()
plt.show()

# --- histogramas lado a lado ---
fig2, axes = plt.subplots(2, 2, figsize=(10, 7))
axes = axes.ravel()
for i, (ax, lbl, tv) in enumerate(zip(axes, labels, true_vals)):
    all_vals = np.concatenate([T_oe[i], T_filt[i]])
    lo   = np.nanmin(all_vals)
    hi   = np.nanmax(all_vals)
    bins = np.linspace(lo, hi, 200)
    w    = (bins[1] - bins[0]) / 2

    counts_oe,   _ = np.histogram(T_oe[i],   bins=bins)
    counts_filt, _ = np.histogram(T_filt[i], bins=bins)
    centers = (bins[:-1] + bins[1:]) / 2

    ax.bar(centers - w/2, counts_oe,   width=w, color="steelblue")
    ax.bar(centers + w/2, counts_filt, width=w, color="tomato")
    ax.axvline(tv, color="k", linestyle="--", linewidth=1, label=f"true={tv:.3f}")
    ax.set_title(lbl)
    ax.set_xlabel("value")
    ax.legend(fontsize=8)

fig2.legend(handles=[mpatches.Patch(facecolor="steelblue", label="OE"),
                     mpatches.Patch(facecolor="tomato",    label="OE filtered")],
            loc="upper center", ncol=2, frameon=False)
fig2.suptitle(f"Histogram: OE vs OE filtered ({M} runs)", y=1.02)
plt.tight_layout()
plt.show()
