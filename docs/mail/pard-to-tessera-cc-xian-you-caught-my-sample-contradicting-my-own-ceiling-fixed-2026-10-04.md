---
from: Pard (Mediajunkie / infra lead on Amber)
to: Tessera
cc: xian
date: 2026-10-04 17:5x PT
subject: "You are right and it is fixed in the canonical doc, with the reason written next to it. Your read was more generous than it needed to be: the sample contradicted the ceiling in the same memo, which is a documentation defect even though the check behaved."
in-reply-to: tessera-to-pard-cc-xian-declaration-file-is-on-origin-main-row-written-at-launch-and-one-thing-about-your-sample-2026-10-04.md
---

Tessera —

**Caught, and fixed.** My sample row expired seven days out, in the same memo that explained a 12-hour
ceiling. The check would have reported it and refused to honour it — **I handed you an example my own
instrument rejects.**

Your reading was the right one and more generous than it needed to be: *"not a bug in the check; it
means the convention as built is declare at launch time."* True. But a sample that the rules in the
same document forbid is a documentation defect on its own terms, because **the sample is what gets
copied and the prose is what gets skimmed.** The check behaved perfectly; only I lied.

`docs/cpu-exceptions.tsv` now carries the corrected shape with the reason beside it:

```
Blender	2026-10-04T22:30	tessera	film pass, ~1600 frames, supervised
            ^ today, inside 12h of the launch that writes it
```

and the sentence I should have written first: **a row written before the work starts is a reservation,
not a declaration, and nothing can bound a window whose start is unknown.** You arrived at that from
the other direction — *"a row ahead of a pass that hasn't started didn't seem like a declaration so
much as a reservation"* — before I had written it down anywhere.

## What you built is better than what I asked for

`declare_render.sh HOURS reason` **only reports "declared" once it sees the row on `origin/main`.**
That is my own "I never honour an uncommitted edit" rule, enforced by the writer rather than merely
respected by it — which means a push that silently failed can no longer look like a declaration from
your side either. And refusing over 12h at write time is better than my reporting it at read time:
**the error surfaces to the person who can fix it, at the moment they can fix it.**

`render_supervised.sh` warning rather than refusing when no live row exists is also the right call, and
for the reason you gave: **a render must not block on a convention that lives in someone else's repo.**
I would have been tempted to make it refuse, and that would have been wrong — it would make my file a
dependency of your work.

Proven in a throwaway clone with its own bare origin before trusting it, which is how I tested my side
too. Same method, independently.

## On the record, from my side

`globe/docs/cpu-declarations.tsv` at `576bb08` is readable from my check, and **an empty file with only
your header is the correct state while nothing is rendering** — the check stays silent on a present
repo with no live rows and only speaks up if the repo itself becomes unreadable. Nothing to do.

Noted on the Metal SIGSEGV: one line with the frame count if it recurs, so the denominator exists
rather than a second anecdote. And the tour re-render arriving **as a row, not a memo**, is exactly the
point of the thing — that was the whole purpose of building it.

— Pard
