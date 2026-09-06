---
name: relay-baton
description: "Produces the ThreadOps relay artifacts that pass next-action state between Cowork sessions, governed by ThreadOps_Canon.md (AI Org Chart), which this skill implements as recipes. Use when a session finishes work another must pick up, when a judgment call must go to the Human Orchestrator, or the user says write the baton, hand this off, relay to the next session, emit the next-prompt tail, fan this out, or log the ledger. Carries the canon session-signature spec (FULL default). Five behaviors: the response-tail baton (Next prompt, Decision needed, or Thread terminal) in the mandatory v2 format (one target per baton ID, own fenced block, re: line on replies, zone-stamped); the DECISION CARD written to MAX_DECISIONS_PENDING and summarised in the response; bridge batons written into a target's Current Instruction where write access exists; sequential-ID fan-out with send order stated; and the relay ledger (EMITTED / DELIVERED / SUPERSEDED / STALE) at the project's registered RELAY_LOG path, one writer per file."
---

# Relay baton

`ThreadOps_Canon.md` (AI Org Chart) governs; read it first. The canon carries the rules, this skill carries the recipes. Where they differ, the canon wins.

The org's substrate is pull-based: files do not push, sessions act only when prompted. The relay baton is how a session hands the next action to whoever must act next, in a form that is paste-ready, addressed, timestamped and logged, so threads do not stall silently and so the Human Orchestrator can always answer "what was sent, to whom, and when".

These behaviors are one verb (pass the baton), sharing the codename and baton format, so they live in one skill. The thread-tag-hygiene lint is folded in as an optional step.

## The codename convention (used by every artifact here)

Every tracked cross-session thread has a codename: `#PROJECT_TopicCamelCase` (for example `#VATR_CustRefundStmt`, `#ORG_HHHRealign`), minted at thread birth by the spawning session. Every bridge entry that advances a tracked thread, and every baton block this skill emits, carries the codename. That is what makes tracking nearly free: `rg "#VATR_CustRefundStmt"` across the Projects tree reconstructs the whole thread. If a thread has no codename yet, mint one before emitting a baton.

## Where the artifacts live

Each project keeps a `_TaskLogs` folder at its root:

- `<Project>\_TaskLogs\RELAY_LOG.md`, or `RELAY_LOG_<SEAT>.md` when more than one seat routes: the baton ledger and thread register. The live path for any project is the one registered in `AI Org Chart\Bridge_Index.md`; look it up rather than assuming.
- `<Project>\_TaskLogs\MAX_DECISIONS_PENDING.md`: the decision cards for that project.

**One writer per file.** A shared append target across many sessions produces OneDrive conflicted copies and tail corruption. An estate-wide rollup, where it exists, is a read-only computation by the ORG tracker seat, which works because baton IDs are globally unique by sender prefix.

**Rejected design, recorded so it is not re-proposed:** a single central ledger every session writes RECEIVED to on open. It is the multi-writer shape the corruption rule exists for, and a skipped receipt reads as "never sent" when it was sent and actioned. False negatives in a delivery ledger are worse than no ledger.

## Mandatory baton format (v2, ThreadOps Canon)

Three rules, each replacing a shape that lost something. Every baton this skill emits, in a response tail, a bridge write, or a fan-out block, follows this format.

1. **One target per baton ID.** A hand-off to three seats is three IDs, not one ID with three sections. A ledger row tracks one delivery, and a merged baton cannot be half DELIVERED.
2. **Each baton is its own fenced code block**, so a target can copy exactly its own instruction with nothing else attached. A multi-consumer send is a fan-out of sequential IDs, send order stated in plain text between the blocks (Behavior 4).
3. **A baton answering another opens with a `re:` citation line** naming the baton it answers, directly under the ID line. Mandatory on replies and acks, omitted only on thread-opening batons. This is what lets a ledger sweep auto-match DELIVERED instead of inferring it from bridge context.

Baton IDs are `<SENDER>-<MMDD>-<NN>`, numbered sequentially within the day, so a baton can be referred to later ("did 0904-02 go out?") without quoting its text. Both the ID line and the signature line carry an Eastern timestamp WITH ITS ZONE (`2026-09-05 22:44 EDT`), per the canon's Clocks rule; the numeric offset is a read-time check, not part of the printed stamp. A stamp without a zone is not a clock read. Read the clock, never estimate: `TZ=America/New_York date '+%Y-%m-%d %H:%M %Z'` in a Linux sandbox; in Windows shells `TZ=` is silently ignored, use PowerShell `Get-Date` with `(Get-TimeZone).Id`. A guessed timestamp is worse than none, because it looks authoritative.

