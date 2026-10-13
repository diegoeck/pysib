# Experiments of the IFAC Journal of Systems and Control article

Scripts and results of the numerical experiments in

> D. Eckhard, *pysib: An Open-Source Python Toolbox for SISO Polynomial System
> Identification*, submitted to IFAC Journal of Systems and Control
> (revised version, manuscript IFACSC-D-26-00656).

All results were obtained with `pysib` v0.2.5. Each experiment compares
`pysib`, its filtered variant, SIPPY (`sippy_unipi` 1.0.1, default options) and
pysid 0.1.1 on Monte Carlo data with fixed random seeds.

## Requirements

```
pip install pysib==0.2.5 sippy_unipi==1.0.1 pysid==0.1.1 matplotlib
```

pysid 0.1.1 passes 2-D arrays to `scipy.linalg.toeplitz`, which SciPy 1.17 and
later treat as a batch; `comparators.py` applies a one-line shim that restores
the 1-D behavior. SIPPY is run in a separate process because its IPOPT/MUMPS
back end occasionally crashes with a segmentation fault; such a crash counts as
a failed SIPPY run.

## Files

| Script | Article | Output |
|---|---|---|
| `robustness_noisy_data.py`, `robustness_noisy_data_plot.py` | Sec. 5.1, Tables 5–6, Fig. 1 | `robustness_noisy_data.npz`, `robustness_noisy_data_results.md` |
| `filtered_continuation_oe.py`, `filtered_continuation_oe_plot.py` | Sec. 5.2, Table 7, Fig. 2 | `filtered_continuation_oe.npz`, `filtered_continuation_oe_results.md` |
| `revision_cases.py <case> ...`, `revision_summary.py` | Sec. 5.3, Tables 8–9 | `revision_<case>.npz`, `revision_results.md` |
| `armax_noise_models.py` | Sec. 5.3 (ARMAX noise models) | `armax_noise_models_results.md` |
| `scaling_n.py` | Sec. 5.4, Table 10 | `scaling_n.npz`, `scaling_n_results.md` |
| `comparators.py` | common adapters and metrics | — |

The cases of `revision_cases.py` are `bj1`, `bj2`, `armax`, `prbs` and `motor`
(the eighth-order power-system model). Computing times depend on the machine;
the article reports times measured sequentially on an Apple M4.

Example:

```
python robustness_noisy_data.py && python robustness_noisy_data_plot.py
python revision_cases.py bj1 bj2 armax prbs motor && python revision_summary.py
```
