#!/usr/bin/env python3
"""Explore manifest coverage: declared vs present, with the two kinds of absence
named separately.

Brief 10-26 (Klatch round 457): one ABSENT sentinel covering "never existed" and
"declared but dropped" hid the second case from drift accounting. The Explore
page is manifest-driven (scrubber_assets/keyframes.json and
future/keyframes-future.json list every keyframe the scrubber will fetch), so
there are two distinct ways a keyframe can be missing and they mean different
things:

  DECLARED-ABSENT  manifest lists a file the directory does not hold -> the live
                   page fetches a 404 and the scrubber shows a hole (NOT OK, exit 1)
  PRESENT-UNDECLARED a .webp sits in the directory no manifest references -> dead
                   weight shipped to Pages, or a keyframe that never got wired in
                   (reported, exit 0: nothing on the page breaks)

Usage: check_explore_manifest.py <manifest.json> [...]   (asset dir = manifest's dir)
Exit 0 = every declared file present; 1 = at least one declared file absent, or
NO keyframe declared at all; 2 = a manifest could not be read (unparseable, no
"keyframes" key, or keyframes not a list of objects). Each verdict names its kind.
~0.05 s, no network.

Brief 11-27 (Klatch unit-521): a size predicate reads an empty collection in
one of two directions, and "no declared file is absent" is the false-green one
— an empty keyframes list declared nothing, so nothing was absent, and the
checker printed "0 declared, 0 present ... [ok]" (driven 11-27). A manifest
with no keyframes is refused by name. Before 11-27 a non-list or a non-object
keyframe also crashed the checker with a traceback (exit 1, no label the
fire check's verdict counts); both are UNREADABLE now.
"""
import json
import os
import sys

IMAGE_EXT = {".webp", ".png", ".jpg", ".jpeg"}


def check(path):
    try:
        with open(path) as f:
            m = json.load(f)
        keys = m["keyframes"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(f"  {path}: UNREADABLE ({e.__class__.__name__}: {e}) (NOT OK)")
        return 2
    if not isinstance(keys, list) or any(not isinstance(k, dict) for k in keys):
        print(f"  {path}: UNREADABLE (keyframes must be a list of objects) (NOT OK)")
        return 2
    d = os.path.dirname(path) or "."
    on_disk = {n for n in os.listdir(d) if os.path.splitext(n)[1].lower() in IMAGE_EXT}
    if not keys:
        print(f"  {path}: EMPTY MANIFEST — 0 keyframes declared, {len(on_disk)} image(s) on disk; "
              f"Explore would load nothing from it (NOT OK)")
        return 1
    declared = [k.get("file", "") for k in keys]
    absent = [f for f in declared if not f or not os.path.isfile(os.path.join(d, f))]
    undeclared = sorted(on_disk - set(declared))
    dup = sorted({f for f in declared if declared.count(f) > 1})
    verdict = "ok" if not absent else "NOT OK"
    print(f"  {path}: {len(declared)} declared, {len(declared) - len(absent)} present, "
          f"{len(absent)} declared-absent, {len(undeclared)} present-undeclared [{verdict}]")
    for f in absent:
        print(f"    DECLARED-ABSENT: {f!r} (page will 404 at this keyframe)")
    for f in undeclared:
        print(f"    PRESENT-UNDECLARED: {f} (shipped, never fetched)")
    for f in dup:
        print(f"    DECLARED-TWICE: {f}")
    return 1 if absent else 0


def main(argv):
    if not argv:
        print("usage: check_explore_manifest.py <manifest.json> [...]", file=sys.stderr)
        return 2
    rc = 0
    for p in argv:
        rc = max(rc, check(p))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