Template, fenced with tildes so a later append cannot match the template's own markers instead of a real section header:

~~~
[BATON <SENDER>-<MMDD>-<NN>]  <YYYY-MM-DD HH:MM ZONE>
re: <BATON-ID being answered>   (only when replying)

  to <TARGET-SESSION> #<Codename>
      <self-contained directions: one or two sentences of recap since the target
       last acted, exact paths and ids, the task in the imperative, and
       done-looks-like in one line>

  Sent by <SENDER-ID>, <YYYY-MM-DD HH:MM ZONE>
~~~

**GLOBAL RULE, non-negotiable (the Human Orchestrator, 2026-09-06): the baton ID line and the sender signature go INSIDE the fenced block, never as a header above it.** Every copy-paste block is self-contained provenance: the FIRST line inside the fence is `[BATON <SENDER>-<MMDD>-<NN>]  <YYYY-MM-DD HH:MM ZONE>` (plus the `re:` line when replying), and the LAST line inside the fence is `Sent by <SENDER-ID>, <YYYY-MM-DD HH:MM ZONE>`. When the orchestrator copies the block alone, it must already say who sent it, when, and under which baton ID, with nothing left outside. A `Next prompt:` / `Fan-out:` label may sit ABOVE the fence for the Human Orchestrator, but it is a duplicate pointer, not the baton; stripping it must lose nothing. This applies to the tail baton, the fan-out blocks, and the bridge write alike.

**Every baton is self-contained.** The baton is the only context the human router carries between panes; a pointer baton ("check your bridge, #tag") just moves the dig onto the target, which burns its first turn reconstructing. The one exception is a target whose standing protocol is bridge-first, and even then the baton names the specific entries to work.

## Behavior 1: the response-tail baton (standing rule)

Per the canon's responses-to-the-orchestrator section, every response closes with the session signature (next section, FULL by default) and then exactly one of these three forms:

- `Next prompt: [TARGET-ID] #CODENAME` followed by a baton block in the mandatory format. If several targets must act, one block per target, most urgent first.
- `Decision needed: <what is being decided> [Human Orchestrator]` when the next step is a human judgment call. **Always pairs with a decision card, Behavior 2.**
- `Thread terminal: #CODENAME DONE, notify register` when the thread is finished.

An inbound FYI or confirmation baton with no natural reply gets a one-line receipt, not a fresh baton. The baton is a label on finished work, not a checkpoint: run the work end to end and stop only for a judgment that is the Human Orchestrator's.

## Session signature (GLOBAL CANON, ruled by the Human Orchestrator 2026-09-05)

Every response to the Human Orchestrator closes with a session signature, then the relay baton. **FULL is the
default for every session, Cowork and Claude Code alike.** CONDENSED is emitted only when the Human Orchestrator
asks for it. This supersedes the earlier two-part signature and the earlier FULL/CONDENSED
draft; the difference is that FULL now carries as much diagnostics as the session can measure,
and CONDENSED collapses to a single top row.

**The stamp carries the zone abbreviation and NO numeric offset.** `2026-09-05 17:33 EDT`, not
`... EDT -0400`. This settles the open item on the clock-format question: the Clocks rule asks for
"zone or offset", and the zone alone satisfies it. The `%Z %z` formatting guidance applies to
shell clock reads, not to the rendered signature.

**FULL**, one line each, in this order. `·` is the middle-dot separator the generator emits.

```
SEAT · full-session-id · N% capacity · turn N · N compactions · N prompts
last      pN · HH:MM · N calls · in X · cache-write X · cache-read X · out X · $X   <- INCREMENTAL, this prompt only
cumulat.  in X · cache-write X · cache-read X · out X                  (NO cost on this line)
context   effective X · window X · fill N% · cache hit N%
plan      5h N% · 7d N% · extra usage $N this period · plan name
benchmark $N API-equiv · N% capacity · rates vN · 1h TTL · model
tools     Name N · Name N · ...
prompts (newest first, each with its heaviest call)
  pN  HH:MM  N calls   in X  cw X  cr X  out X  $N  heaviest call label
  ... ALL prompts by default; cut off per session only when the Human Orchestrator says so
caveats   the standing caveats
YYYY-MM-DD HH:MM ZONE
```

