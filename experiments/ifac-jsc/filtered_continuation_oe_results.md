# Effect of filtered continuation

M = 100, N = 1000, NOISE\_STD = 30.0

| method | mean error | std error | success rate (< 5%) | unstable F | largest root modulus | median time per call [s] |
|--------|------------|-----------|---------------------|------------|----------------------|--------------------------|
| OE | 5.685361e-02 | 4.365901e-02 | 60.0\% | 39 | 1.0034 | 0.2188 |
| OE filtered | 2.174056e-02 | 7.943141e-03 | 100.0\% | 0 | 0.9284 | 1.3563 |
| SIPPY | 9.632990e-02 | 3.810772e-02 | 15.0\% | 0 | 0.9984 | 0.0855 |
| pysid | 1.194936e-01 | 1.019783e-01 | 36.0\% | 49 | 1.0034 | 0.0109 |

OE: 39 unstable estimates, 39 of them unsuccessful; 1 stable unsuccessful estimates.