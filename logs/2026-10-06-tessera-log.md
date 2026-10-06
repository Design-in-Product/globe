# Tessera Session Log — 2026-10-06

## 10:22 PT — Duty-cycle fire (scheduled)

Sync pulled the 10/06 brief; otherwise clean. **No mail addressed to
Tessera**; **no answer to the two 🔒 decisions** anywhere in the three
repos since yesterday's escalation to Janus (tight grep, own mail
excluded). Health green: brief age 0 d, site 200, Pages built, hook live,
no stray Blender, 0 live CPU declarations.

**Brief 10/06, both findings audited against this repo.**

Finding 1 (macOS `sed -i -E` silently takes `-E` as a backup suffix, runs
BRE, exits 0): no `sed -i` in any tracked script; no `*-E` / `*-i`
artefacts tracked or untracked. Clean.

Finding 2 (a CI health check that hardcodes one workflow name is a
coverage claim for one file; derive the list and print the denominator):
**this one I had.** Three HTML pages carry inline scripts
(`index.html`, `explore/index.html`, `previews/scrubber-spike/index.html`);
the pre-commit gate covered exactly one path, and the checker's regex
matched only `type="module"` — so `index.html`'s classic script, the JS
that drives the live hero and the film chaining, **had no gate at all**.
A syntax error there would have shipped the landing page broken while
every check I run said green.

Fixed, structurally: the checker now extracts every inline `<script>`
block (module or classic, skipping `src=` includes and non-JS types),
checks each, and prints the denominator ("3 script block(s) across 3
page(s)"); the hook gates every staged `.html`, not a hardcoded path;
`fire_check.sh` passes `git ls-files "*.html"` rather than defaulting to
one page. **Proven before trusted:** real run 3/3 OK; a deliberate break
in `index.html`'s classic script → checker exit 1 and the hook refuses
the commit; tree restored (0 staged lines).

Same shape as the 9/28 rollup undercount and the 10/02 deploy poll: an
instrument that measured one thing and read as "the site." The lesson
that keeps paying is the denominator — say what was checked, and derive
that list from the thing itself.

**Postscript, 10:35 — a slow Pages build, recorded rather than glossed.**
The "Pages built" in the 10:22 health block was the *pre-push* check
(`3e0d2d6`). The push of `6c59b74` registered a build at 10:24 that sat
in `building` ~11 min against a 20–93 s norm; `wait_pages.py` timed out
at 300 s (exit 2, its honest code — not "built"). Ruled out my side
first: `.nojekyll` still on origin/main, the commit touched four script/
log files. A 25-min background waiter saw it reach **built at 10:35**,
live `/explore/` 200. GitHub-side slowness, transient; nothing to fix.
Worth having: the wait script's timeout is a state, not a failure, and I
didn't write "built" until it was.
