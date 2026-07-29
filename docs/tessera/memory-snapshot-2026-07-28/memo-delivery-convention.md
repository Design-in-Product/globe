---
name: memo-delivery-convention
description: "Inter-agent memos are delivered by writing the file into the RECIPIENT's repo, not ours"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1b2ec6f6-37e2-43d3-9f24-caf747003efc
---

Sending a memo to another DinP agent means placing the file in the **recipient's** repo mail directory — e.g., mail to Janus goes in `~/Development/designinproduct/docs/mail/`. A memo committed to our own `docs/mail/` is *incoming* mail or undelivered.

**Why:** xian corrected this on 2026-07-13 when Tessera first drafted a memo into the globe repo ("The main trick is you put the mail in their repo, not in ours").

**How to apply:** filename convention stays `memo-{from}-to-{to}-{topic}-{date}.md`; write it directly into the recipient's `docs/mail/`. Our own `docs/mail/` holds mail addressed *to* Tessera.

Related: [[roadmap-execution-mandate]]
