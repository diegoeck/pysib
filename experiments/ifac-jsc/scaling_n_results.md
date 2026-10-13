# Scaling with the data length (nonconvex OE benchmark)

M = 20 records per length, sigma_v = 30.0

| N | gradient-phase outer iterations (of 100) | Gauss-Newton iterations (of 1000) | pysib: success / median time [s] | pysib filtered: success / median time [s] | SIPPY: success / median time [s] | pysid: success / median time [s] |
|---|---|---|---|---|---|---|
| 500 | 100-100 (median 100) | 160-200 (median 175) | 65% / 0.109 | 95% / 0.905 | 10% / 0.042 | 35% / 0.006 |
| 1000 | 100-100 (median 100) | 160-200 (median 170) | 45% / 0.220 | 100% / 0.927 | 5% / 0.080 | 25% / 0.011 |
| 2000 | 100-100 (median 100) | 160-200 (median 170) | 40% / 0.447 | 100% / 1.192 | 15% / 0.174 | 25% / 0.026 |
| 5000 | 100-100 (median 100) | 160-210 (median 170) | 60% / 1.451 | 100% / 2.564 | 0% / 1.274 | 30% / 0.195 |
| 10000 | 100-100 (median 100) | 160-220 (median 170) | 60% / 3.016 | 100% / 4.983 | 0% / 1.860 | 30% / 0.677 |
