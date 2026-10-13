# Revision cases: summary

Success: relative simulation error below 5%. Unstable: returned model with a
predictor polynomial on or outside the unit circle. Failed: the estimator
raised an exception (counted as unsuccessful). Time: median seconds per call.

| case | structure | mean SNR [dB] | method | success | median error | unstable | failed | time [s] |
|---|---|---|---|---|---|---|---|---|
| bj1 | BJ | 8.7 | pysib | 41% | 1.08e-01 | 52 | 0 | 0.566 |
| bj1 | BJ | 8.7 | pysib filtered | 97% | 2.44e-02 | 0 | 0 | 5.568 |
| bj1 | BJ | 8.7 | SIPPY | 8% | 1.04e-01 | 6 | 0 | 0.305 |
| bj1 | BJ | 8.7 | pysid | 0% | nan | 0 | 100 | 0.007 |
| bj2 | BJ | 8.7 | pysib | 55% | 1.46e-02 | 45 | 0 | 0.671 |
| bj2 | BJ | 8.7 | pysib filtered | 100% | 9.89e-03 | 12 | 0 | 6.615 |
| bj2 | BJ | 8.7 | SIPPY | 11% | 1.05e-01 | 27 | 0 | 0.667 |
| bj2 | BJ | 8.7 | pysid | 0% | nan | 0 | 100 | 0.003 |
| armax | ARMAX | 8.7 | pysib | 21% | 1.39e-01 | 28 | 0 | 0.376 |
| armax | ARMAX | 8.7 | pysib filtered | 64% | 4.44e-02 | 0 | 0 | 3.695 |
| armax | ARMAX | 8.7 | SIPPY | 0% | 2.38e-01 | 91 | 0 | 0.019 |
| armax | ARMAX | 8.7 | pysid | 25% | 1.31e-01 | 23 | 0 | 0.038 |
| prbs | OE | 8.7 | pysib | 100% | 2.18e-02 | 0 | 0 | 0.240 |
| prbs | OE | 8.7 | pysib filtered | 100% | 2.18e-02 | 0 | 0 | 0.823 |
| prbs | OE | 8.7 | SIPPY | 8% | 1.04e-01 | 4 | 0 | 0.081 |
| prbs | OE | 8.7 | pysid | 91% | 2.31e-02 | 0 | 0 | 0.034 |
| motor | OE | 101.2 | pysib | 100% | 1.91e-03 | 0 | 0 | 0.409 |
| motor | OE | 101.2 | pysib filtered | 100% | 1.88e-03 | 0 | 0 | 0.531 |
| motor | OE | 101.2 | SIPPY | 88% | 5.40e-05 | 15 | 0 | 0.682 |
| motor | OE | 101.2 | pysid | 100% | 4.37e-03 | 0 | 0 | 0.014 |
