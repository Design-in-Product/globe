# 2026-10-20 — Tessera log

## 10:22 fire

Sync: `13c19e9` (brief pointer). Mail: nothing new. `fire_check.sh`: site and /explore/ 200, Pages deployed for `13c19e9`, no stray Blender, no live declarations. Brief 10-20 read from the hub clone: Klatch's SDK-bump assessment — "zero declared breaking changes" is not a safe signal when the call site casts away the type and the tests mock the library. No equivalent here (no SDK, no mocked suite; Blender 5.1.2 and the venv are pinned and exercised by real renders). Its aside, a changelog regex that silently missed the `## [x.y.z](…)` heading variant, is the same drift lesson as 10-19, already applied to the drain guard.

Second cut still staged in `review-2/` for xian (since 10-17 10:44).

Drain: health check, brief read and checked. Deferred: ship + old-frame clearance (blocker: xian has not watched the second cut in motion); crossfade decision (blocker: xian's call). Two clean mail checks (10:22, 10:25).

## 16:22 fire

Sync: up to date at `b19fbae`. Mail: nothing new. `fire_check.sh`: site and /explore/ 200, Pages deployed for `b19fbae`, no stray Blender, no live declarations. Second cut still staged in `review-2/` for xian (since 10-17 10:44).

Drain: health check only; nothing else unblocked. Deferred: ship + old-frame clearance (blocker: xian has not watched the second cut in motion); crossfade decision (blocker: xian's call). Two clean mail checks (16:22, 16:23).

## 16:51 — xian in session: second cut approved and SHIPPED (heading time from the ship commit's clock; first written as an estimate)

xian, from kindbook, after watching all six films: "I love all six of these. Bravo!" That is the human viewing the rule waited on, so: merged `origin/palette-cobalt-brass` into main (`2332bbe`, clean, 83 files: theme, FILMS v8/v3 refs, "Reading the films", poster, ramped Explore keyframes); copied the six films from `review-2/` (sha1 identical to the pipeline outputs and to what xian watched) plus `poster_v8.png` into the repo root; pushed `a5779f7` (GitHub's >50 MB warning on `tectonic_flat_v8.mp4`, 95.8 MB — under the 100 MB limit; pushed as watched, not re-encoded). `wait_pages.py`: deployed for `a5779f7` in 75 s. HEAD on all nine URLs (index, poster, six films, /explore/) → 200 with content-length equal to the local bytes. Roadmap items 4 and 6 → SHIPPED 2026-10-20 (items 2 and 3 note v3); handoff updated; memory updated.

Open with xian, not objected to: the faint 1:03 crossfade copy stays as shipped since v7 unless he asks. Pard told: shipped, and the old frame sets I intend to delete (list in the memo); deleting waits on his ack.

Drain: ship complete and proven live; docs/memory/log updated; Pard told. Deferred: deleting `review-1/`, `stale-1/` (9.1 GB) and the earth-tone render sets (blocker: Pard's ack, per the tell-before-deleting rule); nothing else on the roadmap is in flight (items 7/8 someday/maybe until xian says).

## 17:05 — mail wake: Pard's ack on the frame sets; two corrections

Pard acked deleting `stale-1/` (9.1 GB), `render_frames_v7/` (4.8 GB) and `review-1/` (278 MB) after checking that nothing on Amber references them, and noted my memo was stamped 17:14 yet arrived before 17:01. Both true. The stamp was an estimate, not `date`; the ship entry's heading above was likewise a guess and is now set from the ship commit's clock. Memory written (`timestamps-from-the-clock`).

Worse: I replied "done" in the same breath as the `rm -rf`, and the session's permission policy denied the `rm`. Nothing was deleted; free space unchanged at 88 GB. Correction memo sent to Pard at once (`…correction-not-deleted-yet-rm-denied…`, mediajunkie `5ed48be`). xian is in session and is asked to run the removal by hand; I report to Pard only after `df` shows it.

The drain guard refused this very commit: a fixed heading shows in the diff as an added `## ` line with no added body, which the guard read as an entry without a Drain line. Fixed in `check_drain.sh` (a heading with no added body is a rename, not an entry) with three new test cases, 32/32 pass.

Drain: Pard's ack read; both corrections sent; memory and log fixed. Guard false positive on heading edits fixed and tested. Deferred: the deletion itself (blocker: `rm -rf` is denied for this seat; waits on xian running it); telling Pard the space is back (blocker: the deletion).
