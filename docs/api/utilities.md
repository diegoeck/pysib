# Utilities

This page summarizes utility functions exposed by `pysib`.

## `pysib.plota`

```python
Torg = pysib.plota(T, a)
```

Plots Monte-Carlo parameter estimates ordered by one selected parameter.

Parameters:

- `T`: parameter estimate matrix with shape `(n_params, n_runs)`.
- `a`: row index used for sorting, using Python's zero-based indexing.

Returns:

- `Torg`: sorted parameter matrix with shape `(n_params, n_runs)`.

The function also creates a Matplotlib plot of the sorted parameter estimates.

## Example

```python
Torg = pysib.plota(T, a=0)
```

This sorts the Monte-Carlo runs by the first parameter and plots all parameter trajectories in that sorted order.
