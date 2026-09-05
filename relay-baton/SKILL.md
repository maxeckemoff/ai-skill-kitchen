---
name: relay-baton
description: "Produces the ThreadOps relay artifacts that pass next-action state between Cowork sessions, governed by ThreadOps_Canon.md (AI Org Chart); this skill is the recipe, the canon is the rule. Use when a session finishes work another must pick up, or the user says write the baton, hand this off, relay to the next session, emit the next-prompt tail, fan this out, or log the ledger. Four behaviors: (1) the response-tail baton, Next prompt / Decision needed / Thread terminal, in mandatory v2 format (one target per baton ID, its own fenced block, a re: line on replies, zone-proof Eastern stamps); (2) bridge batons written into the target's Current Instruction when the sender has write access; (3) fan-out sequences, sequential baton IDs with send order stated between blocks, never merged into one block; (4) the relay ledger, EMITTED / DELIVERED / SUPERSEDED / STALE against the project's registered RELAY_LOG path, one writer per file, seat-scoped when a project has more than one routing seat."
---

# Relay baton

`ThreadOps_Canon.md` (AI Org Chart) governs; read it first. The canon carries the rules, this skill carries the recipes. Where they differ, the canon wins.

The org's substrate is pull-based: files do not push, sessions act only when prompted. The relay baton is how a session hands the next action to whoever must act next, in a form that is paste-ready and logged, so threads do not stall silently. This skill emits the ThreadOps relay artifacts and, optionally, lints bridge entries for the codename hygiene that makes threads greppable.

These four behaviors are one verb (pass the baton), sharing the codename and baton format, so they live in one skill. The thread-tag-hygiene lint is folded in as an optional step, not a separate skill, per the kitchen-sprawl guidance.

## The codename convention (used by every artifact here)

Every tracked cross-session thread has a codename: `#PROJECT_TopicCamelCase` (for example `#VATR_CustRefundStmt`, `#ORG_HHHRealign`), minted at thread birth by the spawning session. The rule: every bridge entry that advances a tracked thread, and every baton block this skill emits, carries the codename. That is what makes tracking nearly free, `rg "#VATR_CustRefundStmt"` across the Projects tree reconstructs the whole thread. If a thread has no codename yet, mint one before emitting a baton.

## Mandatory baton format (v2, ThreadOps Canon)

Three rules, each replacing a shape that lost something. Every baton this skill emits, in a response tail, a bridge write, or a fan-out block, follows this format.

1. **One target per baton ID.** A hand-off to three seats is three IDs, not one ID with three sections. A ledger row tracks one delivery, and a merged baton cannot be half DELIVERED.
2. **Each baton is its own fenced code block**, so a target can copy exactly its own instruction with nothing else attached. A multi-consumer send is a fan-out of sequential IDs, send order stated in plain text between the blocks (see Behavior 3).
3. **A baton answering another opens with a `re:` citation line** naming the baton it answers, directly under the ID line. Mandatory on replies and acks, omitted only on thread-opening batons. This is what lets a ledger sweep auto-match DELIVERED instead of inferring it from bridge context.

Both the ID line and the signature line carry an Eastern timestamp WITH ITS ZONE, per the canon's Clocks rule. A stamp without a zone is not a clock read; generate one with `TZ=America/New_York date '+%Y-%m-%d %H:%M %Z %z'` (Linux sandboxes honor the override; Windows shells use PowerShell `Get-Date` with `(Get-TimeZone).Id`, since `TZ=` is silently ignored there).

Template, fenced per the append-verification quoting rule so a later append cannot match the template's own markers instead of a real section header:

~~~
[BATON <SENDER>-<MMDD>-<NN>]  <YYYY-MM-DD HH:MM ZONE OFFSET>
re: <BATON-ID being answered>   (only when replying)

  to <TARGET-SESSION> #<Codename>
      <self-contained directions: recap, paths and ids, imperative task,
       done-looks-like, one codename section per identifier>

  Sent by <SENDER-ID>, <YYYY-MM-DD HH:MM ZONE OFFSET>
~~~

## Behavior 1: the response-tail baton (standing rule)

End the response with exactly one of these three forms, in the mandatory format above:

- `Next prompt: [TARGET-ID] #CODENAME` followed by a paste-ready block the user can drop straight into the target session.
- `Decision needed: <what is being decided> [Human Orchestrator]` when the next step is a human judgment call.
- `Thread terminal: #CODENAME DONE, notify register` when the thread is finished.

