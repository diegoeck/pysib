"""Monte-Carlo statistics and plots for the BJ example."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter

import pysib


ROOT = Path(__file__).parent

data = np.load(ROOT / "mc_results_bj.npz")
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
NZ = int(data["NZ"])
M = int(data["M"])
N = int(data["N"])

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


def make_model(theta):
    """Build a pysib model dictionary from a BJ parameter vector."""
    return {
        "A": np.array([1.0]),
        "B": np.concatenate((np.zeros(NZ), theta[:NB])),
        "C": np.concatenate(([1.0], theta[NB:NB + NC])),
        "D": np.concatenate(([1.0], theta[NB + NC:NB + NC + ND])),
        "F": np.concatenate(([1.0], theta[NB + NC + ND:])),
    }


def summary_rows(name, estimates):
    """Return parameter-summary rows for a Monte Carlo matrix."""
    true = np.asarray(true_vals)
    mean = np.nanmean(estimates, axis=1)
    std = np.nanstd(estimates, axis=1, ddof=1)
    bias = mean - true
    rmse = np.sqrt(np.nanmean((estimates - true[:, None]) ** 2, axis=1))
    return [
        (name, label, true_i, mean_i, bias_i, std_i, rmse_i)
        for label, true_i, mean_i, bias_i, std_i, rmse_i
        in zip(labels, true, mean, bias, std, rmse)
    ]


def print_summary(name, estimates):
    """Print a compact Monte-Carlo summary table."""
    print(f"\n{name}")
    print("param    true       mean       bias        std       rmse")
    for _, label, true, mean_i, bias_i, std_i, rmse_i in summary_rows(name, estimates):
        print(
            f"{label:>5} {true:9.4f} {mean_i:10.4f} {bias_i:10.4f}"
            f" {std_i:10.4f} {rmse_i:10.4f}"
        )


t = np.arange(N)
u = (
    np.sin(2 * np.pi * t / 18)
    + np.sin(2 * np.pi * t / 28)
    + np.sin(2 * np.pi * t / 61)
)
y0 = lfilter(B_SIM, F_SIM, u)
errors_bj = np.empty(M)
errors_filt = np.empty(M)

for run in range(M):
    y_bj = pysib.simulate(u, make_model(T_bj[:, run]))
    y_filt = pysib.simulate(u, make_model(T_filt[:, run]))
    errors_bj[run] = np.linalg.norm(y0 - y_bj) / np.linalg.norm(y0)
    errors_filt[run] = np.linalg.norm(y0 - y_filt) / np.linalg.norm(y0)

success_bj = np.mean(errors_bj < 0.05)
success_filt = np.mean(errors_filt < 0.05)


print(f"Monte-Carlo BJ summary ({M} runs)")
print(f"mean SNR: {np.nanmean(snr_db):.1f} dB")
print_summary("BJ", T_bj)
print_summary("BJ filtered", T_filt)
print("\nrelative simulation error")
print("method        mean       std     success(<5%)")
print(
    f"BJ       {errors_bj.mean():10.6f} {errors_bj.std(ddof=1):9.6f}"
    f" {100 * success_bj:10.1f}%"
)
print(
    f"BJ filt. {errors_filt.mean():10.6f} {errors_filt.std(ddof=1):9.6f}"
    f" {100 * success_filt:10.1f}%"
)

lines = []
lines.append("# Box-Jenkins filtered continuation\n")
lines.append(f"M = {M}, N = {N}, mean SNR = {np.nanmean(snr_db):.1f} dB\n")
lines.append("## Relative simulation error\n")
lines.append("| method | mean error | std error | success rate (< 5%) |")
lines.append("|--------|------------|-----------|---------------------|")
lines.append(
    f"| BJ | {errors_bj.mean():.6e} | {errors_bj.std(ddof=1):.6e}"
    f" | {100 * success_bj:.1f}\\% |"
)
lines.append(
    f"| BJ filtered | {errors_filt.mean():.6e}"
    f" | {errors_filt.std(ddof=1):.6e} | {100 * success_filt:.1f}\\% |"
)
lines.append("\n## Parameter estimates\n")
lines.append("| method | parameter | true | mean | bias | std | rmse |")
lines.append("|--------|-----------|------|------|------|-----|------|")
for row in summary_rows("BJ", T_bj) + summary_rows("BJ filtered", T_filt):
    method, label, true, mean_i, bias_i, std_i, rmse_i = row
    lines.append(
        f"| {method} | ${label}$ | {true:.8f} | {mean_i:.8f}"
        f" | {bias_i:.8f} | {std_i:.8f} | {rmse_i:.8f} |"
    )

with open(ROOT / "example_monte_carlo_bj_results.md", "w") as f:
    f.write("\n".join(lines))

print("\nexample_monte_carlo_bj_results.md written")

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
fig.savefig(ROOT / "example_monte_carlo_bj_spread.pdf", bbox_inches="tight")
print("example_monte_carlo_bj_spread.pdf written")

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
fig2.savefig(ROOT / "example_monte_carlo_bj_parameters.pdf", bbox_inches="tight")
print("example_monte_carlo_bj_parameters.pdf written")
