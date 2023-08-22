#!/usr/bin/env bash
set -euo pipefail
git pull
poetry version minor
VERSION=$(grep pyproject.toml -e '(?<=^version = ")(.*)(?=")' -Po)
echo "Commit"
git add -u
git commit -m "$VERSION"
git push -o ci.skip
echo "tag and special syntax to push the tag"
git tag "$VERSION"
git push origin "$VERSION"