The paste-ready block under a Next prompt is a complete instruction the target can act on without hunting for context: what to do, the concrete inputs (paths, IDs), and the expected deliverable. One tail per response; if several threads advanced, lead with the most urgent and note the others.

## Behavior 2: the bridge baton

When the sender has write access to the target's bridge, do not just hand the baton to the Human Orchestrator, ALSO write it into the target's `## Current Instruction` section, in the mandatory format above (including the `re:` line if it answers a prior baton). The receiving session picks it up on its bridge-freshness re-read (see the bridge-freshness rule), so the Human Orchestrator's paste shrinks to "check your bridge." Steps:

1. Confirm write access to the target bridge and its path.
2. Replace the target's Current Instruction with the baton: the paste-ready ask, tagged with `#CODENAME`, signed by the sender with the date.
3. In the response tail, point the Human Orchestrator at it: `Next prompt: [TARGET-ID] #CODENAME - baton written to its bridge Current Instruction; tell it to re-read its bridge.`

Where no write access to the target bridge exists, the response tail carries the full baton block for the Human Orchestrator to paste directly. Never leave a baton only in your own head or buried mid-response.

## Behavior 3: fan-out sequences (the PQREV pattern)

When one result feeds several sessions, emit a numbered, dependency-ordered sequence: sequential baton IDs, each its OWN fenced block per the mandatory format, send order stated in plain text between the blocks. Do not merge targets into one block; a fan-out is several baton IDs, not one ID with several sections. Template:

```
Fan-out: #CODENAME
Send order: 1, then 2 and 3 in parallel, then 4
```

~~~
[BATON <SENDER>-<MMDD>-<NN>]  <YYYY-MM-DD HH:MM ZONE OFFSET>

  to <TARGET-A> #CODENAME (no deps)
      <self-contained directions>

  Sent by <SENDER-ID>, <YYYY-MM-DD HH:MM ZONE OFFSET>
~~~

~~~
[BATON <SENDER>-<MMDD>-<NN+1>]  <YYYY-MM-DD HH:MM ZONE OFFSET>

  to <TARGET-B> #CODENAME (after 1)
      <self-contained directions>

  Sent by <SENDER-ID>, <YYYY-MM-DD HH:MM ZONE OFFSET>
~~~

State dependencies explicitly so the Human Orchestrator knows what can fire now and what waits. Mark which steps are parallel-safe. Every block carries the codename and its own baton ID.

## Behavior 4: the relay ledger (proof of what went out)

Point at the project's registered RELAY_LOG path, never a hardcoded folder. Find it via `AI Org Chart\Bridge_Index.md`'s ledger registry; if a project has no registered ledger yet, that is a signal to register one before logging, not a reason to write to an unregistered file.

- **One writer per file.** A project with more than one routing seat gets seat-scoped sibling ledgers, `<Project>\_TaskLogs\RELAY_LOG_<SEAT>.md`, one per seat. A single project-level `RELAY_LOG.md` is the special case where exactly one seat routes. A seat that is not a file's writer drafts its baton in its response and never writes that file.
- **Four statuses**: EMITTED (baton sent), DELIVERED (target acted or acked; the `re:` line is what lets a sweep auto-match this instead of inferring it), SUPERSEDED (a later baton replaced this one before delivery), STALE (three days with no reply; the sender re-sends or escalates rather than waiting further).
- **Rotation**: monthly, to `<Project>\_TaskLogs\archive\RELAY_LOG_<SEAT>_<YYYYMM>.md`.
- **Registration**: every live ledger, project-level or seat-scoped, is registered in the Bridge_Index ledger-registry row; a seat's first routed baton is what makes its ledger live and registrable. Baton IDs stay globally unique by sender prefix, so the split across seat files costs nothing to read across.

## Optional step: thread-tag-hygiene lint

When asked to check tag hygiene, or before a register sweep, scan recent bridge Activity Log entries and flag any that advance a tracked thread but omit its `#codename`. A cheap check: `rg -n "#\w+_[A-Za-z]" <bridge>` shows which entries are tagged; entries that clearly advance a known thread but have no tag are the misses. Output a short list: file, entry date, the codename that should be added. Do not edit the entries silently; propose the additions and let the owner apply them. This keeps `rg`-based thread reconstruction reliable.

## Paths and links inside batons

A baton is mostly paths, so a path that does not open is a baton that stalls. The format depends on **who reads it**, and getting this wrong is the most common reason a "clickable" path is not clickable.

**Rule 1: a relative link resolves against the READER's workspace root, not the writer's.**

