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
