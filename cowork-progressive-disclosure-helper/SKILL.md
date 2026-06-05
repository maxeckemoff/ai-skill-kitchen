---
name: cowork-progressive-disclosure-helper
description: Proactively monitors a running Cowork session for context window pressure and alerts the user before automatic compaction takes over, so they can do targeted compaction or split off subordinate sister sessions deliberately. Use this skill whenever a session has been running long, has accumulated multiple substantial tool calls, file reads, or web fetches, has just completed a sub-task, or when the user mentions context, compaction, token usage, session length, splitting, bifurcation, sister sessions, subordinate sessions, handoff, or how much context is left. Also use whenever a natural transition point appears (a deliverable ships, a topic shifts, an investigation wraps up), so the user can choose to checkpoint or bifurcate cleanly instead of letting automatic compaction strip context unpredictably. The user prefers manual control over what carries forward, so err on the side of alerting before pressure becomes critical, not after.
---

# Cowork session pressure alert and bifurcation helper

This skill replaces the surprise of automatic compaction with deliberate, user-driven session management. When a Cowork session is approaching context pressure or has reached a natural break point, alert the user with a structured heads-up and offer concrete options: continue, checkpoint, or bifurcate.

The user has explicitly chosen this manual-control model because automatic compaction summarizes opaquely, loses fidelity in unpredictable places, and offers no choice about what survives. The skill's job is to give the user that choice.

## When to fire the alert

Fire when ANY of these conditions are met, but fire each condition only once per session (do not re-alert at the same threshold).

**Pressure thresholds (estimated context usage).** Rough estimates are fine; absolute precision is not the point. Use your judgment based on visible conversation length, tool result sizes, file reads, and skill loadings.

- Around 50% used: a gentle "midpoint heads-up" alert.
- Around 65% used: a "consider bifurcating soon" alert.
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

**Explicit invocation.** Fire whenever the user asks about context usage, compaction, session length, bifurcation, or any related topic. In this case, do not wait for natural break points; respond immediately.

## How to estimate context usage

You do not have a direct token counter, but you can estimate within reasonable bounds.

- The Cowork session has a 200K token context window on Pro, Max, and Team plans (500K on some Enterprise models, 1M only on API tier 4 beta).
- System prompt and tool schemas typically consume 15K to 30K just at session start, depending on how many MCPs and skills are loaded.
- Each large tool result you have seen (web pages, file contents, connector data, skill resources) is visible to you in your context. Estimate ~1 token per 0.75 English words, more conservatively for HTML or code with structural markup.
- Conversation turns are usually 500 to 3000 tokens each unless heavy with tool calls.

When alerting, give a rough range, not a false-precise number. For example, "approximately 60 to 70 percent used" is better than "127K tokens used" unless you can actually back that figure up.

## The intervention ladder (progressive disclosure)

When alerting, do not just offer "continue, checkpoint, or bifurcate" as three flat options. Surface a ladder of six progressively heavier interventions. Recommend the right level for the current pressure and context, but show all levels so the user can override up or down.

**Level 0: Continue.** No action. The current session keeps going and accepts whatever automatic compaction does later.

**Level 1: Inline recap.** A 3-to-5 sentence "where we are" recap appended to the response. Not saved externally, not changing the session, just helps the user stay oriented. Useful at the first alert threshold (~50%) so the user has a clean snapshot in their visible scrollback.

**Level 2: External checkpoint.** A fidelity-preserving summary the user saves outside the session (memory markdown, project notes, scratch file). The current session continues. Useful at a milestone moment when the user wants a recoverable state record but isn't ready to move work elsewhere.

**Level 3: Single bifurcation.** Spin one specific scope off into a sister session via a handoff document. The current session continues with the remaining scope. Useful when one well-defined sub-task is mature enough to live on its own and removing it would meaningfully relieve pressure.

**Level 4: Multi-way split.** The current session is decomposed into a thin parent (or "index session") plus N child sessions, one per major scope. Each child gets its own handoff document; the parent retains only a compact index of what went where, decisions made, and pointers back to children. Useful when several scopes have accumulated and the cleanest answer is to fan them out.

**Level 5: Full reorganization.** The current session is treated as a "donor session" that's harvested for its valuable artifacts and then retired. A fresh tree of sessions is started in a project, with a new top-level plan. Useful when the session has drifted across so many concerns that no single split pattern saves it.

The levels are not strictly cumulative; the user can also blend (e.g., "give me a Level 1 recap now and a Level 3 bifurcation of the BI thread").

## Alert format

Use a compact, scannable structure. The alert should NOT interrupt the work in progress unless pressure is critical; it should be added at the end of the response after answering whatever the user just asked. Format:

```
---
### Session pressure heads-up

**Estimate**: approximately X% used (rough).
**Trigger**: [why I am alerting now, in one sentence].
**Recommended level**: [N - short label]

**Scopes I detect in this session:**
1. [Scope A: 1-line description]
2. [Scope B: 1-line description]
3. [...]

**Your options (lighter to heavier):**
0. Continue (no action)
1. Inline recap (orient without changing state)
2. External checkpoint (save state, keep going)
3. Bifurcate one scope into a sister session
4. Multi-way split (thin parent index + N children)
5. Full reorganization (retire this session, start fresh)

Tell me a level, or name specific scopes to spin off, or say "continue" to dismiss this alert.
---
```

When pressure is critical (around 90%), drop Level 0 from the options and make the recommendation more directive.

## How to recommend a level

The right level depends on pressure, scope diversity, and where the user is in their work:

- ~50% pressure, single coherent topic, no natural break: recommend **Level 0 or 1**.
- ~65% pressure, milestone reached, no need to move work: recommend **Level 2**.
- ~65% pressure, one scope is clearly mature and separable: recommend **Level 3**.
- ~80% pressure with 3+ distinct scopes in play: recommend **Level 4**.
- ~90% pressure or session has drifted across many unrelated concerns: recommend **Level 5**.

These are defaults. Override toward the heavier end if scopes have meaningfully different reference data needs (different connectors, projects, files) since that benefits more from separation. Override toward the lighter end if the user has signaled they want to stay focused on the current scope.

## Detecting scopes in the current session

Before producing the alert, scan the visible conversation for distinct work threads. A scope is typically:

- A bounded sub-task with its own subject (e.g., "the BI investigation," "the Zoho MCP setup," "the Zoom AI Companion config")
- A self-contained deliverable (a skill being built, a document being drafted, a debugging run)
- A line of inquiry the user pursued separately from others (different topic, different files, different connectors)

Distinguish scopes from tangents. A 2-turn aside is not a scope; a 10-turn sub-investigation is. List the scopes in the alert so the user can reason about which to keep, which to spin off, and which to drop.

## Executing a split (progressive disclosure within Level 3, 4, or 5)

When the user picks a heavy intervention (Level 3, 4, or 5), do not jump straight to producing handoff documents. Walk through these stages so the split is deliberate:

**Stage 1: Scope inventory.** Confirm or refine the scope list. Show the user what you identified and let them rename, merge, split, or remove scopes. Brief: "I see scopes A, B, C, D. Confirm or edit before I propose a split pattern."

**Stage 2: Split proposal.** Recommend which scopes go where:
- For Level 3: which scope spins off into the child, what s