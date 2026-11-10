#!/usr/bin/env bash
# The ONE place the Explore manifest list is derived. Prints every tracked
# scrubber_assets/**/*.json, one per line, read from the git index (so a
# manifest staged for the first time is included). Prints nothing when none is
# tracked — the caller must name that case (brief 11-09: an empty derived list
# is a new branch; brief 11-10, Klatch: the rule was typed by hand in the hook
# AND the fire check, two copies of a cure for copying — a cure is in the blast
# radius of the defect it fixes).
# Usage: manifests=$(bash scripts/explore_manifests.sh)
cd "$(dirname "$0")/.."
git ls-files -- 'scrubber_assets/*.json' 'scrubber_assets/**/*.json' | sort -u
