#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: scripts/check-release-artifacts.sh <tag>" >&2
  echo "Example: scripts/check-release-artifacts.sh v0.2.3" >&2
  exit 2
fi

tag="$1"
artifact_dir="release-artifacts/${tag}"

if [ ! -d "$artifact_dir" ]; then
  echo "Missing ${artifact_dir}; download artifacts first." >&2
  exit 1
fi

python -m twine check "${artifact_dir}"/*/*
