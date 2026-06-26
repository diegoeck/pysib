# SYSID 2027 publication flow

This checklist tracks the publication path for the SYSID 2027 article, the
associated `pysib` release, and later journal handling.

## 1. Freeze the software artifact

- [x] Review the current diff and split changes into coherent commits.
- [x] Commit the filtered-estimator code change, tests, docs, and regenerated
      paper/manual artifacts.
- [x] Create the final release commit for `pysib` v0.2.3.
- [x] Tag the release as `v0.2.3`.
- [x] Build source distribution and wheels through GitHub Actions.
- [x] Download official GitHub Actions artifacts to `release-artifacts/v0.2.3/`.
- [x] Run `scripts/check-release-artifacts.sh v0.2.3`.
- [x] Publish only the official v0.2.3 artifacts to PyPI.
- [x] Create the GitHub Release from tag `v0.2.3`.
- [x] Confirm Zenodo DOI metadata used by the manuscript.

## 2. Freeze the SYSID manuscript

- [x] Confirm the paper cites the final package version and DOI.
- [x] Rebuild the paper from a clean state:
      `make clean && make && pdflatex -interaction=nonstopmode main.tex`
- [x] Confirm no unresolved references or citations remain in `main.log`.
- [x] Confirm the final PDF is the one intended for submission.
- [x] Create a clean arXiv submission bundle containing only required files:
      `main.tex`, `references.bib`, `main.bbl`, `ifacconf_latex/ifacconf.cls`,
      `ifacconf_latex/ifacconf.bst`, and the used PDF figures.

## 3. arXiv preprint

- [x] Decide the arXiv category, likely `eess.SY` with possible `cs.MS`
      cross-listing.
- [x] Prepare a source archive, not just a PDF, unless there is a reason to use
      PDF-only submission.
- [x] Include the custom IFAC class/style files and all figures used by the
      manuscript.
- [x] Include `references.bib` and/or the generated `main.bbl`.
- [x] Exclude auxiliary files, logs, old PDFs, unused figures, and experiment
      data files.
- [x] Upload to arXiv and inspect the generated PDF before final submission.
- [x] After announcement, record the arXiv ID: `2606.26376`.
- [x] Add the arXiv ID to the GitHub Release notes, documentation, and later
      journal/conference cover letters if useful.

## 4. SYSID submission

- [x] Wait for the official SYSID 2027 call/submission page and verify:
      page limit, template, journal-option instructions, deadlines, anonymity
      rules, and whether arXiv preprints are explicitly allowed.
- [x] If the SYSID version differs from the arXiv version, create a submission
      branch or tagged archive for the exact submitted version.
- [x] Upload the required PDF/source package through the official submission
      system.
- [x] Save the submitted PDF and submission confirmation in local records.
- [ ] Track reviews and required revisions.

## 5. Journal option / IFAC Journal of Systems and Control

- [x] Confirm the exact journal-option workflow from SYSID 2027 instructions.
- [x] Check whether the journal version should be identical to the SYSID
      manuscript or expanded after review.
- [x] Create a separate journal submission version under
      `docs/paper-ifac-journal/`.
- [x] Prepare title page, cover letter, highlights, and manuscript PDF.
- [x] Disclose the arXiv preprint and SYSID submission number 5 in the cover
      letter.
- [x] Submit to IFAC Journal of Systems and Control.
- [ ] Update the arXiv record with journal reference and DOI after acceptance.
- [ ] Update `pysib.net`, README, changelog, and citation metadata after final
      publication.

## Current local status

- `pysib` v0.2.3 has been released on PyPI and GitHub.
- arXiv preprint: <https://arxiv.org/abs/2606.26376>.
- SYSID submission completed; submission number: `5`.
- IFAC Journal of Systems and Control submission completed.
- Next tracked action: wait for reviews / editorial decision.
