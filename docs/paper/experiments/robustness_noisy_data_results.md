# Robustness under noisy data

M = 500, N = 500, NOISE\_STD = 0.1

## True OE parameters

| parameter | value |
|-----------|-------|
| $b_1$ | 1.00000000 |
| $f_1$ | -1.10000000 |
| $f_2$ | 0.26250000 |

## OE-structure estimates (SM and OE)

| method | parameter | mean | std |
|--------|-----------|------|-----|
| SM | $b_1$ | 1.00035237 | 0.00436880 |
| SM | $f_1$ | -1.09972652 | 0.00382553 |
| SM | $f_2$ | 0.26226868 | 0.00330754 |
| OE | $b_1$ | 1.00028169 | 0.00437836 |
| OE | $f_1$ | -1.09978869 | 0.00383730 |
| OE | $f_2$ | 0.26232151 | 0.00331758 |

## ARX baseline parameters (not directly comparable to OE parameters)

| parameter | mean | std |
|-----------|------|-----|
| $\theta_{1}$ | -0.96402559 | 0.01213341 |
| $\theta_{2}$ | 0.14247447 | 0.01069840 |
| $\theta_{3}$ | 1.15416775 | 0.01383448 |