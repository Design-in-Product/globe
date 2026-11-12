#!/usr/bin/env bash
# Build the folder that GitHub Pages uploads: every tracked file except the
# paths listed in .pages-exclude, then gate it with scripts/check_pages_refs.py.
#
# Why (2026-11-12, Claude Duet's proposal via xian, weighed by Tessera): the
# workflow uploaded the whole checkout (~809 MB); ~295 MB of it is superseded
# films and raw plate data that no page links. deploy-pages aborted twice on
# 11-10 when the sync outran its 10-min window. Staging drops the dead weight
# WITHOUT changing any URL a page uses — the gate refuses the stage if a page
# names a file the staging left out (or that never existed), so an excluded
# file cannot 404 behind a green deploy. The durable fix (films off Pages)
# stays a hosting decision for xian; this does not pre-empt it.
#
# .pages-exclude: one tracked path per line, or a folder prefix ending in "/";
# "#" comments. An entry that matches no tracked file is refused by name (the
# manifest checker's DECLARED-ABSENT, applied here: a stale line is drift).
# Portable to bash 3.2 (Amber) and 5 (ubuntu runner): no mapfile, no arrays.
# Usage: scripts/stage_pages.sh <dest>    (dest is created; must not exist)
set -euo pipefail
dest=${1:?dest folder}
cd "$(dirname "$0")/.."
[ -e "$dest" ] && { echo "stage_pages: $dest exists — refusing to stage over it" >&2; exit 2; }
excl=.pages-exclude
rules=$(grep -vE '^[[:space:]]*(#|$)' "$excl" 2>/dev/null || true)
nrules=$(printf '%s\n' "$rules" | grep -c . || true)
tracked=$(git ls-files)
[ -n "$tracked" ] || { echo "stage_pages: git ls-files printed nothing — not a checkout? (NOT OK)" >&2; exit 2; }
mkdir -p "$dest"
kept=0; dropped=0; used=$'\n'
while IFS= read -r f; do
  skip=
  while IFS= read -r r; do
    [ -n "$r" ] || continue
    if [ "$f" = "$r" ] || { [ "${r%/}" != "$r" ] && [ "${f#"$r"}" != "$f" ]; }; then used="$used$r"$'\n'; skip=1; break; fi
  done <<< "$rules"
  if [ -n "$skip" ]; then dropped=$((dropped+1)); continue; fi
  mkdir -p "$dest/$(dirname "$f")"
  cp -p "$f" "$dest/$f"
  kept=$((kept+1))
done <<< "$tracked"
stale=0
while IFS= read -r r; do
  [ -n "$r" ] || continue
  case "$used" in *$'\n'"$r"$'\n'*) ;; *) echo "stage_pages: $excl entry '$r' matches no tracked file — stale entry, fix the list (NOT OK)" >&2; stale=1 ;; esac
done <<< "$rules"
[ "$stale" = 0 ] || exit 1
echo "stage_pages: $kept files staged, $dropped excluded by $nrules rule(s); $(du -sm "$dest" | cut -f1) MB in $dest"
python3 scripts/check_pages_refs.py "$dest" || { echo "stage_pages: a page names a file that is not in the upload — refusing to stage (NOT OK)" >&2; exit 1; }
