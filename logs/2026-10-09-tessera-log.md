# Tessera log — 2026-10-09

## 10:00 PT — Mail wake: xian says yes to the Actions deploy

Janus relaying xian: "Yes, Tessera's plan is good" — switch Pages to the
Actions artifact deploy (`build_type=workflow`); do everything I can; write
up the steps that need his hands; not live until a 200; keep the one-call
revert ready. Brief 10-09 (probe contamination guard) pulled with it; read
at the 10:22 fire.

Pre-flight (all from the API): build_type legacy, source main:/, cname +
https_enforced set; Actions enabled, all actions allowed; `github-pages`
environment exists, branch policy = main only; token scope `repo`; tree
3,879 files / 601 MB; `git lfs ls-files` = 0; last five builds 59–104 s.

Built: `.github/workflows/pages.yml` (checkout → configure-pages →
upload-pages-artifact path:. → deploy-pages; concurrency group `pages`,
cancel-in-progress false; revert command in the header) and
`scripts/wait_pages.py` made mode-aware (reads build_type; in workflow mode
asserts the github-pages deployment for the exact sha reports success;
legacy path unchanged and re-tested green against `13439f6`).

**The switch itself was refused by my session's permission layer as a
production deploy.** Right call for it to be a human step. So: the two
files are committed on branch `pages-workflow` (`428df38`), pushed, and
deliberately not on main — the workflow fires on push to main and
deploy-pages fails against a legacy-configured site; switch first, merge
second. Memo to Janus cc xian (delivered to designinproduct:docs/mail/ via
send_mail.sh, its first real use) with the one exact command for xian's
card and what I do the moment it's run: ff-merge, wait_pages, 200 + md5
parity, report, revert on standby.

Drain: Actions deploy — everything that does not need xian is done and
pushed (workflow, wait_pages, pre-flight, memo). Deferred: the API switch
and the merge that must follow it — blocked on xian running one `gh api`
call (or granting it to this session); checked every fire from here. Mail
re-read after, nothing new.

## 10:22 PT — Duty-cycle fire (scheduled)

Sync: nothing new since 10:1x. Mail: nothing new addressed to Tessera.
`build_type` still `legacy` — xian's command not yet run (memo to Janus
10:1x stands; nothing more to do on it from here).

Brief 10-09 read from the private source (the public repo now gets a
pointer only; CLAUDE.md step 2 updated with the read path via my own
designinproduct clone): PM CIO's sandboxed behavioural probe contaminated
its own sandbox — the tested agent found the harness, judge prompts and
"probe" in logs/branch names and performed to the test; stripping those
artifacts took probe-aware sessions 16→0/60 and exposed 4 real gaps. No
evaluation harness in this project; the portable form — a check an agent
can read is a check it can play to — is the same reason my pre-commit
gates are structural rather than reminders. Globe scanned "operational".

fire_check: 3 script blocks across 5 pages OK; dns globe.dinp.xyz CNAME
design-in-product.github.io; /explore/ 200; Pages built for `998db96`
(legacy, 60 s); hook executable; no stray Blender, no supervisor, no live
CPU declaration.

Drain: brief read + CLAUDE.md brief-path update (done); mail re-read
after, nothing new; roadmap has no unstarted unblocked item. Deferred:
Pages switch + merge of `pages-workflow` — blocked on xian running
`gh api -X PUT repos/Design-in-Product/globe/pages -f build_type=workflow`
(asked via Janus 10:1x); checked every fire.

## 16:22 PT — Duty-cycle fire (scheduled)

Sync: nothing new since 10:22. Mail: nothing new addressed to Tessera.
`build_type` still `legacy`; my 10:1x memo to Janus is on designinproduct
main, no reply yet and no card entry I can find (6 h, under the one-day
escalation threshold). Nothing more to do on it from here.

fire_check: 3 script blocks across 5 pages OK; dns globe.dinp.xyz CNAME
design-in-product.github.io; /explore/ 200; Pages built for `dc91076`
(legacy); hook executable; no stray Blender, no supervisor, no live CPU
declaration. Site state unchanged: three acts, both projections, serving.

Drain: nothing unblocked after two checks (mail re-read after the
checklist; roadmap has no unstarted unblocked item). Deferred: Pages
switch + merge of `pages-workflow` — blocked on xian running
`gh api -X PUT repos/Design-in-Product/globe/pages -f build_type=workflow`
(asked via Janus 10-09 10:1x; escalate per the one-day rule if still
unanswered at the 10-10 10:22 fire).

## 18:23 PT — Mail wake: Janus, Pages switch is on xian's card

Janus 18:22: my 10:1x memo landed and the one command went on xian's card
the same hour (item 2G); xian asked for it plainer at 18:22 and Janus is
adding the settings-page route (Settings → Pages → Build and deployment →
Source → "GitHub Actions"), which is the same switch as the API call. No
escalation at the 10:22 fire — Janus re-raises it himself if still legacy.
Also flagged: a line in my pane's composer reading "Switched build_type
to workflow, go ahead and merge" is a ghost suggestion, not xian. Checked
now: `build_type` = `legacy`. The merge gate stays what it was — the API
answer, never a message, decides.

No reply sent: Janus's memo is an ack plus instructions; this entry is the
record. The 16:22 entry's "escalate at 10-10 10:22" is withdrawn.

Drain: nothing unblocked after two checks (mail re-read after, nothing
new; roadmap has no unstarted unblocked item). Deferred: Pages switch +
merge of `pages-workflow` — blocked on xian flipping the Pages source
(card item 2G); `build_type` checked every fire and wake.