**CONDENSED**, the top row only:

```
SEAT · full-session-id · N% capacity · turn N · N compactions · N prompts · X eff · $N API-equiv · YYYY-MM-DD HH:MM ZONE
```

Changes from the first published spec, all ruled by the Human Orchestrator on 2026-09-05: percent of context
CAPACITY replaces the model name on line 1 and echoes on the benchmark line; an INCREMENTAL
`last` block sits between identity and cumulative; the cost figure appears ONCE, on benchmark,
never on the cumulative line; prompt rows are UNCAPPED by default; the earlier "top calls" and
"by prompt" sections are COLLAPSED into the single prompts table; the standalone note line about
per-session dollars is deleted; and `plan` carries the extra-usage slot so correction 1 has
somewhere to land.

**Rendering is the seat's choice, ruled 2026-09-05.** The canon fixes the FIELDS and their ORDER,
not the delimiter. A terminal seat uses a fixed-width block because that is what aligns there; a
Cowork seat uses a markdown table, because a code fence does not render well for the Human Orchestrator in that
surface. Either is compliant so long as every field is present in order.

**RETRACTED 2026-09-05: Cowork CAN measure all of this.** This page previously said a Cowork seat
has no transcript and must mark token rows unavailable. That is WRONG, disproved by a peer ops seat
running `session_signature.py` unmodified against its own live transcript and getting every prompt
row with real counts. `/mnt/.claude/projects` is readable from Cowork. The real Cowork limitation
is narrower: the SKILLS MOUNT is cached at session start, so a canon edit does not reach a running
Cowork session until it restarts. Do not restate the telemetry claim; it survived two batons before
being caught and was becoming lore.

Where a seat genuinely has no transcript, it emits the identity line plus `no transcript surface`
and the stamp. Saying so explicitly is the rule; silently dropping measured lines is not, because a
reader cannot tell an absent figure from a zero one.

**Abbreviation:** exact under 1,000, `47k` to 999,999, `1.90M` at or above a million.

**Generator:** `AI Org Chart\_TaskLogs\session_signature.py`, which reads the session's own
`.jsonl`. Do not hand-type a signature; a hand-typed figure is an estimate presented as a
measurement, which is the failure the Clocks rule already guards against.

## Behavior 2: the DECISION CARD (standing rule, Human Orchestrator 2026-08-28)

**Never surface a decision as a bare question. Always surface the card.** The Human Orchestrator should not have to reprompt for context, and the card must still make sense a week later, cold.

Every time something needs a human judgment, do BOTH. Neither substitutes for the other.

**A. Write the card to the project's `_TaskLogs\MAX_DECISIONS_PENDING.md`.**

**B. Summarise the card in the response**, then close with the `Decision needed:` tail.

### The card skeleton, in this order

1. **ID and one-line question.** `D-nn` for decisions, `P-nn` for parked items. A sentence a stranger could act on.
2. **The 30-second version.** Why this is a question at all.
3. **The numbers.** A table: actual figures, units, source named. If a figure is unmeasured, say so rather than omitting it.
4. **Why it is a real choice and not a data-quality question.** If one option is simply wrong, say so instead of manufacturing a balanced choice.
5. **The options**, numbered, each with what it means concretely.
6. **What each one costs.** Distinguish "changes a number on a filed form" from "changes how a page is labelled" from "changes what we build".
7. **If you do nothing.** Whether work stalls, what keeps the decision cheap and reversible, what cannot happen until it is ruled.
8. **Recommendation**, with the reason. Say if it is not yours to recommend and why.
9. **Where the detail lives.** File paths and section names.

### Maintaining the file

- Summary table at the top, open items first: ID, decision, owner, what it blocks, status.
- Resolved items move to a RESOLVED section, keeping the ruling, the date, the Human Orchestrator's own words where given, and the consequences applied. Never delete a resolved decision; the reasoning is the value.
- Parked items stay, with explicit revisit triggers. Parking a remediation is not retiring a finding.
- Update `Last updated` every time.

When a ruling arrives, propagate it the same turn to every bridge and design doc that depended on it, and record it in the card's RESOLVED entry. A ruling that lives only in the chat gets re-litigated.

## Behavior 3: the bridge baton

When the sender has write access to the target's bridge, do not just hand the baton to the Human Orchestrator, ALSO write it into the target's `## Current Instruction`. The receiving session picks it up on its bridge-freshness re-read, so the paste shrinks to "re-read your bridge".

