"""Summary table of the revision cases (reads revision_<case>.npz)."""
from pathlib import Path

import numpy as np

import comparators as C
from revision_cases import CASES

ROOT = Path(__file__).parent

lines = ["# Revision cases: summary\n",
         "Success: relative simulation error below 5%. Unstable: returned model with a",
         "predictor polynomial on or outside the unit circle. Failed: the estimator",
         "raised an exception (counted as unsuccessful). Time: median seconds per call.\n",
         "| case | structure | mean SNR [dB] | method | success | median error | unstable | failed | time [s] |",
         "|---|---|---|---|---|---|---|---|---|"]
for name in CASES:
    path = ROOT / f"revision_{name}.npz"
    if not path.exists():
        continue
    d = np.load(path)
    for i, method in enumerate(d["methods"]):
        r = C.summarize(d["err"][i], d["unstable"][i], d["failed"][i], d["seconds"][i])
        lines.append(f"| {name} | {d['structure']} | {d['snr_db'].mean():.1f} | {method} "
                     f"| {r['success']:.0f}% | {r['median_error']:.2e} | {r['unstable']} "
                     f"| {r['failed']} | {r['time']:.3f} |")
(ROOT / "revision_results.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
