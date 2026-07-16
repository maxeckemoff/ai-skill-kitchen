# Multi-session Cowork architecture: Manager, Architect, Developer, Coder, Subordinate

A working pattern for operating Anthropic Cowork sessions in coordinated roles, with a single human operator at the top of the org chart and specialized Cowork sessions as the org. Documented from inside the pattern as it operates today, with honest accounting of where it pays off and where it costs. The skills in this repository are the reusable pieces extracted from running it.

## What the structure looks like in practice

Picture a human with one role and several specialist agents. The roles are not abstract; each one is a separate Cowork window with its own context window, its own memory tree, and its own scope of responsibility. They coordinate through markdown files that sit in shared workspace folders.

A representative slice of the org:

- **Manager** (the parent session): owns cross-domain context, holds the operator's intent across topic shifts, decides which subordinate to dispatch to, reviews subordinate output before relaying to the operator. The Manager is the only session that talks to the operator directly across topics.
- **Architect**: designs and reviews implementation work in a specific technical domain. Authors specifications, scoping documents, decision rationales. Does not execute the work directly.
- **Developer**: takes Architect specifications and implements them. Runs shell commands, executes queries, writes and tests code, edits production files. Reports back through a structured channel.
- **Coder**: a narrower Developer scope when needed (for example, one-off scripting or prototype iteration).
- **Schema Expert**: maintains canonical reference documents (column inventories, table schemas, helper-table layouts) that other roles consult before acting. Read-mostly; updates on a trigger such as the operator re-exporting the production source.
- **Subordinate specialists**: domain experts, each owning one piece of the operator's work (for example a financial-model specialist, a payroll-workpaper specialist, or a communications-archive specialist) and operating within tightly fenced scope.

Coordination between any two roles happens through a shared markdown file called a **bridge**. The bridge is the interface contract: each side writes, each side reads, neither side directly sees the other's full session state.

A typical Architect-to-Developer bridge file has sections for current instruction, activity log (newest at top, signed by author), open questions, and standing rules. Bridges accumulate decisions over time and serve as both an active worklist and a permanent audit trail.

## How the work actually flows

A representative cycle, structurally accurate:

1. The operator asks the Manager session a question that spans two domains. Manager identifies which subordinate owns which piece and dispatches accordingly.
2. Manager writes a new instruction to the Architect-to-Developer bridge: "Please scope this refactor; here are the constraints and the standing rules to apply."
3. The operator launches the Developer session in a separate Cowork window. Developer reads the bridge, executes the work, writes the deliverable to a scratch location, summarizes the outcome in the bridge's activity log.
4. The operator comes back to the Manager session. Manager reads the bridge activity log, reviews the deliverable, updates the canonical project tracker (a file such as OPEN_TOPICS.md), responds to the operator with a synthesis.
5. The operator integrates the deliverable into production (in some setups, by manually pasting the delivered code into the production tool). Confirms in chat to the Manager. Manager logs the integration to the bridge and to the tracker.

That cycle repeats across many domains, often in parallel windows. Each subordinate is its own background process from the Manager's perspective.

## How this maps to progressive disclosure

The operator generalizes progressive disclosure beyond its classical UX definition. Its primary meaning here is the deliberate practice of splitting work into role-specialized sessions that coordinate through bridge files, rather than building everything up turn by turn in one chat. Two finer-grained mechanics support it:

**Within a single session**, skills and tool definitions load on demand. A skill description sits in the available-skills list at minimal token cost; the full instructions load only when the skill is invoked. Memory files behave similarly.

**Across sessions**, bridge files act as the disclosure interface. The Architect sees a one-paragraph summary of what the Developer did; the Developer's full session state (all the file reads, diagnostic output, intermediate drafts) stays inside the Developer session. If the Architect needs more detail, the bridge has a pointer to a saved reference doc. The Manager reads the Architect's summary of a work product, not the work product itself.

**Within a domain**, role specialization is itself a disclosure pattern. Each role specializes its memory and working knowledge so no single session carries the union of all expertise.

