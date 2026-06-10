---
name: cowork-progressive-disclosure-helper
description: Monitors a Cowork session for context pressure and alerts before automatic compaction, then walks the user through a 6-level intervention ladder that includes role-aware multi-session moves (Manager, Architect, Developer, Schema Expert, Subordinate specialists) with bridge file scaffolding. Use whenever a session has run long, accumulated heavy tool calls or file reads, completed a sub-task, or when the user mentions context, compaction, tokens, session length, bifurcation, sister sessions, subordinate sessions, handoff, bridge files, or role dispatch. Also fire at natural transition points (deliverable ships, topic shifts, investigation wraps), or when the user is operating a multi-session Cowork architecture and a scope is ready for handoff. The user prefers manual control over what carries forward, so err on the side of alerting before pressure becomes critical.
---

# Cowork progressive disclosure helper

This skill replaces the surprise of automatic compaction with deliberate, user-driven session management. When a Cowork session is approaching context pressure or has reached a natural break point, alert the user with a structured heads-up and offer a graduated set of options ranging from "do nothing" to "spin up a new subordinate session with a proper bridge file."

The user has explicitly chosen this manual-control model because automatic compaction summarizes opaquely, loses fidelity in unpredictable places, and offers no choice about what survives. The skill's job is to give the user that choice, and to translate it into the role-aware multi-session architecture they have documented and operate today.

## Progressive disclosure: virtual employees with bridge coordination

In the user's operating model, progressive disclosure means the deliberate practice of splitting work into delineated "virtual employees" (Manager, Architect, Developer, Coder, Schema Expert, Subordinate specialists), each with its own Cowork session, its own context budget, its own memory tree, and bridge files as the coordination interface between them.

This is NOT in-session iteration in a single chat. Building up context turn by turn in one window is the baseline use of Claude AI. Progressive disclosure is the architecture that comes after you've outgrown the single window and started running an org chart.

The classical UX definition of progressive disclosure (revealing complexity gradually within a single interface) generalizes here to revealing context gradually across sessions: each virtual employee only sees what its role needs, with bridges as the disclosure interface. Within this pattern, two finer-grained disclosure mechanics also operate (skills and memory load on demand within a single session; role specialization means no single session carries the union of all expertise). But the load-bearing meaning of "progressive disclosure" in the user's operating model is the virtual-employee orchestration via bridges.

This skill is the operating-system level helper for that practice. It detects when the current session is hitting a natural seam and helps the user spawn the right new virtual employee with the right bridge, OR helps the user keep their current session productive when no dispatch is warranted.

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

Use a compact, scannable structure. The alert should NOT interrupt the work in progress unless pressure is critical; it should be added at the end of the response after answering whatever the user just asked. Format:

```
---
### Session pressure heads-up

**Estimate**: approximately X% used (rough).
**Trigger**: [why I am alerting now, in one sentence].
**Recommended level**: [N - short label]

**Scopes I detect in this session:**
1. [Scope A: 1-line description, suggested role if dispatched]
2. [Scope B: 1-line description, suggested role if dispatched]
3. [...]

**Your options (lighter to heavier):**
0. Continue (no action)
1. Inline recap (orient without changing state)
2. External checkpoint (save state, keep going)
3. Dispatch one scope as a subordinate session via bridge
4. Multi-way decomposition (Manager + N role-assigned subordinates)
5. Full reorganization (retire this session, start fresh org)

Tell me a level, or name specific scopes and roles to dispatch, or say "continue" to dismiss this alert.
---
```

When pressure is critical (around 90%), drop Level 0 from the options and make the recommendation more directive.

## How to recommend a level

The right level depends on pressure, scope diversity, and where the user is in their work:

- ~50% pressure, single coherent topic, no natural break: recommend **Level 0 or 1**.
- ~65% pressure, milestone reached, no need to dispatch: recommend **Level 2**.
- ~65% pressure, one scope is clearly mature and role-assignable: recommend **Level 3** with role suggestion.
- ~80% pressure with 3+ distinct scopes in play, each role-assignable: recommend **Level 4**.
- ~90% pressure or session has drifted across many unrelated concerns: recommend **Level 5**.

Override toward heavier if scopes have meaningfully different reference data needs (different connectors, projects, files, or roles), since that benefits more from dispatch. Override toward lighter if the user has signaled they want to stay focused on the current scope.

