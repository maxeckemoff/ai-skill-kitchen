# cowork-progressive-disclosure-helper

A Claude Cowork skill that replaces surprise automatic compaction with deliberate, role-aware session management. When a session approaches context pressure or hits a natural break point, the skill alerts you with a structured heads-up and walks you through a six-level intervention ladder that includes dispatching scopes as role-assigned subordinate sessions with proper bridge file scaffolding.

## Why it exists

Cowork's default behavior at context limits is to silently summarize earlier messages into an opaque compressed form. You lose control over what survives. For high-fidelity work (tax, compliance, data analysis, anything where specific facts matter) automatic compaction can drop the wrong details.

This skill flips the model: you stay informed about pressure and choose what to preserve, summarize, or dispatch as a properly-scoped subordinate session.

## What progressive disclosure means here

The skill generalizes progressive disclosure beyond its classical UX definition. Three layers operate simultaneously:

1. **Within a session**: skills, memory files, and tool definitions load on demand.
2. **Across sessions**: bridge files act as the disclosure interface between sessions.
3. **Within a domain**: role specialization (Architect, Developer, Schema Expert, etc.) so no single session carries the union of all expertise.

The skill operates at layers 2 and 3, helping you produce the right bridge or spawn the right new subordinate when a scope is ready to leave the current session.

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

**Level 3: Dispatch to a subordinate.** One scope spins off into a role-assigned su