In VS Code a markdown link like `[name](_plans/active/file.txt)` is resolved relative to the root of the workspace the reader has open. That is fine for your own response, which the Human Orchestrator reads while your project is open. It is wrong inside a paste-ready block destined for another session, because that session is rooted in a different project folder and the same relative path either misses or resolves to the wrong file. Silently.

So:

- **Links in your own response, for the Human Orchestrator:** workspace-relative from YOUR primary root, forward slashes. Clickable.
- **Paths inside a paste-ready baton block for another session:** absolute, in a code span. Not a markdown link. The receiving session pastes or opens it with Quick Open, and absolute paths do not care whose root is open.

**Rule 2: never include your own workspace folder name in a relative link.** The root is implicit. Prefixing it produces `Project/Project/...`, and it also drags the folder name's spaces and ampersands into the path, which is what breaks link parsing. Project folders in this org contain both (for example `FP&A Develop & Maintain`). Path from inside your root and those characters never appear.

**Rule 3: never percent-encode, never climb out with `../`, and never reach for a URI scheme or bracket wrapper.**

- `%20` for a space while leaving `&` raw is a hybrid that parses as neither. Do not encode at all.
- `../` climbs above the workspace root and has nothing to bind to. If the target is outside your root, that is the signal to switch to an absolute path in a code span, not to add more `../`.
- `file:///` URIs, `vscode://file/` URIs, and angle-bracket-wrapped destinations (`[x](<path with spaces>)`) are all dead in this chat renderer. Five-way test 2026-08-31 against a sibling-project target: angle-bracket relative, percent-encoded relative, file URI and vscode URI all failed; only the plain in-root relative control opened. A URI that works in a terminal does not work here, so do not burn a round trip re-testing them.

**Self-test before sending a baton with paths in it:** does the relative path start with `_plans` or another folder that exists directly inside your primary root, contain no spaces, no ampersands, no `%`, no `../`, no angle brackets, and no `file:` or `vscode:` scheme? If yes it will open. If it fails any of those, use an absolute path in a code span instead.

## How the four relate

- Finishing a piece of work that one other session must pick up: Behavior 1 (tail), plus Behavior 2 if you can write their bridge.
- One result feeding several sessions: Behavior 3 (fan-out).
- Recording that a baton went out, and later that it landed: Behavior 4 (ledger), on whichever seat is that project's registered writer.
- Housekeeping before a register refresh: the optional lint.

## Anti-patterns to avoid

- Do not omit the codename from a baton or fan-out block; untagged threads fall out of `rg` reconstruction.
- Do not bury the next action mid-response; it goes in the tail (and the target bridge when possible).
- Do not write a bridge baton into a target you lack write access to; hand it to the Human Orchestrator via the tail instead.
- Do not silently rewrite bridge entries during the lint; propose the codename additions.
- Do not merge more than one target into a single baton ID or a single fenced block; a fan-out is sequential IDs, each self-contained, never sections inside one block.
- Do not omit the `re:` line when a baton answers another; that citation is what lets a ledger sweep auto-match DELIVERED.
- Do not stamp a baton with a guessed or zone-less time; every stamp prints its zone or offset, or it is not a clock read.
- Do not write to an unregistered or hardcoded ledger path; look up the project's registered RELAY_LOG in Bridge_Index first, and do not write a ledger file you are not the registered writer for.
- Do not use em dashes or AI-tone phrasing in batons or tails; they are artifacts the Human Orchestrator and other sessions read.
- Do not put a workspace-relative markdown link inside a paste-ready block for another session; it resolves against their root, not yours, and fails silently. Absolute path in a code span.
- Do not prefix your own project folder name onto a relative link, and do not try to reach another project with `../`, percent-encoding, angle brackets, or a `file:`/`vscode:` URI. All five shapes are verified dead (2026-08-31); plain in-root relative is the only clickable form, and everything else is an absolute path in a code span.

## Test triggers

Examples that SHOULD fire this skill:

- "I'm done here; write the baton to hand this to VAT-DEV."
- "Fan this out: BI-ZOHO validates, then VAT-DEV and PQREV in parallel, then VAT-ARCH signs off."
- "Emit the next-prompt tail for this, and write it into the target's bridge if you can."
- "Log this baton to the ledger" or "mark BATON-0904-12 as delivered."

Examples that should NOT fire this skill:

- "Write a T-number implementation ask for the Developer." (that is `architect-to-developer-ask-authoring`; a relay baton routes an existing next-action, it does not author the implementation spec)
- "Stand up a new subordinate session." (that is `bridge-handoff-authoring`)
- "What changed in my watched docs?" (that is `live-source-watch`)
