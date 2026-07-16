---
name: relay-baton
description: "Produces the ThreadOps relay artifacts that pass next-action state between Cowork sessions. Use when a session finishes work another session must pick up, or the user says write the baton, hand this off, relay to the next session, emit the next-prompt tail, or fan this out. Three behaviors: (1) the standing response-tail baton in one of three forms (Next prompt with a paste-ready block for a named target session; Decision needed for the Human Orchestrator; or Thread terminal marking a codename done); (2) bridge batons written into the target session's Current Instruction when the sender has write access, otherwise handed to the Human Orchestrator via the tail; (3) PQREV-style fan-out sequences, numbered and dependency-ordered, one block per target with send order stated and the thread codename on every block. Includes an optional thread-tag-hygiene lint step that flags bridge entries missing their codename."
---

# Relay baton

The org's substrate is pull-based: files do not push, sessions act only when prompted. The relay baton is how a session hands the next action to whoever must act next, in a form that is paste-ready and logged, so threads do not stall silently. This skill emits the three ThreadOps relay artifacts (per the 2026-07-08 ThreadOps ruling, section 5) and, optionally, lints bridge entries for the codename hygiene that makes threads greppable.

These three behaviors are one verb (pass the baton), sharing the codename and baton format, so they live in one skill. The thread-tag-hygiene lint is folded in as an optional step, not a separate skill, per the kitchen-sprawl guidance.

## The codename convention (used by every artifact here)

Every tracked cross-session thread has a codename: `#PROJECT_TopicCamelCase` (for example `#VATR_CustRefundStmt`, `#ORG_HHHRealign`), minted at thread birth by the spawning session. The rule: every bridge entry that advances a tracked thread, and every baton block this skill emits, carries the codename. That is what makes tracking nearly free, `rg "#VATR_CustRefundStmt"` across the Projects tree reconstructs the whole thread. If a thread has no codename yet, mint one before emitting a baton.

## Behavior 1: the response-tail baton (standing rule)

End the response with exactly one of these three forms:

- `Next prompt: [TARGET-ID] #CODENAME` followed by a paste-ready block the user can drop straight into the target session.
- `Decision needed: <what is being decided> [Human Orchestrator]` when the next step is a human judgment call.
- `Thread terminal: #CODENAME DONE, notify register` when the thread is finished.

The paste-ready block under a Next prompt is a complete instruction the target can act on without hunting for context: what to do, the concrete inputs (paths, IDs), and the expected deliverable. One tail per response; if several threads advanced, lead with the most urgent and note the others.

## Behavior 2: the bridge baton

When the sender has write access to the target's bridge, do not just hand the baton to the Human Orchestrator, ALSO write it into the target's `## Current Instruction` section. The receiving session picks it up on its bridge-freshness re-read (see the bridge-freshness rule), so the Human Orchestrator's paste shrinks to "check your bridge." Steps:

1. Confirm write access to the target bridge and its path.
2. Replace the target's Current Instruction with the baton: the paste-ready ask, tagged with `#CODENAME`, signed by the sender with the date.
3. In the response tail, point the Human Orchestrator at it: `Next prompt: [TARGET-ID] #CODENAME - baton written to its bridge Current Instruction; tell it to re-read its bridge.`

Where no write access to the target bridge exists, the response tail carries the full baton block for the Human Orchestrator to paste directly. Never leave a baton only in your own head or buried mid-response.

## Behavior 3: fan-out sequences (the PQREV pattern)

When one result feeds several sessions, emit a numbered, dependency-ordered sequence, one block per target, parallel-safe steps marked, and the send order stated. Template:

```
Fan-out: #CODENAME
Send order: 1, then 2 and 3 in parallel, then 4

1. [TARGET-A] (no deps) #CODENAME
   <paste-ready block>
2. [TARGET-B] (after 1) #CODENAME
   <paste-ready block>
3. [TARGET-C] (after 1, parallel with 2) #CODENAME
   <paste-ready block>
4. [TARGET-D] (after 2 and 3) #CODENAME
   <paste-ready block>
```

State dependencies explicitly so the Human Orchestrator knows what can fire now and what waits. Mark which steps are parallel-safe. Every block carries the codename.

## Optional step: thread-tag-hygiene lint

When asked to check tag hygiene, or before a register sweep, scan recent bridge Activity Log entries and flag any that advance a tracked thread but omit its `#codename`. A cheap check: `rg -n "#\w+_[A-Za-z]" <bridge>` shows which entries are tagged; entries that clearly advance a known thread but have no tag are the misses. Output a short list: file, entry date, the codename that should be added. Do not edit the entries silently; propose the additions and let the owner apply them. This keeps `rg`-based thread reconstruction reliable.

## How the three relate

- Finishing a piece of work that one other session must pick up: Behavior 1 (tail), plus Behavior 2 if you can write their bridge.
- One result feeding several sessions: Behavior 3 (fan-out).
- Housekeeping before a register refresh: the optional lint.

## Anti-patterns to avoid

- Do not omit the codename from a baton or fan-out block; untagged threads fall out of `rg` reconstruction.
- Do not bury the next action mid-response; it goes in the tail (and the target bridge when possible).
- Do not write a bridge baton into a target you lack write access to; hand it to the Human Orchestrator via the tail instead.
- Do not silently rewrite bridge entries during the lint; propose the codename additions.
- Do not emit a fan-out without stating dependencies and send order; an unordered list is not a relay.
- Do not use em dashes or AI-tone phrasing in batons or tails; they are artifacts the Human Orchestrator and other sessions read.

## Test triggers

Examples that SHOULD fire this skill:

- "I'm done here; write the baton to hand this to VAT-DEV."
- "Fan this out: BI-ZOHO validates, then VAT-DEV and PQREV in parallel, then VAT-ARCH signs off."
- "Emit the next-prompt tail for this, and write it into the target's bridge if you can."

Examples that should NOT fire this skill:

- "Write a T-number implementation ask for the Developer." (that is `architect-to-developer-ask-authoring`; a relay baton routes an existing next-action, it does not author the implementation spec)
- "Stand up a new subordinate session." (that is `bridge-handoff-authoring`)
- "What changed in my watched docs?" (that is `live-source-watch`)
