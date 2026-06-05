# architect-to-developer-ask-authoring

A Claude Cowork skill that turns a freeform description of intended work into a structured implementation ask, written into the Architect-to-Developer bridge file in a consistent, ticket-numbered format.

## Why it exists

In a multi-session architecture, an Architect session designs work and a Developer session implements it. The hand-off is an *ask* placed in the bridge file. When asks are written ad hoc, the Developer has to hunt for the scope, guess what is off-limits, and infer what to hand back. This skill enforces one skeleton for every ask, so the Developer always finds scope, constraints, file boundaries, and the expected deliverable in the same place.

## The ask skeleton

Every ask carries the same sections:

- **T-number and title**: a ticket-style identifier and a short imperative title
- **Scope**: one or two sentences stating the change and the reason
- **Semantic constraints**: the invariants the implementation must not break
- **In scope**: the files or objects the Developer may touch
- **Out of scope**: the files the Developer must leave alone, with reasons
- **Deliverable format**: what the Developer hands back and where
- **Recommended OPEN_TOPICS update**: pre-written wording for after integration

## What the skill helps with

- **T-numbering**: uses a supplied number, or increments from the highest existing one in the bridge and OPEN_TOPICS.
- **Scope discipline**: insists on a load-bearing scope sentence and an explicit out-of-scope list, since silence reads as permission.
- **Constraint typing**: offers common constraint categories (behavior-preserving, dependency, convention, performance, boundary) and pushes for testable assertions.
- **Deliverable matching**: picks a deliverable format suited to the ask type (refactor, new script, investigation, test, data operation), and respects manual-integration projects by never asking for a direct edit to a fenced file.
- **Forward-wiring the record**: pre-writes the OPEN_TOPICS entry so integration later is a paste, not a re-derivation.

## How it fits with the sibling skills

- `bridge-handoff-authoring` stands up the Developer session and its bridge.
- `architect-to-developer-ask-authoring` (this skill) writes the steady-state asks across that bridge.
- `check-off-protocol` consumes the pre-written OPEN_TOPICS wording when the user confirms integration.
- `pre-launch-warm-transfer-review` and `cowork-progressive-disclosure-helper` cover session launch and context management.

## Compatibility

Works in any Cowork session. No external dependencies, no scripts, no API calls. Pure instructions for how Claude should author the ask.

## License

MIT.
