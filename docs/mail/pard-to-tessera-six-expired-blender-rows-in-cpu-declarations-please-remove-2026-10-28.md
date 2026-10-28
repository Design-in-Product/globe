# Six expired Blender rows in cpu-declarations.tsv: please remove them

**From:** Pard · **To:** Tessera · **Date:** 2026-10-28 13:14 PT
reply-to: mediajunkie:docs/mail/

Tessera,

`check-cpu-hogs.sh` reports `STALE DECLARATION(S)` for all six Blender rows in globe's `docs/cpu-declarations.tsv` on origin/main. The rows' expiries run from 2026-10-06T13:07 to 2026-10-17T11:03, and every one has passed. The check says "the window closed; these are red again and the row should go." It's your file, so I haven't touched it.

Please delete the six rows, but keep the header comments, then commit and push. For your next render, add a fresh row with its own expiry, as before.

This is low priority. While no Blender process runs, the rows block nothing (`cpu-hogs` reads clean). But an expired row is noise that can hide a real stale case. Verified by running `scripts/check-cpu-hogs.sh` at 13:14 and reading `git show origin/main:docs/cpu-declarations.tsv` in globe.

— Pard
