---
name: bridge-handoff-authoring
description: Scaffolds the warm-transfer kickoff prompt and initial bridge file for a new Cowork subordinate session in a multi-session architecture (Manager, Architect, Developer, Coder, Schema Expert, Subordinate specialists). Use when the user is about to spawn a new subordinate, or says "spawn a new sub", "kickoff", "kickoff prompt", "warm transfer", "subordinate prompt", "handoff to a new session", "stand up a Developer", "new specialist session", or similar. Produces a paste-ready first message for the new session covering role assignment, bridge path, scope, dataset orientation, role-specific recipes, expected first response, and the standing rules to load immediately. Also produces the initial bridge file template if one does not yet exist. Distinguishes rules that propagate across all sessions from scope-specific rules that belong only in this bridge.
---

# Bridge handoff authoring

Every time a new subordinate session is spun up, someone has to write the warm-transfer kickoff prompt: role, scope, dataset orientation, recipes, expected first response, standing rules to load. The shape is identical across cases. This skill scaffolds that prompt and, if needed, the initial bridge file the new session will read.

This skill produces two artifacts:

1. The **kickoff prompt** the user pastes as the new subordinate's first message.
2. The **initial bridge file** the kickoff prompt points the subordinate at (only if it does not already exist).

This skill assumes the user's documented multi-session architecture. It is a sibling of `cowork-progressive-disclosure-helper` (which decides *when* to split) and `pre-launch-warm-transfer-review` (which reviews the drafted prompt before launch). This skill's job is to *author* the prompt and bridge cleanly the first time.

## Step 1: Determine the role

Before writing anything, decide what role the new subordinate should hold. Ask the user if it is not obvious. Use these heuristics:

- **Architect** for design-heavy work: specifying, scoping, deciding between approaches, reviewing trade-offs. Deliverable is a spec or rationale, not running code.
- **Developer** for execution-heavy work: implementing, running shell commands, executing SQL, editing and testing production files. Deliverable is changed state in the workspace or production.
- **Coder** for one-off scripting or prototype iteration. Less ceremony than Developer; no long-lived memory expectation.
- **Schema Expert** for canonical reference work: column inventories, table schemas, helper-table layouts that other sessions consult. Read-mostly; updates on triggers like "user re-exported the production code."
- **Subordinate specialist** for a recurring domain (FP&A Projection, FP&A Payroll, Comms Analyst, etc.) that owns one piece of the user's work and operates in tightly fenced scope.
- **A new specialist** if the scope is a genuinely new long-lived domain none of the above covers. Name it after the domain, not the task.

If the scope does not clearly recur, flag that a subordinate may be overkill and a one-off in the current session might be cheaper. The launch overhead only pays back for scopes that recur and accumulate expertise.

## Step 1b: Assign the sidebar identity code

Every subordinate needs a stable identity so the org chart stays legible in the session list and so the session knows who it is and who it talks to. Assign a short PROJECT-ROLE code plus a task name.

- **Code format**: `PROJECT-ROLE`, uppercase and hyphenated. The project part is a short abbreviation of the project or org group; the role part abbreviates the role from Step 1. Examples: `VAT-DEV` (Maintain VAT Engine, Developer), `VAT-ARCH` (Architect), `GCP-DEV` (Deploy GCP BI Suite, Developer), `FPA-PROJ-ENG` (FP&A Projection, Engineer), `SKL-BLD` (Skill Builder). Keep it short enough to read at a glance.
- **Sidebar label**: `CODE - short task name`, for example `VAT-DEV - consolidate TrimOrNull helpers`. The code leads so sessions scan and sort by identity.
- Derive the code from session context (the project plus the role from Step 1). If the project abbreviation is not obvious, ask the user or check the session registry.

A note on mechanism: a Cowork session's sidebar label is set by the user, not by the session itself. As of this writing a session cannot reliably rename its own sidebar entry from its first prompt; if that capability is confirmed later, this skill can lean on it. So this skill does two things instead: it embeds the identity code inside the kickoff prompt (so the session knows its own ID and signs bridge entries with it), and it gives the user a copy-pastable rename instruction for the sidebar label.

## Step 2: Gather the orientation inputs

A good kickoff prompt is concrete. Collect (or ask the user for) these before drafting:

- **Scope statement**: the one bounded responsibility this session owns, in one or two sentences.
- **Bridge file path**: where the bidirectional channel lives. Default convention: `_plans/handoff/[Descriptive_Name]_Bridge.md`, or wherever the user's existing bridges sit. Match the existing convention if other bridges exist.
- **Dataset orientation**: concrete file paths, project IDs, connector names, table names, VM names, the actual artifacts this session will touch. Vague references ("the data") are a failure mode; name the paths.
- **Recipes / recurring patterns**: role-specific procedures this session will repeat. A Developer gets defensive-coding gotchas and the check-off expectation; an FP&A specialist gets the model's tab layout and refresh cadence; a Schema Expert gets the re-audit trigger.
- **Expected first response**: what the subordinate should produce or confirm on its first turn, so the user knows the handoff landed.
- **Standing rules to load immediately**: see Step 4.

If any of these are missing and you cannot infer them, ask the user rather than inventing them.

## Step 3: Scaffold the kickoff prompt

Produce a paste-ready prompt in this shape. Fill every bracket; delete any line that genuinely does not apply rather than leaving an empty placeholder.

