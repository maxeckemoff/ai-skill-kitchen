---
name: relay-baton-codex
description: Create portable Codex task handoffs with generated native session signatures, self-contained baton blocks, explicit provenance, and durable send-state tracking. Use when handing work to another Codex task, drafting a next prompt, or recording whether a handoff was only drafted, persisted, or delivered.
---

# Relay Baton for Codex

Use this skill for handoffs between Codex tasks. It is self-contained and has no external project-canon dependency.

## Native session signature

Immediately before a substantive final response, run the bundled generator:

```text
python <this-skill-directory>/scripts/codex_session_signature.py --seat <assigned-seat>
```

If `CODEX_THREAD_ID` or `CODEX_SESSION_ID` is unavailable, pass the current native Codex task UUID with `--session`. Preserve the assigned seat or task identity. Include the generated FULL output without hand-editing its metrics or truncating prompt rows. Use `--condensed` only when the user explicitly requests it.

The FULL output keeps this field order:

1. identity, task ID, capacity, turn, compactions, and native prompt runs
2. `last`, for the latest native prompt run
3. `cumulat.`, without a cost field
4. `context`, using the latest request snapshot and actual runtime window
5. `plan`, using the account windows actually available
6. `benchmark`, clearly labeled as Standard API equivalent rather than spend
7. `tools`
8. uncapped `prompts`, newest first
9. `caveats`
10. timezone-stamped completion line

Missing telemetry stays unavailable. Do not turn missing values into zero. Credit units are not dollars. Cumulative tokens are not current context occupancy. Benchmark rates currently support Astra only; for any other model the benchmark remains unavailable. Account meters may remain unavailable unless the user's own native snapshot is present.

Codex does not separately charge for cache writes. The renderer therefore shows `cache-write n/a*`, while preserving any raw reported `cache_write_input_tokens` count in caveats and JSON. It labels noncache input as total input minus cache reads; a reported write subset stays within that noncache amount. The Standard API benchmark prices reported token categories only, may omit unreported cache creation, and is neither Codex credit usage nor billed spend. A published API cache-retention minimum is not a measured TTL for a Codex task, so task TTL remains unavailable unless directly observed.

The generator reads native Codex rollout records. Never substitute imported conversation metrics or another task's ID. On Windows, install the Python `tzdata` package if `zoneinfo` cannot load `America/New_York`.

## Handoff baton

Use one target per baton ID and one fenced block per target. A copied block must retain its identity, time, sender, destination, task, and evidence without relying on surrounding prose.

Use IDs in the form `<SENDER>-<MMDD>-<NN>`, sequential within the sender's day. Read the clock and include its zone. Replies add a `re:` line directly below the baton ID.

```text
[BATON <SENDER>-<MMDD>-<NN>]  <YYYY-MM-DD HH:MM ZONE>
re: <BATON-ID being answered>   (replies only)

  to <TARGET-TASK> #<THREAD-TAG>
      <brief recap and verified current state>
      <exact files or IDs needed by the recipient>
      <imperative next action>
      Done looks like: <observable result>.

  Sent by <SENDER>, <YYYY-MM-DD HH:MM ZONE>
```

The baton ID line and `Sent by` line belong inside the fence. For several recipients, create separate sequential IDs and state the dependency order outside the blocks.

## Provenance and persistence

Showing a baton in a response does not prove it was sent. Track the state honestly:

- `DRAFTED`: composed or displayed, but no durable retrievable copy exists.
- `EMITTED`: displayed and persisted verbatim in a recipient-owned instruction file or a sender-owned outbox.
- `DELIVERED`: the recipient supplied a reply or action receipt that cites the baton or otherwise establishes delivery.
- `SUPERSEDED`: replaced before action.
- `STALE`: no delivery evidence after the sender's chosen follow-up interval.

Use a sender-owned ledger and outbox in a location chosen for the project. Do not hardcode a global registry or another user's directory. Write only files the current task owns. A ledger row records the baton ID, timestamp, target, thread tag, ask, state, and durable-copy location.

Persist the exact baton block in the same turn before marking it `EMITTED`. A response-only baton remains `DRAFTED`. Do not claim external transmission merely because a prompt was prepared. Re-read recipient state before reissuing a stale baton.

## Final response tail

After the generated signature, use exactly one applicable tail:

- `Next prompt: <TARGET> #<THREAD-TAG>` followed by the self-contained baton block when another task should act.
- `Decision needed: <specific decision> [user]` when work requires the user's judgment; include enough context and options for the decision to stand alone.
- `Thread terminal: #<THREAD-TAG> DONE` when no work remains.

Do not add a new baton merely to acknowledge an informational receipt. A handoff is an action artifact, not decoration.
