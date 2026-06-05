---
name: check-off-protocol
description: "Runs the standardized post-integration sequence after the user confirms to a Manager session that they have integrated a Developer subordinate's delivery. Use when the user says 'integrated', 'merged', 'applied', 'it's live', 'live now', 'done', 'checked off', 'pasted it in', or similar, after a Developer has reported a deliverable back through a bridge. Executes four steps: read the Developer's most recent bridge Activity Log entry to identify what was delivered, append the integration to OPEN_TOPICS.md (or the canonical project tracker) with the right version marker, clear or update the relevant bridge's Current Instruction depending on whether the ask is fully or partially resolved, and surface any follow-ups the Developer flagged as open or next-up. Includes criteria for fully resolved versus partial and how to surface follow-ups without re-litigating settled decisions."
---

# Check-off protocol

When the user integrates a Developer subordinate's delivery (in many setups, by manually pasting code into production and confirming in chat), the same housekeeping sequence fires every time. Skipping a step leaves the permanent record out of sync with reality: a bridge that still shows an active ask that is actually done, an OPEN_TOPICS that never recorded the change, a follow-up that the Developer flagged and nobody captured. This skill runs that sequence in a fixed order so nothing is dropped.

The trigger is a user confirmation of integration, not a Developer delivery. The Developer reporting back is *not* the trigger; the user saying "integrated" or "it's live" is. This skill is the Manager-side close-out of a cycle that `architect-to-developer-ask-authoring` opened.

## The four-step sequence

Run these in order. Do not skip ahead; each step depends on the previous one.

### Step 1: Read the Developer's most recent bridge entry

Open the relevant Architect-to-Developer (or Manager-to-Developer) bridge file and read the newest Activity Log entry, plus any the user's confirmation references. Identify:

- The T-number and title of what was delivered.
- What actually changed (files, objects, behavior).
- Any caveats, edge cases, or partial-completion notes the Developer recorded.
- Anything the Developer flagged in Open Questions or as next-up.

If the user's confirmation is ambiguous about *which* ask they integrated (more than one is in flight), ask which T-number before proceeding. Do not assume the most recent one.

### Step 2: Append the integration to OPEN_TOPICS.md

Record the integration in the canonical project tracker (OPEN_TOPICS.md or the user's equivalent). If `architect-to-developer-ask-authoring` pre-wrote the OPEN_TOPICS wording in the ask, use it; otherwise compose an entry in the project's house style.

A good entry is a completed-state record, newest at top, and includes:

- The T-number and a one-line description of what landed.
- The integration date (use the current date from context, not a session-start date).
- The version marker the project uses (semver bump, dated tag) if applicable.
- A pointer to the bridge entry or scratch file for detail, rather than restating it.

Example: `T-041: TrimOrNull consolidated into one shared helper (was 77 inline copies). Integrated 2026-06-05. v1.4.0. Detail: Architect-Developer bridge Activity Log 2026-06-05.`

Keep it terse. OPEN_TOPICS is an index of what landed when, not a narrative.

### Step 3: Clear or update the bridge's Current Instruction

Decide whether the ask is fully resolved or partial, then act.

**Fully resolved** (clear the Current Instruction):

- The deliverable met the scope statement in full.
- The Developer recorded no remaining work for this T-number.
- The user's confirmation covers the whole ask, not just part.

When fully resolved, replace the Current Instruction with a neutral idle marker (for example, "No active ask. Awaiting next directive from Manager.") and ensure the resolution is reflected in the Activity Log with a Manager-signed close-out entry.

**Partial** (update, do not clear):

- The user integrated only part of the delivery, or
- The Developer split the ask and only some T-sub-items are done, or
- Integration surfaced a new issue that belongs to the same ask.

When partial, rewrite the Current Instruction to describe only the remaining work, note in the Activity Log what was integrated and what remains, and keep the T-number open with a sub-marker if the project uses them.

Append a Manager-signed Activity Log entry either way, recording the integration and the resolved/partial decision, newest at top.

### Step 4: Surface follow-ups

Collect anything the Developer flagged as open or next-up (from Open Questions, from caveats in the Activity Log, from a "recommend next" note) and surface them to the user as a short list of options. For each follow-up:

- State it in one line.
- Note whether it is a blocker, a nice-to-have, or a new scope.
- Recommend whether it warrants a new ask (via `architect-to-developer-ask-authoring`), a new subordinate (via `bridge-handoff-authoring`), or can be deferred.

Do not re-open settled decisions. A follow-up is forward-looking work the delivery revealed, not a re-litigation of choices already made and integrated. If the user expresses doubt about a settled choice, that is a separate conversation; flag it as such rather than folding it into the follow-up list.

## Output format

After running the sequence, report back compactly:

```
## Check-off: [T-number] - [title]

- **Integrated:** [one line on what landed]
- **OPEN_TOPICS:** updated ([version marker], [date])
- **Bridge:** [Current Instruction cleared / updated to remaining work]
- **Follow-ups:** [numbered list, or "none flagged"]
```

If there are follow-ups that warrant action, end with a single clear question about which to pursue, rather than starting any of them unprompted.

## Criteria summary: fully resolved vs partial

Treat as **fully resolved** only when all three hold: scope met in full, no Developer-recorded remainder, user confirmation covers the whole ask. If any one is uncertain, treat as **partial** and keep the ask open. It is cheaper to leave an ask open one extra cycle than to close one that still had remaining work and lose track of it.

## Anti-patterns to avoid

- Do not fire on a Developer delivery alone. Wait for the user's integration confirmation.
- Do not assume which T-number was integrated when several are in flight. Ask.
- Do not clear a Current Instruction that still has remaining work. When in doubt, mark partial.
- Do not restate the full delivery in OPEN_TOPICS. Record the outcome and point to detail.
- Do not re-litigate settled decisions under the banner of follow-ups.
- Do not start follow-up work unprompted. Surface options and let the user choose.
- Do not use em dashes or AI-tone phrasing in OPEN_TOPICS entries or bridge log entries; these are durable records the user reads.
