---
name: cowork-progressive-disclosure-helper
description: Monitors a Cowork session for context pressure and alerts before automatic compaction, then walks the user through a 6-level intervention ladder that includes role-aware multi-session moves (Manager, Architect, Developer, Schema Expert, Subordinate specialists) with bridge file scaffolding. Use whenever a session has run long, accumulated heavy tool calls or file reads, completed a sub-task, or when the user mentions context, compaction, tokens, session length, bifurcation, sister sessions, subordinate sessions, handoff, bridge files, or role dispatch. Also fire at natural transition points (deliverable ships, topic shifts, investigation wraps), or when the user is operating a multi-session Cowork architecture and a scope is ready for handoff. The user prefers manual control over what carries forward, so err on the side of alerting before pressure becomes critical.
---

# Cowork progressive disclosure helper

This skill replaces the surprise of automatic compaction with deliberate, user-driven session management. When a Cowork session is approaching context pressure or has reached a natural break point, alert the user with a structured heads-up and offer a graduated set of options ranging from "do nothing" to "spin up a new subordinate session with a proper bridge file."

The user has explicitly chosen this manual-control model because automatic compaction summarizes opaquely, loses fidelity in unpredictable places, and offers no choice about what survives. The skill's job is to give the user that choice, and to translate it into the role-aware multi-session architecture they have documented and operate today.

## Progressive disclosure as a three-layer principle

The user generalizes progressive disclosure beyond the classical UX definition. In their operating model, three layers of disclosure run simultaneously:

1. **Within a single session**: skills, memory files, and tool definitions load on demand. A skill description sits in the available-skills list at minimal token cost; full instructions load only when the skill is invoked. This is the layer Anthropic's skill loading documents.
2. **Across sessions**: bridge files (shared markdown documents in workspace folders) act as the disclosure interface between sessions. One session sees a paragraph summary of what another session did; full session state stays inside its own context. Bridges are bidirectional and asynchronous.
3. **Within a domain**: role specialization is itself a disclosure pattern. The Architect doesn't carry Power Query lore because the Developer does. The Schema Expert doesn't carry chart formatting expertise because FP&A Modeling does. Each role specializes so no single session is forced to carry the union of all expertise.

This skill operates at layer 2 and layer 3. It detects when the current session is hitting a natural seam, then helps the user produce the right bridge or spawn the right new subordinate.

## The role vocabulary

The user operates a documented multi-session architecture. Use this vocabulary when proposing splits:

- **Manager (parent session)**: holds cross-domain context, holds user intent across topic shifts, decides which subordinate to dispatch to, reviews subordinate output before relaying to the user. The Manager session is the only one that talks to the user directly across topics.
- **Architect**: designs and reviews implementation work in a specific technical domain. Authors specifications, scoping documents, decision rationales. Does not execute the work directly.
- **Developer**: takes Architect specifications and implements them. Runs shell commands, executes SQL, writes and tests code, edits production files. Reports back through the bridge.
- **Coder**: a narrower Developer scope for one-off scripting or prototype iteration. Less ceremony than Developer.
- **Schema Expert**: maintains canonical reference documents (column inventories, table schemas, helper-table layouts) that other roles consult before acting. Read-mostly; updates on triggers like "user re-exported the production code."
- **Subordinate specialists**: domain experts (FP&A Projection, FP&A Payroll, Comms Analyst, etc.) that own a piece of the user's life and operate within tightly fenced scope.

When detecting scopes and proposing splits, frame them in this vocabulary. "Spin off as a Developer subordinate for the BI work" lands more usefully than "spin off a sister session."

## When to fire the alert

Fire when ANY of these conditions are met, but fire each condition only once per session (do not re-alert at the same threshold).

**Pressure thresholds (estimated context usage).** Rough estimates are fine; absolute precision is not the point. Use your judgment based on visible conversation length, tool result sizes, file reads, and skill loadings.

