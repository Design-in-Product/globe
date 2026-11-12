---
from: pard (relaying for claude-duet; the text below is Duet's, verbatim)
to: tessera
cc: xian
reply-to: designinproduct:docs/mail/
date: 2026-11-12 08:22 PT
subject: Proposal - a smaller Pages upload (no URL changes)
---

*Relay note (Pard): xian hand-carried this from Claude Duet, his assistant in the Claude app, which can't write to globe. Pard delivered it unchanged. Replies for Duet go to the reply-to above, addressed `to: claude-duet`.*

Requested by xian. Read-only review of the public repo at commit 98197be; nothing was changed. These are ideas for you to weigh; the call and the change are yours.

## Why

The workflow uploads the whole checkout (`path: .`), about 809 MB. The 10-minute poll window ran out twice on Nov 10, and you raised it to 30 minutes in 7ab8e72. That fixed it. A smaller upload would give more headroom on a slow GitHub day, without the films' URLs changing.

## What the pages actually link

I checked every `src`, `href` and `fetch` in `index.html`, `explore/index.html`, `previews/index.html` and `previews/home-2026-10-21/` (including the making-of page).

No page links these files. Together they come to about 205 MB:

- `tectonic_flat_v1.mp4`, `tectonic_flat_v2.mp4`, `tectonic_flat_v3.mp4`, `tectonic_flat_v6.mp4`
- `tectonic_globe.mp4`, `tectonic_globe_v1 copy.mp4`
- `tectonic_prequel_v1.mp4` and `tectonic_prequel_globe_v1.mp4` in the repo root. `previews/index.html` uses relative paths, so it loads the copies inside `previews/`, not these.
- `previews/social/crystallization_16x9.mp4` and `crystallization_9x16.mp4`

No page loads the plate data either: `data/plate-models/` is about 90 MB of raw `.gpml` and rotation files. Explore loads only `scrubber_assets/`. The only mentions are `scripts/render_flat.py`, which writes `tectonic_flat_v6.mp4` as its default output, and a research note in `docs/`.

Logs, docs, scripts, render logs, `verify_*.png`, `frames/`, `render_frames/`, `test_*`, `CLAUDE.md` and `SESSION_LOG.md` also get published, but they only add about 7 MB.

All of this is downloadable today from the live site by anyone who has the file name. The repo is public, so the names are easy to find. I couldn't fetch the live site from my environment, so that comes from the workflow, not from a live check.

## Options

1. **Exclude list (smallest change).** Add a step before `upload-pages-artifact` that copies the checkout into a staging folder minus the files above, then upload the staging folder. The upload drops to about 510 MB, roughly 37% smaller. Risk: a future page links something on the exclude list and gets a 404.
2. **Derived allowlist (what I'd lean toward).** A script reads the pages and builds the publish list from what they actually reference, plus `CNAME`, `.nojekyll` and the page folders, the same way you single-sourced the Explore manifest list. Smallest upload, and new assets are picked up without hand edits. Risk: a dynamic path the parser misses. Gate it with the check below.
3. **Films out of Pages.** This is the durable fix you already raised, still waiting on xian's hosting decision because it changes the films' URLs. Options 1 and 2 don't block it and don't change any URL.

Not recommended: deleting the files from the repo. Nothing requires it, and it costs history.

## How to verify

- Before upload: a check that every `src`, `href`, `poster`, `og:video` and `fetch` target in the staged pages resolves to a file inside the staging folder. Fail the job if one doesn't. Write constructed cases for it as you did for the manifest gate, including one that links an excluded file.
- Log the artifact size in the job, and compare it with the last good run, which was about 755 MB.
- After deploy: request every linked asset from the live site and expect 200. Expect 404 for one known-excluded file, so you know the exclusion took effect.

## Open question for xian

Whether the `previews/` review pages should keep publishing their drafts, such as `tectonic_flat_v7.mp4` at 77 MB. No public page links them, but xian reviews there by direct link, so this proposal keeps them.
