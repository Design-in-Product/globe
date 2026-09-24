# Tessera Session Log — 2026-09-24

## 10:22 PT — Duty-cycle fire (scheduled, first daily firing)

Sync: `globe` fast-forwarded `a932ef9` → `a87c069` (day's brief only);
`mediajunkie` and `designinproduct` clean. **Mail: nothing new addressed
to Tessera in any of the three** (listed newest-first, filtered). No
first-look feedback on `/explore/` yet.

## Brief 9/24 applied to my own tooling — and it found something

Three findings; finding 2 (Klatch Round 262) landed directly: *"an arm
never shown to go red is consistent with an arm that cannot."* The only
automated check `/explore/` gets is the `node --check` harness I'd been
running ad hoc — and I had never shown it capable of failing. Tested it
three arms:

- **A** real page → pass.
- **B** injected syntax error → **fail**, so the check is real, not vacuous.
- **C** extraction yields nothing → **pass**. *That's the hole.*
  `node --check` on an empty file succeeds, so if the extraction regex
  ever stopped matching (an added attribute, a quote-style change), the
  harness would have printed "syntax OK" having checked zero lines.

Same silent-fallback class as the July ASS-overlay incident, where a
`try/except` shipped a film with no overlay and reported success. Worth
noting the harness had been *correct* every time I ran it — the defect
was latent, reachable only by editing the page's script tag. Exactly the
kind of thing that surfaces when you test the instrument instead of
trusting its output.

**Fixed** (`adacf68`): promoted to `scripts/check_explore_syntax.py` with
a `MIN_CHARS` guard, and distinct exit codes so extraction failure (2)
and guard trip (3) can never be read as a pass (0).

**One more instance, self-inflicted:** the first draft was bash, and it
died of a bash-3.2 heredoc-inside-command-substitution parse error —
**while exiting 0**. A checker that breaks and reports success is the
precise failure it exists to prevent; caught it because I re-ran all
three arms against the new script rather than assuming a rewrite of a
verified design stays verified. Rewrote in Python: no shell quoting,
explicit exits. All three arms re-verified against the final version
(0 / 1 / 2).

**Otherwise a no-op fire.** Explore still awaiting xian's first look
(orientation, mobile load, the 1200→1000 Ma ghost-slide); the Pard
provisioning thread still his call to nudge or close.
