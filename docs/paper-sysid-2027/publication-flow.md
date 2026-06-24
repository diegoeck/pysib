# SYSID 2027 publication flow

This checklist tracks the publication path for the SYSID 2027 article, the
associated `pysib` release, and later journal handling.

## 1. Freeze the software artifact

- [ ] Review the current diff and split changes into coherent commits.
- [ ] Commit the filtered-estimator code change, tests, docs, and regenerated
      paper/manual artifacts.
- [ ] Create the final release commit for `pysib` v0.2.3.
- [ ] Tag the release as `v0.2.3`.
- [ ] Build source distribution and wheels.
- [ ] Run:
      `python3.13 -m twine check dist/pysib-0.2.3*`
- [ ] Publish only the v0.2.3 artifacts:
      `python3.13 -m twine upload dist/pysib-0.2.3*`
- [ ] Create the GitHub Release from tag `v0.2.3`.
- [ ] Archive the GitHub release on Zenodo, or confirm that Zenodo has minted
      the v0.2.3 version DOI.
- [ ] If Zenodo creates a new version DOI, update `references.bib`,
      `main.tex`, and rebuild `main.pdf`.

## 2. Freeze the SYSID manuscript

- [ ] Confirm the paper cites the final package version and DOI.
- [ ] Rebuild the paper from a clean state:
      `make clean && make && pdflatex -interaction=nonstopmode main.tex`
- [ ] Confirm no unresolved references or citations remain in `main.log`.
- [ ] Confirm the final PDF is the one intended for submission.
- [ ] Create a clean submission bundle containing only required files:
      `main.tex`, `references.bib`, `main.bbl`, `ifacconf_latex/ifacconf.cls`,
      `ifacconf_latex/ifacconf.bst`, and the used PDF figures.

## 3. arXiv preprint

- [ ] Decide the arXiv category, likely `eess.SY` with possible `cs.MS`
      cross-listing.
- [ ] Prepare a source archive, not just a PDF, unless there is a reason to use
      PDF-only submission.
- [ ] Include the custom IFAC class/style files and all figures used by the
      manuscript.
- [ ] Include `references.bib` and/or the generated `main.bbl`.
- [ ] Exclude auxiliary files, logs, old PDFs, unused figures, and experiment
      data files.
- [ ] Upload to arXiv and inspect the generated PDF before final submission.
- [ ] After announcement, record the arXiv ID.
- [ ] Add the arXiv ID to the GitHub Release notes, documentation, and later
      journal/conference cover letters if useful.

## 4. SYSID submission

- [ ] Wait for the official SYSID 2027 call/submission page and verify:
      page limit, template, journal-option instructions, deadlines, anonymity
      rules, and whether arXiv preprints are explicitly allowed.
- [ ] If the SYSID version differs from the arXiv version, create a submission
      branch or tagged archive for the exact submitted version.
- [ ] Upload the required PDF/source package through the official submission
      system.
- [ ] Save the submitted PDF and submission confirmation in local records.
- [ ] Track reviews and required revisions.

## 5. Journal option / IFAC Journal of Systems and Control

- [ ] Confirm the exact journal-option workflow from SYSID 2027 instructions.
- [ ] Check whether the journal version should be identical to the SYSID
      manuscript or expanded after review.
- [ ] Disclose the arXiv preprint in the cover letter if required.
- [ ] Update the arXiv record with journal reference and DOI after acceptance.
- [ ] Update `pysib.net`, README, changelog, and citation metadata after final
      publication.

## Current local status

- `pysib` has been bumped locally to v0.2.3.
- Local v0.2.3 sdist and one macOS CPython 3.13 wheel have been built.
- `twine check` passed locally.
- The package has not yet been uploaded to PyPI.
- The release tag and GitHub Release have not yet been created.
- The arXiv, SYSID, and journal submissions have not yet been made.
