# Installation

## Install from PyPI

Install `pysib` with pip:

```bash
pip install pysib
```

## Requirements

`pysib` requires:

- Python >= 3.9
- NumPy
- SciPy
- Matplotlib
- LAPACK

On macOS, `pysib` links against the Accelerate framework. On Linux, it links against `liblapack`.

## Development install

For development from a local checkout, run:

```bash
pip install -e .
```

This compiles the local C extensions and installs the package in editable mode.

## Native extensions

The `oe`, `armax`, `bj`, and filtered estimators use C extensions linked against LAPACK.

The `arx`, `sm`, `correlation`, `iv`, `predict`, and `simulate` functions are implemented in Python using NumPy and SciPy.

## Verify the installation

After installation, check that the package imports correctly:

```bash
python -c "import pysib; print(pysib.__name__)"
```

For a development checkout, run the test suite with:

```bash
python3 -m pytest tests/ -v
```
