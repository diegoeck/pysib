#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: scripts/download-release-artifacts.sh <tag> <github-run-id>" >&2
  echo "Example: scripts/download-release-artifacts.sh v0.2.3 28126144565" >&2
  exit 2
fi

tag="$1"
run_id="$2"
dest="release-artifacts/${tag}"

if [ -e "$dest" ]; then
  echo "Refusing to overwrite existing ${dest}" >&2
  echo "Move or remove it first if you really want to redownload." >&2
  exit 1
fi

mkdir -p "$dest"
gh run download "$run_id" --dir "$dest"
find "$dest" -type f | sort
