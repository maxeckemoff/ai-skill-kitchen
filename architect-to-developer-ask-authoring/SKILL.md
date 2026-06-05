---
name: architect-to-developer-ask-authoring
description: "Produces a structured implementation ask from an Architect session to a Developer subordinate, written into the Architect-to-Developer bridge file's Current Instruction section in the user's documented T-number convention. Use when an Architect needs to hand work to a Developer, or the user says 'T-number ask', 'write a Developer ask', 'Architect to Developer', 'scope this refactor', 'implementation ask', 'spec this for the Developer', or similar. Each ask carries a consistent skeleton: T-number and title, scope statement, semantic constraints, in-scope files, out-of-scope files, deliverable format, and recommended OPEN_TOPICS update wording for after the Developer integrates. Helps decide what belongs in scope versus out, and picks a deliverable format suited to the ask type."
---

# Architect-to-Developer ask authoring

An Architect session designs and scopes work; a Developer subordinate implements it. The hand-off is an *ask* written into the Architect-to-Developer bridge file's Current Instruction section. The asks follow a consistent shape so the Developer always knows where to find scope, constraints, and the expected deliverable. This skill turns a freeform description of intended work into that structured ask.

This is a sibling of `bridge-handoff-authoring` (which stands up the Developer session in the first place) and `check-off-protocol` (which handles what happens after the Developer delivers and the user integrates). This skill governs the steady-state asks that flow across an already-established Architect-to-Developer bridge.

## The ask skeleton

Every ask written to the bridge's Current Instruction uses this skeleton. Fill each section; omit a section only when it genuinely does not apply, and say so explicitly rather than leaving it blank.

```markdown
## Current Instruction

**[T-number]: [Short imperative title]**

**Scope:** [One or two sentences: what to change and why. The Developer should be able to read only this and know the goal.]

**Semantic constraints:**
- [A rule the implementation must preserve, e.g. "output schema must not change", "null handling stays identical", "no new external dependencies"]
- [Another]

**In scope (files / objects the Developer may touch):**
- [explicit path or object]
- [another]

**Out of scope (do not touch):**
- [explicit path or object the Developer must leave alone, and why]
- [another]

**Deliverable format:** [What the Developer hands back and where: a diff, a rewritten file in a scratch location, a test result, a summary in the Activity Log. Be specific.]

**Recommended OPEN_TOPICS update (for after integration):**
> [Pre-written wording the Manager can paste into OPEN_TOPICS.md once the user confirms integration, including any version marker.]
```

## The T-number convention

The user references asks by a T-number (a ticket-style identifier such as `T-041`). Use it so asks are addressable across the bridge's Activity Log and in OPEN_TOPICS.

- If the user supplies a T-number, use it verbatim.
- If they do not, look at the bridge's Activity Log and OPEN_TOPICS for the highest existing T-number and increment. Surface the number you assigned so the user can correct it.
- If no numbering scheme is in use yet, propose starting at `T-001` and confirm before adopting it.

Keep the title short and imperative: "Consolidate the TrimOrNull helper", not "This ask is about consolidating helpers".

## Writing the scope statement

The scope statement is the load-bearing sentence. A Developer reading only the scope should understand the goal without reading the rest. Good scope statements name the change and the reason: "Replace the 77 inline TrimOrNull definitions with a single shared helper query, to remove the duplicate-helper maintenance burden." Avoid scope statements that only name a symptom ("fix the helpers") or that bury the goal in constraints.

## Choosing semantic constraints

Semantic constraints are the invariants the implementation must not break. They are what lets the Architect delegate execution without re-reviewing every line. Common constraint types:

- **Behavior-preserving**: output schema, row count, null handling, sort order, or numeric results must be identical before and after.
- **Dependency**: no new external packages, no new connectors, no new helper tables without the loud-failure guard.
- **Convention**: follow the project's versioning header, naming convention, or defensive-coding pattern.
- **Performance**: no change that materially increases refresh time, or a specific buffering requirement.
- **Boundary**: the change must be self-contained to the in-scope files and must not require edits elsewhere.

State constraints as testable assertions where possible, so the Developer can verify them ("row count unchanged", not "be careful with rows").

## Deciding in scope versus out of scope

Be explicit about both. The out-of-scope list is as important as the in-scope list, because it prevents scope creep and protects fenced files.

- **In scope**: the specific files or objects the Developer may edit. Name them by path. If the Developer should create new files, say where.
- **Out of scope**: files the Developer must not touch even if they look related. Include the reason ("these go through the user's manual check-off protocol, not direct edit"; "this is owned by the Schema Expert"). When a project has files that change only through a human integration step, list them here every time.

If you cannot enumerate the in-scope or out-of-scope files because you lack the project layout, ask rather than guessing. A wrong out-of-scope list is worse than asking.

## Choosing a deliverable format by ask type

Match the deliverable to the work:

- **Refactor / edit of existing code**: a diff, or the rewritten file saved to a scratch location for the user's manual integration. Specify which, and where the scratch file goes.
- **New script or one-off**: the script file plus a one-line run command and expected output.
- **Investigation / diagnosis**: a written findings summary in the Activity Log (or a linked file if long), not changed code.
- **Test or verification**: the command run, the result, and a pass/fail statement.
- **Data operation (SQL, migration)**: the statements run, row counts affected, and a before/after sample.

Always state where the deliverable lands and how the user will consume it. For projects where the user integrates manually, the deliverable is a reviewable artifact in a scratch location, never a direct edit to a fenced production file.

## Pre-writing the OPEN_TOPICS update

Because the user runs a manual integration step, pre-write the wording the Manager will paste into OPEN_TOPICS.md once the user confirms the change is live. This saves a round-trip later and keeps the permanent record consistent. Include any version marker the project uses (semver bump, dated entry). Phrase it as a completed-state record: "T-041: TrimOrNull consolidated into shared helper (was 77 inline copies). Integrated [date]. vX.Y.Z." The `check-off-protocol` skill consumes this wording at integration time.

## Anti-patterns to avoid

- Do not write an ask with a vague scope statement that forces the Developer to reverse-engineer the goal from the constraints.
- Do not omit the out-of-scope list. Silence is read as permission.
- Do not invent file paths or T-numbers. Inspect the bridge and OPEN_TOPICS, or ask.
- Do not specify a deliverable that edits a fenced production file directly when the project uses manual integration.
- Do not use em dashes or AI-tone phrasing; the ask is an artifact the user reads and the Developer consumes.

## Writing the ask to the bridge

Place the finished ask in the Current Instruction section of the Architect-to-Developer bridge, replacing the prior instruction (the prior one should already be reflected in the Activity Log and OPEN_TOPICS if resolved). Do not append a new ask below an unresolved one without flagging the collision to the user; the Current Instruction section holds one active ask at a time by convention.
