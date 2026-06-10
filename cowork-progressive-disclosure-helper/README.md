# cowork-progressive-disclosure-helper

A Claude Cowork skill that replaces surprise automatic compaction with deliberate, role-aware session management. When a session approaches context pressure or hits a natural break point, the skill alerts you with a structured heads-up and walks you through a six-level intervention ladder that includes dispatching scopes as role-assigned subordinate sessions with proper bridge file scaffolding.

## Why it exists

Cowork's default behavior at context limits is to silently summarize earlier messages into an opaque compressed form. You lose control over what survives. For high-fidelity work (tax, compliance, data analysis, anything where specific facts matter) automatic compaction can drop the wrong details.

This skill flips the model: you stay informed about pressure and choose what to preserve, summarize, or dispatch as a properly-scoped subordinate session.

## What progressive disclosure means here

Progressive disclosure in this skill's operating model means the deliberate practice of splitting work into delineated "virtual employees" (Manager, Architect, Developer, Coder, Schema Expert, Subordinate specialists), each with its own Cowork session and context budget, coordinating through shared markdown files called bridges. It is NOT in-session iteration in a single chat. Iterating turn by turn in one window is the baseline use of Claude AI; progressive disclosure is the architecture that comes after you have outgrown the single window and started running an org chart.

Two finer-grained disclosure mechanics also operate within this pattern (skills and memory load on demand inside any one session; role specialization means no single session carries the union of all expertise). But the load-bearing meaning is the virtual-employee orchestration via bridges. This skill is the operating-system level helper for that practice.

## The role vocabulary

The skill knows the documented multi-session role pattern:

- **Manager**: parent session that holds cross-domain context and dispatches to subordinates
- **Architect**: designs and reviews; deliverables are specs and rationales
- **Developer**: executes; deliverables are changed files, runs, tests
- **Coder**: narrower Developer scope for one-offs
- **Schema Expert**: maintains canonical reference docs
- **Subordinate specialist**: domain expert (FP&A Projection, Comms Analyst, etc.)

When the skill proposes a Level 3, 4, or 5 split, it suggests appropriate roles for each subordinate rather than leaving role assignment vague.

## How alerting works

The skill fires at four escalating thresholds (~50%, ~65%, ~80%, ~90% of estimated context usage), plus on activity triggers (heavy tool calls, multiple file reads, large web fetches) and natural transition triggers (topic shifts, completed deliverables, scope changes ready for dispatch). It fires each threshold only once per session to avoid being noisy.

You can also invoke it explicitly by asking about context, compaction, session length, bifurcation, subordinate dispatch, or bridges.

## The six-level intervention ladder

**Level 0: Continue.** Do nothing. Accept eventual auto-compaction. Best when pressure is moderate and you're mid-task.

**Level 1: Inline recap.** A 3-to-5 sentence "where we are" snapshot appended to the response. Not saved externally. Best at the first alert threshold (~50%).

**Level 2: External checkpoint.** A structured state summary you save outside the session (memory markdown, OPEN_TOPICS append, project notes). The work continues in place. Best at milestone moments.

**Level 3: Dispatch to a subordinate.** One scope spins off into a role-assigned subordinate session (Architect, Developer, Coder, or specialist) via a bridge file in the documented format. The current session continues. Best when one sub-task has matured enough to belong in dedicated context.

**Level 4: Multi-way decomposition.** The session decomposes into a Manager that retains only cross-domain orchestration plus N role-assigned subordinates, each with their own bridge file. The Manager keeps a compact index. Best when several scopes have accumulated.

**Level 5: Full reorganization.** The current session becomes donor material. A fresh org chart is started with a new Manager and initial subordinates spun up against fresh bridges. Best when the session has drifted across many concerns.

You can blend levels (e.g., "Level 1 recap now plus Level 3 dispatch to a Developer for the BI thread").

## Bridge file format

The skill produces bridge files in the user's documented convention:

```markdown
# Bridge: [Manager session name] <-> [Subordinate role and scope]

## Current Instruction
[The one active ask the subordinate works on next.]

## Activity Log
[Newest at top, signed by author with [Manager] or [Subordinate role name].]

## Open Questions
[Subordinate appends here when needing a Manager decision.]

## Standing Rules
[Accumulated scope-specific decisions and conventions.]

## Canonical Sources
[Pointers to permanent reference docs.]
```

## Progressive disclosure within splits

When you pick Level 3, 4, or 5, the skill walks you through four stages rather than jumping straight to producing documents:

1. **Scope inventory**: confirm or refine the list of scopes detected.
2. **Dispatch proposal**: which scopes go where, what roles each subordinate gets.
3. **Refinement**: you adjust roles, merge or drop, add subordinates.
4. **Execute**: bridge files produced, plus Manager-side index for Level 4, plus kickoff messages for new subordinates.

## Sibling skills

This skill is one of several in a multi-session architecture toolkit:

- `bridge-handoff-authoring`: scaffolds the warm-transfer kickoff prompt
- `architect-to-developer-ask-authoring`: produces T-number-style asks in the documented format
- `pre-launch-warm-transfer-review`: reviews a warm-transfer prompt before launch
- `check-off-protocol`: standardizes post-integration sequence

If those skills are installed, this skill defers to them for deeper work in their domains.

## Suspending alerts

If you want to handle context manually without further alerts, say "stop alerting me" or "I'll handle context" and the skill will suspend for the rest of the session.

## Compatibility

Works in any Cowork session. No external dependencies, no scripts, no API calls. The skill is purely instructions for how Claude should monitor, alert, and produce bridge artifacts.
