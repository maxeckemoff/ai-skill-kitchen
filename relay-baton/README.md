# relay-baton

A Claude Cowork skill that produces the ThreadOps relay artifacts, the "baton" that passes next-action state from one session to whoever must act next, so cross-session threads do not stall silently.

## Why it exists

The multi-session substrate is pull-based: files do not push, sessions act only when prompted, and next actions live buried in each session's last response. Threads stall. The 2026-07-08 ThreadOps ruling made the baton org doctrine; this skill emits it in the right format every time.

## What it produces

1. **Response-tail baton** (standing rule): every response ends with one of three forms, `Next prompt:` (a named target plus a paste-ready block), `Decision needed: ... [Max]`, or `Thread terminal: #codename DONE`.
2. **Bridge baton**: when the sender can write the target's bridge, the baton is written into the target's Current Instruction, so the receiver picks it up on its bridge-freshness re-read and Max's paste shrinks to "check your bridge." Without write access, the tail carries it.
3. **Fan-out sequences** (the PQREV pattern): numbered, dependency-ordered, parallel-safe steps marked, one block per target with the send order stated.

Plus an optional **thread-tag-hygiene lint** that flags bridge entries missing their `#codename`, folded in as a step rather than a separate skill.

## The codename convention

Every tracked thread carries a codename (`#PROJECT_TopicCamelCase`) on every advancing bridge entry and every baton block, so `rg "#codename"` across the Projects tree reconstructs a whole thread. The skill applies it to every artifact it emits and the lint checks for it.

## How it fits

- `relay-baton` (this skill) routes an existing next-action between sessions.
- `architect-to-developer-ask-authoring` authors the implementation ask itself; `bridge-handoff-authoring` stands up a new session; `check-off-protocol` closes a delivery. relay-baton is the connective tissue between them.
- It relies on the bridge-freshness rule for the receiver to pick up a bridge baton.

## Compatibility

Works in any Cowork session. Writing a bridge baton needs write access to the target's bridge file; otherwise the baton rides the response tail. No new MCP.

## License

MIT.
