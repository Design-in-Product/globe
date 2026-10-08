#!/usr/bin/env bash
# Deliver an outbound memo into the RECIPIENT's repo from Tessera's own clone.
#
# Pard, 2026-10-08, after my rebase --autostash in his live checkout swept his
# uncommitted edit into a commit under my name: "never rebase, stash or pull
# in another seat's working tree. Use your own clone, or commit a single file
# by exact path." These clones live in ~/globe-mail/<repo> (blobless, mine
# alone), so nothing here can touch a sibling's working tree.
#
# Usage: scripts/send_mail.sh <repo> <memo-file> [<inbox-path>]
#   repo        mediajunkie | designinproduct  (the recipient's reply-to repo)
#   memo-file   a finished memo (frontmatter with reply-to: globe:docs/mail/)
#   inbox-path  default docs/mail/ — use the recipient's reply-to path if different
set -euo pipefail
repo=${1:?repo}; memo=${2:?memo file}; inbox=${3:-docs/mail/}
clone=~/globe-mail/$repo
[ -d "$clone/.git" ] || { echo "send_mail: no clone at $clone — git clone --filter=blob:none git@github.com:mediajunkie/$repo.git $clone" >&2; exit 2; }
grep -q '^reply-to: globe:docs/mail/' "$memo" || { echo "send_mail: memo lacks 'reply-to: globe:docs/mail/' (baseline field, 2026-10-08)" >&2; exit 3; }
name=$(basename "$memo")
git -C "$clone" fetch -q origin
git -C "$clone" reset -q --hard origin/main          # my clone only; nothing of anyone else's lives here
mkdir -p "$clone/$inbox"
cp "$memo" "$clone/$inbox$name"
git -C "$clone" add -- "$inbox$name"
git -C "$clone" commit -q -m "mail(tessera->${name#tessera-to-}): $(grep -m1 '^subject:' "$memo" | sed 's/^subject: *//; s/^"//; s/"$//' | cut -c1-110)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" -- "$inbox$name"
git -C "$clone" push -q origin HEAD:main
echo "delivered: $repo:$inbox$name @ $(git -C "$clone" log origin/main --oneline -1)"
