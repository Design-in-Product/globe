#!/usr/bin/env bash
# Deliver an outbound memo into the RECIPIENT's repo from Tessera's own clone.
#
# Pard, 2026-10-08, after my rebase --autostash in his live checkout swept his
# uncommitted edit into a commit under my name: "never rebase, stash or pull
# in another seat's working tree. Use your own clone, or commit a single file
# by exact path." These clones live in ~/globe-mail/<repo> (blobless, mine
# alone), so nothing here can touch a sibling's working tree.
#
# 2026-10-30 (xian via Janus, "one line for every seat"): the commit itself is
# now made by Pard's mediajunkie/scripts/mail-deliver.sh, pointed at MY clone.
# It stamps `date: now` from the Pacific clock, refuses a stamp ahead of the
# clock, and derives the Co-Authored-By / Claude-Session trailers from this
# session (left off with a warning, never guessed). It builds the commit in a
# throwaway worktree on origin/main, pushes by full hash and verifies the file
# landed — so this wrapper no longer resets or commits anything itself. It
# reads git identity from the CURRENT directory, hence the cd to this repo.
# Proven 2026-10-30 against a scratch bare remote + blobless clone: date
# stamped, author Tessera, both trailers, future stamp refused (exit 2).
#
# Usage: scripts/send_mail.sh <repo> <memo-file> [<inbox-path>]
#   repo        mediajunkie | designinproduct  (the recipient's reply-to repo)
#   memo-file   a finished memo: frontmatter with reply-to: globe:docs/mail/
#               and `date: now` (a hand stamp is accepted only if not ahead)
#   inbox-path  default docs/mail/ — use the recipient's reply-to path if different
set -euo pipefail
repo=${1:?repo}; memo=${2:?memo file}; inbox=${3:-docs/mail/}
cd "$(dirname "$0")/.."                                 # identity comes from here
clone=~/globe-mail/$repo
deliver=~/Development/mediajunkie/scripts/mail-deliver.sh
[ -d "$clone/.git" ] || { echo "send_mail: no clone at $clone — git clone --filter=blob:none git@github.com:mediajunkie/$repo.git $clone" >&2; exit 2; }
[ -x "$deliver" ] || { echo "send_mail: $deliver missing or not executable (Pard's tool, mediajunkie main)" >&2; exit 2; }
grep -q '^reply-to: globe:docs/mail/' "$memo" || { echo "send_mail: memo lacks 'reply-to: globe:docs/mail/' (baseline field, 2026-10-08)" >&2; exit 3; }
grep -qE '^date:[[:space:]]*now' "$memo" || echo "send_mail: note — memo carries a hand stamp; 'date: now' lets the tool write it (xian 10-30)" >&2
exec "$deliver" "$clone" "${inbox%/}/$(basename "$memo")" < "$memo"
