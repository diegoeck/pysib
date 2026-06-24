#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: scripts/create-github-release-draft.sh <tag>" >&2
  echo "Example: scripts/create-github-release-draft.sh v0.2.3" >&2
  exit 2
fi

tag="$1"
version="${tag#v}"
artifact_dir="release-artifacts/${tag}"

if [ ! -d "$artifact_dir" ]; then
  echo "Missing ${artifact_dir}; download artifacts first." >&2
  exit 1
fi

notes_file="$(mktemp)"
awk -v version="$version" '
  $0 ~ "^## v" version " " { print; in_section=1; next }
  in_section && /^## v/ { exit }
  in_section { print }
' docs/changelog.md > "$notes_file"

if [ ! -s "$notes_file" ]; then
  echo "Could not extract release notes for ${tag} from docs/changelog.md" >&2
  rm -f "$notes_file"
  exit 1
fi

gh release create "$tag" "${artifact_dir}"/*/* \
  --draft \
  --title "pysib ${tag}" \
  --notes-file "$notes_file"

rm -f "$notes_file"