## Detecting scopes and proposing roles

Before producing the alert, scan the visible conversation for distinct work threads. A scope is typically:

- A bounded sub-task with its own subject
- A self-contained deliverable
- A line of inquiry the user pursued separately from others (different topic, different files, different connectors)

Distinguish scopes from tangents. A 2-turn aside is not a scope; a 10-turn sub-investigation is. List the scopes in the alert so the user can reason about which to keep, which to dispatch, and which to drop.

When proposing a role for a scope, use these heuristics:

- **Architect** for work that is design-heavy: specifying, scoping, deciding between approaches, reviewing trade-offs. The deliverable is a spec or rationale, not running code.
- **Developer** for work that is execution-heavy: implementing, running shell commands, editing files, testing. The deliverable is changed state in the workspace or production.
- **Coder** for one-off scripting, prototype iteration, or a single throwaway task. Less ceremony than Developer.
- **Schema Expert** for canonical reference work: updating column inventories, table schemas, helper-table layouts that other sessions consult.
- **Subordinate specialist** for domain-specific recurring work (FP&A Projection, Comms Analyst, etc.) that fits an existing specialist's scope.
- **A new specialist** if the scope is genuinely a new long-lived domain not covered by existing specialists.

## Executing a split (progressive disclosure within Level 3, 4, or 5)

When the user picks a heavy intervention, do not jump straight to producing bridge documents. Walk through these stages so the dispatch is deliberate:

**Stage 1: Scope inventory.** Confirm or refine the scope list. Show the user what you identified and let them rename, merge, split, or remove scopes. Brief: "I see scopes A, B, C, D. Confirm or edit before I propose a dispatch pattern."

**Stage 2: Dispatch proposal.** Recommend which scopes go where and which role each subordinate plays:
- For Level 3: which scope dispatches, which role gets assigned, what stays in the Manager.
- For Level 4: how scopes group into subordinates, what roles each gets, what the Manager retains.
- For Level 5: what artifacts harvest into the new org, what new top-level Manager scope looks like.

**Stage 3: Refinement.** Give the user a chance to adjust roles, merge subordinates, drop scopes, or add subordinates that are only implicit.

**Stage 4: Execute.** Produce the bridge file(s) using the format below. For Level 4, also produce the Manager-side index. For Level 5, produce the artifact harvest list plus the new top-level plan.

## Bridge file format (the user's documented convention)

When dispatching to a subordinate, produce a bridge file in this exact format. The user has documented this format and uses it across all active subordinates.

```markdown
# Bridge: [Manager session name] <-> [Subordinate role and scope]

## Current Instruction
[The one active ask the subordinate should work on next. Replaced with each new directive from the Manager.]

## Activity Log
[Newest at top. Each entry signed by author with [Manager] or [Subordinate role name]. Includes timestamp, command summary, outcome, key findings. Don't dump unbounded output; sample or link to a saved file.]

## Open Questions
[Append here when the subordinate needs a Manager decision before proceeding. Manager checks this section when reviewing bridge.]

## Standing Rules
[Accumulated decisions and conventions specific to this scope. Treat as load-bearing. Examples: tone preferences, file path conventions, semver rules, defensive coding patterns.]

## Canonical Sources
[Pointers to permanent reference docs the subordinate should consult: schema files, plan documents, OPEN_TOPICS.md, etc.]
```

Save the bridge file to the user's workspace at a path like `_plans/handoff/[descriptive_name]_Bridge.md` or wherever the user's existing convention places them. If unsure, ask.

## Bridge handoff (kickoff) message for the subordinate

When the user is ready to launch the subordinate session, also produce a paste-ready kickoff message that the subordinate session will see as its first input. Use this shape:

```
You are the [role] subordinate for [scope description].

The Manager has set up a bridge file at [path]. Read it now in full. The "Current Instruction" section is your active ask. Append timestamped entries to "Activity Log" (newest at top, signed [your role name]). Surface decisions you need from the Manager to "Open Questions."

[Any one-time orientation specific to this scope: dataset locations, file paths, the user's stated goal, existing conventions.]

Standing rules to follow: [list explicit rules to load into context immediately].

On session start, read [bridge path] and execute the current instruction.
```

## Producing a Manager-side index (for Level 4)

When the split is multi-way, the Manager session becomes thin and orientation-focused. Produce a doc the user can paste back into the trimmed Manager session (or save to `OPEN_TOPICS.md`) that summarizes the dispatch state:

