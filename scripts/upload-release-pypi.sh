#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: scripts/upload-release-pypi.sh <tag>" >&2
  echo "Example: scripts/upload-release-pypi.sh v0.2.3" >&2
  exit 2
fi

tag="$1"
artifact_dir="release-artifacts/${tag}"

if [ ! -d "$artifact_dir" ]; then
  echo "Missing ${artifact_dir}; download artifacts first." >&2
  exit 1
fi

echo "Uploading official GitHub Actions artifacts from ${artifact_dir}"
python -m twine upload "${artifact_dir}"/*/*
