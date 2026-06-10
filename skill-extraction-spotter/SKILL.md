---
name: skill-extraction-spotter
description: "Watches an active session for signs that a piece of work should be codified as a reusable skill, and surfaces a short recommendation with sketched SKILL.md frontmatter. Fire when the same shape of work appears two or more times in a session, when the user expresses friction about repetition (says 'I do this every quarter', 'every client needs this', 'same thing again', 'I keep having to'), or when a finished deliverable has clear inputs, outputs, and decision rules that would apply to future inputs. Do NOT fire on genuinely one-off tasks, on work already covered by an installed skill, or mid-task (wait for a natural seam). Output is advisory only: name the candidate skill, the recurring pattern, the trigger signals, a rough SKILL.md frontmatter sketch, and whether it is worth the maintenance. Hands the accepted candidate to skill-creator for the actual build."
---

# Skill extraction spotter

This skill is the missing monitor in the Kitchen toolkit. The architecture treats recurring work as the raw material for skills, but nothing watches for that raw material as it goes by. This skill does: it notices when the current session is doing something that has the shape of a reusable capability, and it surfaces a short, concrete recommendation so the pattern gets captured instead of re-solved next time.

It is advisory. It never builds a skill itself; it spots the candidate and hands an accepted one to `skill-creator`. It is the proactive front end to the same pipeline `skill-creator` finishes.

## When to fire

Fire at a natural seam (a deliverable shipped, a sub-task wrapped, a topic about to shift), not mid-task, when ANY of these signals appear:

- **Repetition within the session.** The same shape of work has been done two or more times (two similar documents produced, two near-identical analyses, the same multi-step procedure walked twice). Two is the threshold; once is not a pattern.
- **Stated friction about recurrence.** The user signals the work recurs across time or cases: "I do this every quarter", "every client needs this", "same thing again", "I keep having to", "every month I", "for each entity". The recurrence is the signal even if it has only happened once so far in view.
- **A generalizable deliverable.** A finished artifact has identifiable inputs, outputs, and decision rules that would apply to future inputs of the same type (a checklist that would re-run, a transformation with stable steps, a review with fixed criteria). If you could describe how to do it again for a different input, it is a candidate.

## When NOT to fire

- The task is genuinely one-off (a specific decision, a unique investigation, a question answered once).
- An installed skill already covers it. Check the available-skills list first; if it exists, point to it instead of proposing a duplicate.
- You are mid-task. Wait for the seam so the recommendation does not interrupt.
- The pattern is too thin to justify a skill (a single short step with no decision rules). A skill earns its keep by encoding judgment or a multi-step procedure, not by wrapping one trivial action.
- You already fired for this same candidate earlier in the session. Do not re-pitch it every turn.

## How to judge whether it is skill-worthy

Before recommending, run the candidate through these checks and only surface it if most hold:

- **Recurs or will recur.** Two-plus occurrences in view, or a credible statement that it repeats.
- **Generalizes.** The inputs vary but the procedure or judgment stays the same. You can name the variable inputs and the fixed steps.
- **Has decision rules worth encoding.** There is judgment a future run would benefit from (what to include, what to flag, what order, what to avoid), not just a single mechanical action.
- **Has a clear trigger.** You can describe the natural-language cues that should invoke it later. If you cannot, it is not ready to be a skill.
- **Worth the maintenance.** A skill is a durable artifact someone has to keep correct. A pattern used twice a year with stable rules is worth it; a one-off dressed up as a pattern is not.

## What to output

When you fire, keep it short and concrete:

```
### Skill candidate spotted

**Pattern:** [the recurring work, in one sentence]
**Why now:** [which signal fired: repetition / stated friction / generalizable deliverable]
**Proposed skill:** `[kebab-case-name]`
**Worth it?** [yes / borderline, with one line of reasoning on recurrence + maintenance]

**Sketched frontmatter:**
name: [kebab-case-name]
description: [one or two sentences: what it does, plus the trigger cues that should fire it]

**Rough scope:** [2 to 4 bullets on what the skill's body would cover]

Want me to hand this to skill-creator to build?
```

Do not write the full SKILL.md. The sketch is enough for the user to accept, refine, or decline. Only on acceptance does the work move to `skill-creator`.

## Handing off to skill-creator

If the user accepts the candidate, route it to `skill-creator`, which owns building, validating, and packaging the skill. This spotter's job ends at a green-lit sketch. Where the user runs the documented Kitchen pipeline, the built skill then follows the normal path: validate with package_skill, add to the local Skill Kitchen, and push to the repo via a Coder Instructions MD.

## Anti-patterns to avoid

- Do not pitch a skill for one-off work. Recurrence or a credible recurrence claim is required.
- Do not duplicate an installed skill. Check first; point to the existing one instead.
- Do not interrupt mid-task. Wait for the seam.
- Do not write the full skill here. Sketch, get a yes, hand to skill-creator.
- Do not re-pitch the same candidate every turn. Once per candidate per session.
- Do not use em dashes or AI-tone phrasing in the recommendation; it is an artifact the user reads.

## Test triggers

Examples that SHOULD fire this skill:

- "Great, that's the second quarterly entity workpaper I've had you build this session the same way." (repetition, two occurrences)
- "Every client onboarding I end up doing this exact compliance checklist by hand." (stated friction about recurrence)
- "Here's the finished payroll-accrual reconciliation; the steps are the same every month." (generalizable deliverable with stable rules)

Examples that should NOT fire this skill:

- "Help me decide whether to take this one specific deal." (one-off judgment, no recurrence)
- "What's the capital of France?" (no procedure, no recurrence)
- "Run the check-off protocol for T-041." (already covered by an installed skill; point to it, do not propose a new one)
