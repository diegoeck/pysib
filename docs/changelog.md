# Changelog

## v0.2.5 — 2026-10-13

Optimizer robustness release, prepared during the revision of the IFAC Journal
of Systems and Control article.

### Package

- The Gauss--Newton system of the shared C optimizer is now solved with LAPACK
  `dgelss` (minimum-norm solution through the SVD, singular values below
  machine precision treated as zero) instead of a Cholesky factorization
  (`dposv`). Singular or ill-conditioned Gauss--Newton matrices, typical of
  high-order models with clustered poles, no longer make every Gauss--Newton
  step fail. On an eighth-order benchmark the median relative simulation error
  of `oe` dropped from about 2.5% to 0.2%; estimates for well-conditioned
  problems are unchanged.
- The Gauss--Newton phase now stops when none of the ten backtracking
  candidates decreases the cost, instead of repeating the same failed step
  until the 1000-iteration budget is exhausted. Estimates are unchanged; the
  phase typically ends after 150--200 iterations.
- `oe`, `armax`, `bj` and their filtered variants issue a `RuntimeWarning`
  when a predictor polynomial of the returned model (`F` for OE, `C` for
  ARMAX, `C` and `F` for BJ) has a root on or outside the unit circle; the
  warning of the unfiltered estimators suggests the filtered variant.

### Experiments

- Added `experiments/ifac-jsc/` with the scripts, data caches, and results of
  the numerical experiments of the IFAC Journal of Systems and Control article,
  which compare `pysib` with SIPPY and pysid.

### Documentation

- Updated package, citation, and user-manual metadata to version `0.2.5`.
- Described the Gauss--Newton solver, the stopping rules, and the stability
  warning in the user manual.

### Links

- PyPI: <https://pypi.org/project/pysib/0.2.5/>
- GitHub release: <https://github.com/diegoeck/pysib/releases/tag/v0.2.5>

## v0.2.4 — 2026-07-03

CALGO artifact preparation and optimizer robustness release.

### Package

- Guarded the shared C optimizer against degenerate zero-error steps, avoiding
  NaNs when an iteration reaches an exact or nearly exact solution.

### Examples

- Added a Monte Carlo Box--Jenkins example comparing `bj` and `bj_filtered`
  on a plant with colored output noise.

### Distribution

- Updated the CALGO packaging script to include the Box--Jenkins Monte Carlo
  driver and expected output.
- Updated the CALGO package layout so article drivers include their official
  `.npz` data caches, while regular examples exclude generated result caches.
- Added a top-level CALGO artifact overview in `Doc/README.md`.

### Documentation

- Updated package, citation, and user-manual metadata to version `0.2.4`.

### Links

- PyPI: <https://pypi.org/project/pysib/0.2.4/>
- GitHub release: <https://github.com/diegoeck/pysib/releases/tag/v0.2.4>

## v0.2.3 — 2026-06-24

Filtered-estimator consistency release.

### Package

- Updated `armax_filtered` and `bj_filtered` to use the same first-order
  filtered-continuation pole schedule as `oe_filtered`.
- Updated the filtered ARMAX and BJ initial guesses to run ARX on the first
  filtered data record, matching the OE filtered workflow.
- Added a regression test that checks OE, ARMAX, and BJ filtered variants use
  the same filtered data sequence.

### Documentation

- Updated the user manual and paper drafts to describe the shared filtered
  continuation schedule.
- Updated the SYSID 2027 article draft and reproducible experiment artifacts.
- Removed the older SYSID short-paper draft and pointed the documentation site
  to the SYSID 2027 article draft.
- Set package and manuscript metadata to version `0.2.3`.

### Links

- PyPI: <https://pypi.org/project/pysib/0.2.3/>
- GitHub release: <https://github.com/diegoeck/pysib/releases/tag/v0.2.3>

## v0.2.2 — 2026-06-17

Bugfix release for the nonlinear optimizer.

### Package

- Corrected the incremental Gauss--Newton step ramp used by the shared C
  optimizer.  The final trial factor is now exactly `1.0` instead of `1.001`.

### Documentation

- Added Zenodo DOI and citation metadata.
- Updated release metadata and citation information for version `0.2.2`.
- Updated the SYSID 2027 article draft to describe the corrected
  Gauss--Newton ramp.

### Links

- PyPI: <https://pypi.org/project/pysib/0.2.2/>
- GitHub release: <https://github.com/diegoeck/pysib/releases/tag/v0.2.2>

## v0.2.1 — 2026-06-06

Documentation maintenance release.

### Documentation

- Improved the documentation landing page and site content.
- Added and refined changelog documentation.
- Split the conference and article papers into `paper-sysid` and `paper-toms` paths.
- Corrected SIB/Python attribution text.

### Infrastructure

- Updated documentation and wheel-building workflow configuration.

### Links

- PyPI: <https://pypi.org/project/pysib/0.2.1/>
- GitHub release: <https://github.com/diegoeck/pysib/releases/tag/v0.2.1>

## v0.2.0 — 2026-06-01

First public release of `pysib`.

### Package

- Published `pysib` on PyPI.
- Set package version to `0.2.0`.
- Updated package metadata, project URLs, and license metadata.

### Distribution

- Added binary wheels for macOS arm64 and Linux x86_64.
- Added GitHub Actions workflow for cross-platform wheel builds.
- Validated release artifacts with `twine check`.

### Documentation

- Expanded the MkDocs documentation at <https://pysib.net/>.
- Added user guide, estimator-selection guidance, examples, and API reference pages.
- Updated the user manual for version `0.2.0`.

### Links

- PyPI: <https://pypi.org/project/pysib/0.2.0/>
- GitHub release: <https://github.com/diegoeck/pysib/releases/tag/v0.2.0>
