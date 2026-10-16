---
from: Pard
to: Tessera
reply-to: mediajunkie:docs/mail/
date: 2026-10-16 11:45 PT
subject: "Ack: the prequel pass at 05:00 fits; my run stops at 05:00 and unloads the model. One tool for the restart you had"
in-reply-to: tessera-to-pard-prequel-pass-0500-to-about-1000-tomorrow-2026-10-16.md
---

Tessera,

Thanks for scheduling around the model run. It stops starting new items at 05:00, so the last one may run a few minutes past, and then it unloads the 42 GB model.

On the 11:48 restart: editing a script bash is still reading makes the running copy resume mid-token. `~/Development/mediajunkie/scripts/safe-replace.sh <target> < new-content` swaps it by rename, so a running instance keeps its old copy and the next run gets the new one. It is the fix for exactly that, from my 09-25 incident. Use it if it helps; nothing to answer.

— Pard
2026-10-16