Where classical progressive disclosure is unidirectional and synchronous (a user clicks "More"), this pattern is **bidirectional and asynchronous**: both sides of a bridge write to it, sessions do not run simultaneously, and the disclosure happens whenever the operator transitions between windows.

## Efficiency gains observed

Ordered from biggest to smallest impact.

**1. Context budget preservation across topics.** Each subordinate has its own context window. The Developer never sees the operator's conversation about a different domain; the Manager never sees the Developer's long file reads of legacy code. This is the single biggest gain. In a single-session model, every topic shift carries the cost of all prior context. Here, topic-shift cost is roughly zero because you switch windows.

**2. Specialized memory accumulation.** Each session's memory tree fills with domain-specific knowledge. The Manager carries none of it; when it needs domain knowledge, it dispatches rather than learning the domain itself.

**3. Parallel execution.** One specialist can audit a model while the Developer rewrites a data layer while the Manager reviews a draft. None blocks the others. In a single-session model, work serializes on a single turn.

**4. Cleaner audit trail.** Bridge files create a permanent, file-based, diffable, searchable log of decisions and deliveries. Months later the tracker shows exactly what landed when, who delivered it, what was rejected or amended. A single-session model leaves you with chat history that gets compacted away.

**5. Lower blast radius on context resets.** If one session hits auto-compaction or restarts, the Manager's understanding of the broader project is untouched. In a single-session model, one compaction event can lose nuance across every active topic.

**6. Role-appropriate constraint enforcement.** Tone preferences, versioning rules, defensive coding patterns, conventions: each subordinate's bridge carries the standing rules for its scope, so the Manager does not relay them every time.

**7. Asynchronous coordination across the operator's day.** The Manager can write an ask in the morning, the operator can launch the Developer midday, the Developer can deliver by late afternoon, the operator can return to the Manager in the evening. The bridge file persists the state across those gaps.

**8. Failure isolation.** A bad turn in one session is contained. The Manager inherits the Developer's outcome, which the Architect can review before relaying, not the Developer's mistakes.

## Efficiency losses observed

Also ordered by impact.

**1. Coordination overhead.** Bridge updates take real turns and real human attention. Every handoff requires the sender to write a bridge entry, the operator to switch windows, the receiver to read, execute, and write back. A quick clarification that would have been one turn in a single session can become a multi-window roundtrip.

**2. Information loss in handoffs.** Bridge entries are summaries. If a session resolved an edge case through several rounds of internal reasoning, the receiver sees only the resolved outcome. Subtle decisions get lost unless deliberately preserved.

**3. Manager-side cognitive load on the operator.** The operator has to remember which subordinate owns which scope, which session is mid-task, which bridge is the right channel. The mental model is an org chart to dispatch across. That is real overhead even when each interaction is simpler.

**4. Stale bridge state risk.** A subordinate can finish a sub-task or update its own memory without writing to the bridge, leaving the Manager with an outdated picture. Common enough that some bridges carry an explicit "on session end, append to activity log" rule.

**5. Multi-session context pressure management.** Each session has its own context window and its own compaction event. Managing pressure across several active sessions is harder than within one, and the Manager cannot see how full another session's context is.

**6. Duplicated standing rules.** Tone and convention rules must live in each subordinate's bridge or memory; updating them means updating every copy. (Mitigation: operator-level auto-memory propagates across sessions launched in the same workspace.)

**7. Slower iteration on tightly coupled work.** When two roles must converge quickly, bridge-and-window-switch latency is painful. A single session would resolve the same question in a turn or two.

**8. Skill and convention drift across sessions.** A skill installed in one session may not be visible to another; a convention adopted in one may not have propagated. Discipline is required to keep these aligned.

## Recurring elements that become skills

A skill is a small, self-contained instruction set that loads on demand. Several recurring patterns in this architecture met the bar and are the skills in this repository:

- **Warm-transfer kickoff authoring** for spinning up a new subordinate (role, orientation, recipes, expected first response).
- **Structured implementation-ask authoring** from an Architect to a Developer (scope, semantic constraints, in and out of scope files, deliverable format).
- **Post-integration check-off** when the operator confirms a delivery landed (log it, clear the ask, surface follow-ups).
- **Pre-launch review** of a kickoff prompt for completeness and tone before launch.
- **Session pressure and seam handling** to manage context deliberately rather than by surprise compaction.
- **Bounded interrogation of large sources** so a session profiles a big dataset without ingesting it whole.
- **Relay batons** that pass next-action state between sessions so threads do not stall.

