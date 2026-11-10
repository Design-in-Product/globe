# 2026-11-10 — Tessera log

## 10:22 PT — cycle fire: brief 11-10 turned on yesterday's cure; one derivation, one registered gate test

Sync: fast-forwarded to 6d7ea68 (brief 11-10 pointer). Mail: nothing addressed to me in globe, mediajunkie or designinproduct; four new sibling memos since the 16:24 check (all designinproduct, Wedge→Themis and Wren→Janus), none mentioning Tessera or globe. Fire check at 10:22: VERDICT clean, 43 lines; Pages deployed for 6d7ea68 before I started.

Brief 11-10 (two findings, the second is mine from f56f293) applied to the code it describes:
- *A cure for hand-typed values is itself in the blast radius* (Klatch). Checked f56f293 against its own defect definition: the derivation rule `git ls-files -- 'scrubber_assets/*.json' ...` was typed by hand in the hook AND the fire check — two copies of a cure for copying — and the checker test still typed the two filenames. Now one source, `scripts/explore_manifests.sh`, read by all three (6f594c1). The checker test's live case derives its list too and fails by name on an empty derivation.
- *Register the scenario, not the one-off* (11-08, overdue here): the 11-09 empty-list proof was a throwaway clone run, never a test. `scripts/test_manifest_gate.sh` (55dffa2) builds each case against the committed hook in a no-checkout clone: derivation equals `git ls-files`; baseline undeclared asset commits; a manifest declaring a missing keyframe is refused for that reason; a **third manifest never named anywhere** is refused through the derived list; no manifest tracked → derivation prints nothing and the hook refuses "no Explore manifest"; cripple pass hand-types the two old names back and the third-manifest case then commits (the refusal was the derivation's, not a backstop). 7 passed, 0 failed, 3 s, first run. Existing suites unchanged: drain 52/52, checker 9/9.
- Handoff pointer table registers the derivation and both gate tests; header re-dated; 14 of 14 pointers consistent (5f2ec2b).

Not applicable: the Klatch uniqueness-assertion specific (no anchor census here beyond the one above).

Drain: brief 11-10 applied to its own subject (derivation single-sourced, gate test registered, handoff updated — three commits, all tests green). No other ripe work in roadmap/handoff/mail. Deferred, all blocked on xian — preview → live swap, blocker: his edit review of `previews/home-2026-10-21/`; 1:03 ghost test render, blocker: his verdict; sequel treatment, blocker: his decision; contributed-layer licence default CC BY vs BY-SA, blocker: his pick, and no outside layer exists yet.
