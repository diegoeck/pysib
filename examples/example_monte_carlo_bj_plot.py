"""Monte-Carlo plots: load BJ results from mc_results_bj.npz and plot."""
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

import pysib


data = np.load(Path(__file__).parent / "mc_results_bj.npz")
T_bj = data["T_bj"]
T_filt = data["T_filt"]
snr_db = data["snr_db"]
B_SIM = data["B_SIM"]
C_SIM = data["C_SIM"]
D_SIM = data["D_SIM"]
F_SIM = data["F_SIM"]
NB = int(data["NB"])
NC = int(data["NC"])
ND = int(data["ND"])
NF = int(data["NF"])
M = int(data["M"])

true_vals = (
    list(B_SIM[1:1 + NB])
    + list(C_SIM[1:1 + NC])
    + list(D_SIM[1:1 + ND])
    + list(F_SIM[1:1 + NF])
)
labels = (
    [f"b{i+1}" for i in range(NB)]
    + [f"c{i+1}" for i in range(NC)]
    + [f"d{i+1}" for i in range(ND)]
    + [f"f{i+1}" for i in range(NF)]
)


def print_summary(name, estimates):
    """Print a compact Monte-Carlo summary table."""
    mean = np.nanmean(estimates, axis=1)
    std = np.nanstd(estimates, axis=1, ddof=1) if estimates.shape[1] > 1 else np.zeros(estimates.shape[0])
    bias = mean - true_vals
    rmse = np.sqrt(np.nanmean((estimates - np.asarray(true_vals)[:, None]) ** 2, axis=1))

    print(f"\n{name}")
    print("param    true       mean       bias        std       rmse")
    for label, true, mean_i, bias_i, std_i, rmse_i in zip(labels, true_vals, mean, bias, std, rmse):
        print(f"{label:>5} {true:9.4f} {mean_i:10.4f} {bias_i:10.4f} {std_i:10.4f} {rmse_i:10.4f}")


print(f"Monte-Carlo BJ summary ({M} runs)")
print(f"mean SNR: {np.nanmean(snr_db):.1f} dB")
print_summary("BJ", T_bj)
print_summary("BJ filtered", T_filt)

# --- plota (spread) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
plt.sca(ax1)
pysib.plota(T_bj, a=0)
ax1.set_title("BJ (standard)")
plt.sca(ax2)
pysib.plota(T_filt, a=0)
ax2.set_title("BJ filtered")
fig.suptitle(f"Monte-Carlo BJ ({M} runs, mean SNR {np.nanmean(snr_db):.1f} dB)")
plt.tight_layout()
plt.show()

# --- histograms side by side ---
n_params = len(labels)
ncols = 3
nrows = int(np.ceil(n_params / ncols))
fig2, axes = plt.subplots(nrows, ncols, figsize=(12, 3.2 * nrows))
axes = np.atleast_1d(axes).ravel()

for i, (ax, label, true) in enumerate(zip(axes, labels, true_vals)):
    all_vals = np.concatenate([T_bj[i], T_filt[i]])
    lo = np.nanmin(all_vals)
    hi = np.nanmax(all_vals)
    if np.isclose(lo, hi):
        lo -= 0.5
        hi += 0.5
    bins = np.linspace(lo, hi, 200)
    w = (bins[1] - bins[0]) / 2

    counts_bj, _ = np.histogram(T_bj[i], bins=bins)
    counts_filt, _ = np.histogram(T_filt[i], bins=bins)
    centers = (bins[:-1] + bins[1:]) / 2

    ax.bar(centers - w / 2, counts_bj, width=w, color="steelblue")
    ax.bar(centers + w / 2, counts_filt, width=w, color="tomato")
    ax.axvline(true, color="k", linestyle="--", linewidth=1, label=f"true={true:.3f}")
    ax.set_title(label)
    ax.set_xlabel("value")
    ax.legend(fontsize=8)

for ax in axes[n_params:]:
    ax.axis("off")

fig2.legend(
    handles=[
        mpatches.Patch(facecolor="steelblue", label="BJ"),
        mpatches.Patch(facecolor="tomato", label="BJ filtered"),
    ],
    loc="upper center",
    ncol=2,
    frameon=False,
)
fig2.suptitle(f"Histogram: BJ vs BJ filtered ({M} runs)", y=1.02)
plt.tight_layout()
plt.show()
