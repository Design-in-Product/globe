#!/usr/bin/env python3
"""Per-fire depth signal for Tessera's duty cycle.

Built 2026-09-25 in response to cross-pollination brief 9/25, finding 2
(Pard, measuring Klatch's fleet): three scheduled seats fell to ~1/5 of
their normal output over two days while *every* fire still reported `ok`
with exit code 0. "A fire mechanism that checks completion cannot see
depth." Same mechanism, same host, same exposure here.

The honest problem with my own logs as a depth surface: a log entry is a
self-report. A shallow fire that skipped its checks writes the same words
as a thorough one — "no-op, nothing new" is indistinguishable either way.
So this rollup deliberately pairs the self-report against something I
cannot write my way around:

    claimed  — fires I said I ran   (log headings)
    actual   — commits that landed, and lines changed  (git, objective)

A collapse shows up as claimed fires continuing while actual churn goes
flat — exactly Pard's signature, visible the day it starts rather than in
retrospect. It does NOT prove depth: a no-op day is legitimately flat.
It makes the *pattern* legible; the reader still judges.

Usage:  python3 scripts/fire_rollup.py [days]
"""
import collections
import re
import subprocess
import sys
from datetime import date, timedelta

LOG_DIR = "logs"
FIRE_HEADING = re.compile(r"^##\s+.*duty-cycle fire", re.I | re.M)
NOOP = re.compile(r"\*\*(?:genuine )?no-op", re.I)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def churn_by_day(since):
    """Objective: commits and lines changed per day, from git, excluding
    the brief deliveries Janus pushes (not my work)."""
    out = git("log", f"--since={since}", "--date=short",
              "--pretty=format:@%ad %an %s", "--numstat")
    days = collections.defaultdict(lambda: {"commits": 0, "lines": 0})
    day = None
    for line in out.splitlines():
        if line.startswith("@"):
            day, author = line[1:].split(" ", 1)[0], line
            mine = "briefs: cross-pollination" not in author
            if mine:
                days[day]["commits"] += 1
            day = day if mine else None
        elif day and line.strip():
            parts = line.split("\t")
            if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
                days[day]["lines"] += int(parts[0]) + int(parts[1])
    return days


def fires_by_day(days_back):
    """Claimed: fire headings found in each day's session log."""
    claimed = {}
    for i in range(days_back):
        d = (date.today() - timedelta(days=i)).isoformat()
        try:
            text = open(f"{LOG_DIR}/{d}-tessera-log.md").read()
        except FileNotFoundError:
            continue
        claimed[d] = {"fires": len(FIRE_HEADING.findall(text)),
                      "noops": len(NOOP.findall(text))}
    return claimed


def main(days_back=14):
    since = (date.today() - timedelta(days=days_back)).isoformat()
    churn, claimed = churn_by_day(since), fires_by_day(days_back)
    all_days = sorted(set(churn) | set(claimed), reverse=True)

    print(f"{'date':<12}{'fires':>6}{'no-op':>7}{'commits':>9}{'lines':>8}   note")
    print("-" * 64)
    for d in all_days:
        c = churn.get(d, {"commits": 0, "lines": 0})
        f = claimed.get(d, {"fires": 0, "noops": 0})
        note = ""
        if f["fires"] and not c["commits"]:
            note = "fires logged but NOTHING COMMITTED — investigate"
        elif c["commits"] and not f["fires"] and d in claimed:
            note = "work without a logged fire (interactive session?)"
        elif not f["fires"] and d not in claimed:
            note = "no session log for this day"
        elif f["fires"] and f["fires"] == f["noops"]:
            note = "all fires no-op"
        print(f"{d:<12}{f['fires']:>6}{f['noops']:>7}{c['commits']:>9}"
              f"{c['lines']:>8}   {note}")

    print("\nclaimed = what I logged; commits/lines = what git recorded "
          "(brief deliveries excluded).")
    print("A quality collapse looks like: fires steady, commits and lines "
          "flat across days that\nweren't genuinely quiet. Flat alone is not "
          "proof of shallowness — read the log entries.")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 14)