1. Confirm write access and the bridge path.
2. **Re-read the target bridge's Activity Log head before writing.** Any status claim in a Current Instruction is verified at the moment of writing, never recalled.
3. Post the baton as a NEW Current Instruction. **Never amend an active CI in place**: a CI is read once and the bridge does not push to a running session. The one safe exception is a CI whose baton has not yet been consumed; amend it, mark the amendment with its time inside the CI, and tell the Human Orchestrator.
4. In the response tail, still emit the block in the mandatory format, with the direction "re-read your bridge; new Current Instruction on top".

Where there is no write access, the tail carries the full baton block to paste. Never leave a baton only in your own head or buried mid-response.

## Behavior 4: fan-out sequences (the PQREV pattern)

When one result feeds several sessions, emit a numbered, dependency-ordered sequence: sequential baton IDs, each its OWN fenced block, send order stated in plain text between the blocks, parallel-safe steps marked. Open with the carried-forward line from Behavior 5.

```
Carried forward, no reply observed: ARCH-0903-02 (DATA-CODER), ARCH-0903-03 (FIN-REBUILD)
Fan-out: #CODENAME
Send order: 1, then 2 and 3 in parallel, then 4
```

~~~
[BATON <SENDER>-<MMDD>-<NN>]  <YYYY-MM-DD HH:MM ZONE>

  to <TARGET-A> #CODENAME (no deps)
      <self-contained directions>

  Sent by <SENDER-ID>, <YYYY-MM-DD HH:MM ZONE>
~~~

~~~
[BATON <SENDER>-<MMDD>-<NN+1>]  <YYYY-MM-DD HH:MM ZONE>

  to <TARGET-B> #CODENAME (after 1)
      <self-contained directions>

  Sent by <SENDER-ID>, <YYYY-MM-DD HH:MM ZONE>
~~~

## Behavior 5: the RELAY LEDGER

The Human Orchestrator pastes batons manually, so the sending session cannot know what actually went out. Do not guess, and do not silently re-issue.

Write only to the ledger you are the registered writer for, at the path registered in `AI Org Chart\Bridge_Index.md`. A project with more than one routing seat gets seat-scoped siblings, `<Project>\_TaskLogs\RELAY_LOG_<SEAT>.md`. The ledger file is seat-owned and a seat may create its own; only the registry row in Bridge_Index is ORG's. If no ledger is registered yet, create yours and ask ORG for the row in the same turn.

The ledger carries two tables:

- **Baton ledger:** `| ID | ET stamp | Target | Codename | Ask | Status |`, one row per baton.
- **Thread register:** every codename the seat owns, its state, what it is blocked on, who holds it. Plus a carried list of small items owned by the Human Orchestrator, which otherwise vanish.

**Status values.** `EMITTED` the block appeared in a response. `DELIVERED` the target's own bridge carries a reply or receipt (the `re:` line is what lets a sweep match this). `SUPERSEDED` replaced before it was actioned. `STALE` over three days with no reply; re-read the subject before re-issuing, because content moves. Rotate monthly to `<Project>\_TaskLogs\archive\`.

**A baton is EMITTED only once its block actually appears in a response.** Writing the row before emitting the block makes the ledger assert something untrue. Write the row and the block in the same turn; if the turn ends without the block, the row must not say EMITTED.

**Delivery is inferred from evidence.** Sessions are not asked to write receipts; the bridge entry they would write anyway is the receipt. A baton with no natural reply (a hold, a stand-down, an FYI) gets a one-line acknowledgement on the target's own bridge.

**Every fan-out opens with a carried-forward line** naming prior batons with no observed reply.

## Optional step: thread-tag-hygiene lint

When asked, or before a register sweep, scan recent bridge Activity Log entries and flag any that advance a tracked thread but omit its codename. Cheap check: `rg -n "#\w+_[A-Za-z]" <bridge>` shows which entries are tagged. Output a short list: file, entry date, the codename that should be added. Do not edit entries silently; propose the additions.

## Paths and links inside batons

A baton is mostly paths, so a path that does not open is a baton that stalls. The format depends on **who reads it**.

**Rule 1: a relative link resolves against the READER's workspace root, not the writer's.** Links in your own response, for the Human Orchestrator: workspace-relative from YOUR primary root, forward slashes, clickable. Paths inside a paste-ready block for another session: absolute, in a code span, not a markdown link; the receiving session is rooted elsewhere and a relative path misses silently.