```
You are [CODE], the [role] subordinate for [scope description].

The Manager has set up a bridge file at [bridge path]. Read it now in full. The "Current Instruction" section is your active ask. Append timestamped entries to "Activity Log" (newest at top, signed [CODE]). Surface decisions you need from the Manager to "Open Questions". Treat "Standing Rules" as load-bearing.

Scope: [the one bounded responsibility this session owns; what is explicitly out of scope].

Dataset orientation:
- [concrete path / project ID / connector / table / VM the session will touch]
- [another]

Recipes for this role:
- [role-specific recurring procedure or gotcha]
- [another]

Standing rules to follow immediately:
- [explicit rule, e.g. tone, versioning, defensive coding, file-edit protocol]
- [another]

Expected first response: [what to produce or confirm on turn 1 so the Manager knows the handoff landed].

On session start: read [bridge path] and execute the Current Instruction. If anything is ambiguous, append to Open Questions and stop rather than guessing.
```

After the kickoff prompt, give the user the rename step so the sidebar matches the embedded identity:

> Rename the new session's sidebar label to: `[CODE] - [short task name]`

### Role-specific kickoff tailoring

- **Architect**: emphasize that deliverables are specs and decision rationales written to the bridge or a plan doc, not direct edits to production files. Include the canonical sources the Architect must consult before designing.
- **Developer**: emphasize the execution loop (read instruction, execute, log outcome to Activity Log, surface blockers to Open Questions). Include the check-off expectation: production integration goes through the user's manual check-off, not direct edits to fenced files. Point to `architect-to-developer-ask-authoring` as the format the incoming asks will arrive in.
- **Coder**: keep it lean. One task, expected output, where to drop it. No memory or audit-trail ceremony.
- **Schema Expert**: state the re-audit trigger ("when the user re-exports the production code, re-read and refresh the canonical doc") and which doc is canonical.
- **Subordinate specialist**: include the lazy-load instruction if the reference folder is large (do not ingest everything on turn 1; load reference materials only when a task needs them, to preserve the first turn's context budget).

## Step 4: Separate propagating rules from scope-specific rules

Two classes of standing rules exist. Put them in the right place.

**Propagating rules** apply to every session the user runs. These live in user-level auto-memory and propagate to sessions launched in the same workspace, so you do not need to restate them in every bridge. Examples: no em dashes, no obvious AI tone, fact-check load-bearing claims, ask before guessing when stakes are high. Mention in the kickoff that these apply, but the bridge's Standing Rules section should not be padded with them.

**Scope-specific rules** apply only to this subordinate's domain. These belong in the bridge's Standing Rules section. Examples: a file-edit protocol for one project, a versioning convention for one set of files, a defensive-coding pattern for one engine, a refresh cadence for one model.

If you are unsure whether a rule propagates, ask the user. Do not duplicate a propagating rule into the bridge just to be safe; duplication is a documented maintenance cost (every copy has to be updated when the rule changes).

## Step 5: Produce the initial bridge file (if it does not exist)

If the bridge file the kickoff points to does not yet exist, scaffold it in the user's documented format:

```markdown
# Bridge: [Manager session name] <-> [Subordinate role and scope]

## Current Instruction
[The one active ask the subordinate works on first. Replaced with each new directive.]

## Activity Log
[Newest at top. Each entry signed [Manager] or [Subordinate role name], with timestamp, command summary, outcome, key findings. Do not dump unbounded output; sample or link to a saved file.]

## Open Questions
[The subordinate appends here when it needs a Manager decision before proceeding.]

## Standing Rules
[Scope-specific decisions and conventions only. Treat as load-bearing.]

## Canonical Sources
[Pointers to permanent reference docs the subordinate should consult: schema files, plan documents, OPEN_TOPICS.md, dataset locations.]
```

Seed the Current Instruction with the first ask, the Standing Rules with the scope-specific rules from Step 4, and the Canonical Sources with the concrete paths from Step 2. Leave Activity Log and Open Questions empty for the subordinate to fill.

Save the bridge to the path from Step 2. If other bridges exist and there is an index (`_plans/handoff/_INDEX.md` or similar), offer to add a one-line entry for the new bridge.

## Anti-patterns to avoid

- Do not produce a kickoff prompt with unfilled brackets or vague dataset references. Concrete paths and IDs are the whole point.
- Do not pad the bridge's Standing Rules with propagating rules that already live in user-level memory.
- Do not spin up a subordinate for a scope that does not recur. Flag the overhead instead.
- Do not invent dataset paths, project IDs, or conventions. Ask if you cannot infer them.
- Do not write the kickoff in a tone that violates the user's distribution rules (no em dashes, no AI-tone giveaways), since the prompt is itself an artifact the user reads and reuses.

## Handing off to the reviewer

After producing the kickoff prompt, offer to run it through `pre-launch-warm-transfer-review` before the user launches the session, if that skill is installed. The reviewer checks completeness, tone-rule presence, dataset specificity, and open-question framing, and returns a pass / needs-revision verdict.

## Test triggers

Examples that SHOULD fire this skill:

- "I'm about to spin up a new Developer session for the BI migration. Write me the kickoff prompt and bridge."
- "Give me a warm-transfer prompt for a new FP&A Payroll specialist subordinate."
- "Handing this off to a fresh session. Scaffold the subordinate prompt and the initial bridge file."

Examples that should NOT fire this skill:

- "What's the status of the Developer's current task?" (querying an existing session, not standing up a new one)
- "Review this kickoff prompt before I launch it." (that is `pre-launch-warm-transfer-review`)
- "Write a T-number ask for the Developer." (that is `architect-to-developer-ask-authoring`; the Developer session already exists)