- Around 50% used: a gentle "midpoint heads-up" alert.
- Around 65% used: a "consider dispatching soon" alert.
- Around 80% used: an "act now to keep control" alert.
- Around 90% used: a final "auto-compaction is imminent, take action this turn" alert.

**Activity-based triggers.** Even at lower estimated usage, fire when:

- A heavy tool call lands more than 30K tokens of output in a single response (large web fetches, large file reads, large connector responses, large skill resource loads).
- The session has done five or more file reads, even small ones.
- The session has done three or more large web fetches.
- A skill has been invoked that loaded substantial reference content.

**Natural-transition triggers.** Fire when:

- A sub-task has clearly completed and the user signals a topic shift ("ok, next", "now let's", "moving on", "different topic").
- A deliverable has been produced and accepted (a file moved to the workspace, a draft approved, a question answered).
- The conversation has been ongoing for a while and the next request is a fresh scope.
- A scope is recognized as Architect-worthy or Developer-worthy and would benefit from dedicated context.

**Explicit invocation.** Fire whenever the user asks about context usage, compaction, session length, bifurcation, sister sessions, subordinate dispatch, or any related topic. In this case, do not wait for natural break points; respond immediately.

## How to estimate context usage

You do not have a direct token counter, but you can estimate within reasonable bounds.

- The Cowork session has a 200K token context window on Pro, Max, and Team plans (500K on some Enterprise models, 1M only on API tier 4 beta).
- System prompt and tool schemas typically consume 15K to 30K just at session start, depending on how many MCPs and skills are loaded.
- Each large tool result you have seen (web pages, file contents, connector data, skill resources) is visible to you in your context. Estimate ~1 token per 0.75 English words, more conservatively for HTML or code with structural markup.
- Conversation turns are usually 500 to 3000 tokens each unless heavy with tool calls.

When alerting, give a rough range, not a false-precise number. For example, "approximately 60 to 70 percent used" is better than "127K tokens used" unless you can actually back that figure up.

## The intervention ladder

Surface a ladder of six progressively heavier interventions. Recommend the right level for the current pressure and context, but show all levels so the user can override up or down. The heavier levels map to the user's role-aware multi-session architecture.

**Level 0: Continue.** No action. The current session keeps going and accepts whatever automatic compaction does later.

**Level 1: Inline recap.** A 3-to-5 sentence "where we are" recap appended to the response. Not saved externally, not changing the session. Useful at the first alert threshold (~50%) so the user has a clean snapshot in their visible scrollback.

**Level 2: External checkpoint.** A fidelity-preserving summary the user saves outside the session (memory markdown, project notes, an OPEN_TOPICS append). The current session continues. Useful at a milestone moment when the user wants a recoverable state record but isn't ready to dispatch.

**Level 3: Dispatch to a subordinate.** Spin one specific scope off into a subordinate session via a bridge file. The current session continues with the remaining scope. The subordinate gets a role assignment (Architect, Developer, Coder, or specialist) appropriate to the work. Useful when one well-defined sub-task has matured enough that it belongs in a dedicated subordinate with its own context budget.

**Level 4: Multi-way decomposition.** The current session is decomposed into a Manager that retains only cross-domain orchestration plus N subordinates, one per major scope, each with role assignment and bridge file. The Manager keeps a compact index of what went where and which bridges are active. Useful when several scopes have accumulated and the cleanest answer is to fan them out into role-appropriate subordinates.

**Level 5: Full reorganization.** The current session is treated as a "donor session" that's harvested for its valuable artifacts and then retired. A fresh org chart is started: new Manager, new subordinates spun up against fresh bridge files, OPEN_TOPICS reset. Useful when the session has drifted across so many concerns that no single dispatch saves it.

The levels are not strictly cumulative; the user can blend (e.g., "give me a Level 1 recap now and a Level 3 dispatch to a Developer subordinate for the BI thread").

## Alert format

Use a compact, scannable stru