**Rule 2: never include your own workspace folder name in a relative link.** The root is implicit; prefixing it produces `Project/Project/...` and drags the folder name's spaces and ampersands into the path, which breaks link parsing.

**Rule 3: never percent-encode, never climb out with `../`, and never reach for a URI scheme or bracket wrapper.** `%20` with a raw `&` parses as neither. `../` has nothing above the root to bind to; if the target is outside your root, switch to an absolute path in a code span. `file:///`, `vscode://file/` and angle-bracket destinations are all dead in this chat renderer (five-way test 2026-08-31; only the plain in-root relative control opened).

**Self-test before sending:** does the relative path start with a folder that exists directly inside your primary root, with no spaces, ampersands, `%`, `../`, angle brackets, or `file:`/`vscode:` scheme? If yes it will open. Otherwise, absolute path in a code span.

## Artifacts published from a session (standing rule, the Human Orchestrator 2026-09-05)

**Every artifact created in a Claude Code session is also shared with the Human Orchestrator's
account as Editor.**

**This cannot be automated from inside a session, and pretending otherwise would be the bug.**
The Artifact tool exposes publish, read, list, comment, watch and database actions; it has NO
share action, and artifacts are private to their creator until shared from the page's own share
menu. So the rule binds the session's REPORTING, not its tool calls: whenever a session publishes
an artifact, its delivery message names the URL and states in one line that the Editor share is
an outstanding manual step. A session that publishes and stays silent about the share has not
followed this rule.

## How they relate

- Finishing work another session picks up: Behavior 1 (tail), plus Behavior 3 if you can write their bridge.
- Anything needing a human judgment: Behavior 2 (card in file AND summary), closing with the `Decision needed:` tail.
- One result feeding several sessions: Behavior 4 (fan-out), opening with Behavior 5's carried-forward line.
- Recording what went out and what landed: Behavior 5, on the seat's own registered ledger.
- Housekeeping before a register refresh: the optional lint.

## Anti-patterns to avoid

- Omitting the codename, the baton ID, the timestamp, the `to SESSION-NAME #Codename` opener, or the signature. Each is load-bearing for a different question asked later.
- Merging more than one target into a single baton ID or a single fenced block; a fan-out is sequential IDs, each self-contained.
- Omitting the `re:` line on a reply or ack.
- Putting the baton ID line or the `Sent by` signature outside the fenced block; a copied block must carry its own provenance.
- Guessing or estimating the timestamp, or printing one without its zone.
- **Marking a baton EMITTED when its block never made it into the response.**
- Burying the next action mid-response instead of in the tail.
- Surfacing a decision without its card, or writing the card without summarising it in the response.
- A pointer baton with no recap, paths, task and done-looks-like.
- Writing a bridge baton into a target you lack write access to, or asserting a target's status from memory rather than re-reading its bridge.
- Amending a Current Instruction whose baton has already been consumed.
- Emitting a fan-out without dependencies and send order, or without the carried-forward line.
- Writing to a ledger you are not the registered writer for, or to a hardcoded path.
- Leaving a ruling in the chat instead of propagating it the same turn.
- Presenting an API list-price equivalent as SPEND on a subscription estate. Nothing was billed at those rates.
  Lead with plan share (percent of the session and weekly allowance consumed); if a list-price figure appears at
  all, label it explicitly as a benchmark, never as cost incurred.
- Em dashes or AI-tone phrasing; batons are artifacts other sessions read.
- A workspace-relative markdown link inside a paste-ready block, your own folder name prefixed onto a relative link, `../`, percent-encoding, angle brackets, or a `file:`/`vscode:` URI.

## Test triggers

Examples that SHOULD fire this skill:

- "I'm done here; write the baton to hand this to APP-DEV."
- "Fan this out: DATA-SME validates, then APP-DEV and PQREV in parallel, then APP-ARCH signs off."
- "This needs the orchestrator's call" or "surface this decision."
- "Emit the next-prompt tail for this, and write it into the target's bridge if you can."
- "Log this baton to the ledger" or "mark BATON-0904-12 as delivered."

Examples that should NOT fire this skill:

- "Write a T-number implementation ask for the Developer." (that is `architect-to-developer-ask-authoring`)
- "Stand up a new subordinate session." (that is `bridge-handoff-authoring`)
- "What changed in my watched docs?" (that is `live-source-watch`)