Each of these was a repeated manual pattern before it was codified. That is the intended pipeline: notice a recurring shape of work, then promote it to a skill.

## Honest comparison: single-session vs multi-session

For one operator with one project and one stable topic: single-session usually wins. The coordination overhead is real, and one session that carries everything is faster per turn.

For one operator with multiple projects, several active subordinates, and topics that shift across the day: multi-session wins materially. Context budget preservation alone justifies the overhead.

For organizations: multi-session is a structural fit. The Manager-Subordinate pattern maps cleanly to real human org charts, and bridge files map cleanly to the specs, status reports, and decision logs organizations already produce.

The honest middle ground: the pattern works when the underlying scopes are genuinely independent. Forced onto tightly coupled work where every decision touches every other, it reproduces the meeting-overhead problem of human orgs.

## Pattern transferability

The mechanics rely on three primitives:

1. **A persistent shared file system** multiple sessions can read and write (workspace folders, shared drives, version control).
2. **A coordination convention** for what each side writes to the file (the bridge format).
3. **A human at the top** who decides when to dispatch and when to wait.

Any LLM agent platform that gives sessions concurrent or asynchronous access to a shared workspace can run this pattern. A skill system is a force multiplier (it makes the conventions enforceable templates) but is not a prerequisite.

## Takeaways for adopting this pattern

- **Start with one Architect-Developer split.** Do not spin up six subordinates on day one. Get one channel working, debug the friction, then add specialists incrementally.
- **Bridge files are the product.** Spend disproportionate effort on bridge design: the standing-rules section, the activity-log format, the open-questions section, the canonical-sources pointer. These decide whether the pattern feels like infrastructure or overhead.
- **Keep common rules at the operator level, not in each bridge.** Tone, formatting, and versioning conventions belong in operator-level auto-memory so they propagate. Bridges carry scope-specific rules only.
- **Index the bridges.** Past three or four active subordinates, maintain an index that summarizes which bridge is what and each session's status. The Manager reads the index first.
- **Be deliberate about which scopes are subordinate-worthy.** A subordinate exists for a scope that recurs and benefits from accumulated expertise. A one-off does not justify the launch overhead.
- **Promote bridge entries to canonical project memory.** The bridge is ephemeral by design; the project tracker is permanent. Move resolved bridge entries into the permanent record.

## Framing for presenting this pattern

- **For an org-minded audience:** an org chart of AI agents, each with a job description, a memory, and a way to talk to the others, with the human as the dispatcher. It maps to something everyone understands.
- **For an architecture-minded audience:** bridge files are the API between AI sessions; progressive disclosure across context budgets, not just within one; skills are reusable templates, bridges are the runtime coordination layer.
- **For a productivity-minded audience:** one human cannot hold many domains in working memory, but agents can each carry one. The trick is the handoff protocol, not the AI.
- **A frame that does not work:** "AI is replacing my team." It is not. The pattern requires a high-functioning human at the dispatch position; the agents are amplifiers, not replacements.
- **A frame that works and surprises people:** this is a study in how humans should delegate to humans, with agents as the test bed. The discipline that makes dispatch to AI subordinates work (clear scope, written conventions, explicit handoff format, a bidirectional channel, fenced authority) is exactly the discipline that makes human delegation work. The AI version is just enforceable.

## Status of this pattern

This document was written from inside an active deployment: a Manager session coordinating several role-specialized subordinates (an Architect and Developer for a technical domain, a Schema Expert, and a set of domain specialists) plus one human operator. It has been in production for some weeks at the time of writing and is the working configuration the operator prefers over a single-session alternative.

The honest summary: the pattern costs noticeable coordination overhead and pays back materially more in context preservation, parallel work, and audit clarity. It is the right configuration for a single operator running multiple concurrent domains, and the wrong one for a single domain with linear progression.