```markdown
# Manager Index: [overall project label]

## What this Manager is for
[1-2 sentences: this Manager coordinates across the subordinates below; actual work lives in them.]

## Active Subordinates
1. **[Role and scope name]**: bridge at [path]. Status: [what they're working on, what's open].
2. **[Role and scope name]**: bridge at [path]. Status: [...].
3. [...]

## Cross-cutting Decisions and Preferences
[Decisions that apply across all subordinates, kept here so each one doesn't re-litigate them.]
[User preferences and constraints valid for the whole project.]

## Permanent Reference Artifacts
[Files, URLs, datasets that may be consulted from any subordinate.]

## OPEN_TOPICS Pointer
[Where the canonical project tracker lives, if applicable.]

## What this Manager does NOT track
[Specific implementation details now living in subordinates.]
```

## Producing a checkpoint (for Level 2)

When the user picks Level 2, produce a state-preserving summary in this shape:

```markdown
# Checkpoint: [date, short scope label]

## What we have established
- [Verbatim facts, decisions, deliverables that matter]
- [File paths and identifiers]

## Open questions
- [Things still in flight]

## Important context the model would benefit from remembering
- [User preferences and working style observed]
- [Any specific instructions the user has given that should carry forward]
```

The user saves this externally (OPEN_TOPICS append, memory markdown, project notes) and the session continues.

## Producing an inline recap (for Level 1)

Append 3 to 5 sentences of "where we are" inline. No structured doc, no external save. Mention the major scope(s) in flight, the last meaningful decision or deliverable, and the immediate next step. Done.

## Producing a fresh-tree plan (for Level 5)

The current session becomes donor material. Produce a doc that:

1. Lists the valuable artifacts the user should harvest from this session (files moved to the workspace, decisions worth preserving, skills built, drafts produced) with explicit references.
2. Sketches a new top-level Manager scope: what this Manager will coordinate, what subordinates to spin up first, initial role assignments.
3. Provides initial bridge file templates for the first 2 to 3 subordinates.
4. Notes what to abandon: scopes from the donor session that don't deserve carrying forward.

Tell the user explicitly: "After saving the artifacts list and the new top-level plan, retire this session and start fresh with a new Manager and the initial subordinates I've scaffolded."

## Format hints

- Keep the alert under 12 lines unless the user asks for more detail.
- Do not editorialize at length. The user knows the trade-offs; they want a heads-up, not a lecture.
- Do not re-alert at the same threshold; if you alerted at 50% and the user said "continue," do not alert again until the next threshold (65%).
- If the user has said "stop alerting me" or "I'll handle context manually," respect that and suspend further alerts for the session.

## Anti-patterns to avoid

- Do not fire on every turn. Respect the once-per-threshold rule.
- Do not produce alerts during a tightly focused sub-task in progress. Wait for the sub-task to wrap up, then alert at the boundary.
- Do not use false precision ("you are at 127,432 tokens"). Use ranges.
- Do not assume the user wants to dispatch. Offer the options and let them choose.
- Do not produce a bridge file or checkpoint until the user explicitly asks for one.
- Do not propose roles the user hasn't established. If a scope doesn't fit Architect/Developer/Coder/Schema Expert or an existing specialist, ask whether to create a new specialist or use Coder by default.

## When the skill is not appropriate

Suppress the alert if:

- The user is in the middle of a multi-step procedure that should not be interrupted (drafting a document, executing a critical command).
- The user has explicitly turned off alerts for this session.
- The conversation is short and pressure is unambiguously low.
- The next planned action will itself conclude the session naturally.

## Sibling skills

This skill is one of several in the user's multi-session architecture toolkit. When relevant, point to them rather than reinventing:

- `bridge-handoff-authoring`: scaffolds warm-transfer kickoff prompts for new subordinates
- `architect-to-developer-ask-authoring`: produces T-number-style asks in the documented format
- `pre-launch-warm-transfer-review`: reviews a warm-transfer prompt before launch for completeness
- `check-off-protocol`: standardizes the user's post-integration sequence (read bridge, log to OPEN_TOPICS, clear ask, surface follow-ups)

If those skills are installed, defer to them for the deeper work in their respective domains. This skill's job ends at "here is the bridge file" and "here is the kickoff message"; the sibling skills polish those artifacts.
