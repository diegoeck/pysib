# Release workflow

This repository treats GitHub Actions artifacts as the release source of truth.
Local `dist/` builds are useful for smoke tests, but should not be uploaded to
PyPI unless a release is intentionally being made without Actions.

## One-time rule

Use one staging directory per tag:

```bash
release-artifacts/vX.Y.Z/
```

Do not mix artifacts from different versions in the same directory. The
`release-artifacts/` directory is ignored by Git.

## Normal release

1. Update version metadata, changelog, documentation, and PDFs.
2. Run the focused checks from `AGENTS.md`.
3. Commit the release changes.
4. Tag the commit:

```bash
git tag vX.Y.Z
git push origin main
git push origin vX.Y.Z
```

5. Wait for the `Build wheels` GitHub Actions run for that tag to pass.
6. Download the official artifacts:

```bash
scripts/download-release-artifacts.sh vX.Y.Z <github-run-id>
```

7. Check the downloaded artifacts:

```bash
scripts/check-release-artifacts.sh vX.Y.Z
```

8. Upload the checked artifacts to PyPI:

```bash
TWINE_USERNAME=__token__ TWINE_PASSWORD="$PYPI_TOKEN" scripts/upload-release-pypi.sh vX.Y.Z
```

9. Create a draft GitHub Release:

```bash
scripts/create-github-release-draft.sh vX.Y.Z
```

10. Confirm PyPI links and publish the GitHub Release draft.

## Current v0.2.3 state

The tag `v0.2.3` has been pushed and the GitHub Actions wheel build passed.
The official artifacts were downloaded to:

```bash
release-artifacts/v0.2.3/
```

They passed:

```bash
python3.13 -m twine check release-artifacts/v0.2.3/*/*
```

PyPI upload still needs credentials or Trusted Publishing.
