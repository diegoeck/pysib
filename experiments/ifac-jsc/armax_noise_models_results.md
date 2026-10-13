# Local minima of the ARMAX criterion

Success: relative simulation error below 5% (out of 100). Trapped: final cost
above that of the reference minimizer found from the true parameters.

| C roots | variance | SNR [dB] | reference success | pysib success / trapped | pysid success / trapped |
|---|---|---|---|---|---|
| -0.50 | 900 | 8.9 | 57 | 57 / 0 | 57 / 0 |
| -0.50 | 10000 | -1.5 | 8 | 8 / 0 | 8 / 0 |
| -0.90 | 900 | 8.9 | 57 | 57 / 0 | 57 / 0 |
| -0.90 | 10000 | -1.5 | 8 | 8 / 0 | 8 / 0 |
| 0.90 | 900 | 8.8 | 42 | 42 / 0 | 42 / 0 |
| 0.90 | 10000 | -1.7 | 4 | 4 / 0 | 4 / 0 |
| 0.80+0.41j, 0.80-0.41j | 900 | 8.9 | 61 | 61 / 0 | 61 / 0 |
| 0.80+0.41j, 0.80-0.41j | 10000 | -1.5 | 10 | 10 / 1 | 10 / 0 |
| 0.90, -0.90 | 900 | 8.8 | 44 | 44 / 0 | 43 / 1 |
| -0.90, -0.80 | 900 | 8.9 | 59 | 59 / 0 | 57 / 3 |
| 0.50, -0.50 | 900 | 8.9 | 52 | 52 / 0 | 52 / 0 |
| 0.30, 0.20 | 900 | 8.9 | 53 | 53 / 0 | 53 / 0 |
| 0.90, 0.80 | 900 | 8.7 | 65 | 19 / 69 | 31 / 52 |
| 0.95, 0.70 | 900 | 8.7 | 56 | 23 / 57 | 23 / 57 |

## ARMAX case of revision_cases.py

SNR 8.7 dB, reference success 64
| method | success | trapped |
|---|---|---|
| pysib | 21 | 71 |
| pysib filtered | 64 | 0 |
| pysid | 25 | 58 |
