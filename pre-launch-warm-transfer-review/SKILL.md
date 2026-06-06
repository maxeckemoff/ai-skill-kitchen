---
name: pre-launch-warm-transfer-review
description: "Reviews a drafted warm-transfer kickoff prompt before it is sent to a new Cowork subordinate session, and returns a pass or needs-revision verdict with specific suggested edits. Use when a kickoff or handoff prompt has been drafted and is about to be launched, or the user says 'review this prompt', 'before I launch', 'is this kickoff ready', 'check this handoff', 'sanity-check this subordinate prompt', or similar. Checks five categories: completeness (all required sections present), tone-rule presence (no em dashes, no AI-tone giveaways), dataset specificity (concrete paths and IDs versus vague references), open-question framing (what the subordinate should confirm before acting), and standing-rules clarity (scope-specific rules stated, propagating rules not over-duplicated). Flags common failure modes per category and proposes rewrites."
---

# Pre-launch warm-transfer review

Before launching a new subordinate session, the kickoff prompt deserves a sanity check. A prompt that is missing a dataset path, carries an em dash, or never tells the subordinate what to confirm before acting will produce a session that starts on the wrong foot. This skill reviews a drafted kickoff prompt against a fixed checklist and returns a verdict plus concrete edits.

This is the reviewer in the multi-session toolkit. It pairs with `bridge-handoff-authoring`, which produces the prompt this skill reviews. Run this skill on the prompt that skill produced (or on any hand-written kickoff) before the user pastes it into a new session.

## What to review

Take the drafted kickoff prompt as input. If the bridge file it points to is available, read that too, so the review can check that the prompt and bridge agree. Review against the five categories below, in order. For each category, state pass or flag, and if flagged, give the specific fix.

## Category 1: Completeness

A complete kickoff prompt contains:

- **Role assignment**: the subordinate is told which role it holds (Architect, Developer, Coder, Schema Expert, specialist).
- **Bridge path**: an explicit path to the bridge file, with an instruction to read it in full on start.
- **Scope**: what the session owns and, ideally, what is out of scope.
- **Dataset orientation**: the concrete artifacts the session will touch.
- **Recipes**: role-specific recurring procedures or gotchas.
- **Standing rules**: the rules to load immediately.
- **Expected first response**: what the subordinate produces or confirms on turn 1.
- **Start instruction**: read the bridge, execute the Current Instruction, surface ambiguity to Open Questions rather than guessing.

Flag any missing element. Missing dataset orientation and missing expected-first-response are the two most common and most damaging omissions.

## Category 2: Tone-rule presence

The kickoff prompt is an artifact the user reads and reuses, so it must obey the user's distribution rules.

- **No em dashes.** Scan for the em dash character. If present, flag each occurrence and propose the replacement (comma, period, semicolon, parentheses, or a hyphen where a joiner is meant).
- **No AI-tone giveaways.** Flag stock phrases such as "Let me know if", "I hope this helps", "Certainly", "Great question", "delve into", and similar filler. Propose plain replacements or deletion.
- **No hedging that undercuts authority.** A kickoff should be directive. Flag wishy-washy framing ("you might want to maybe consider") and tighten it.

## Category 3: Dataset specificity

Vague references are the most common reason a fresh subordinate flounders on turn 1.

- Flag any reference to "the data", "the files", "the project", "the usual place", or similar, where a concrete path, project ID, connector name, table name, or VM name should appear.
- Check that every path or ID named is plausible and complete, not truncated.
- If the bridge file is available, check that the paths in the prompt match the Canonical Sources in the bridge. Flag mismatches.

## Category 4: Open-question framing

A good kickoff tells the subordinate what to confirm before it acts, so it does not charge ahead on a wrong assumption.

- Check that the prompt instructs the subordinate to surface ambiguity to Open Questions and stop, rather than guessing.
- If the scope contains a known unknown (an unconfirmed assumption, a decision the user has not made), check that the prompt names it as something to confirm first.
- Flag prompts that imply the subordinate should proceed regardless. Propose adding an explicit "confirm X before acting" line.

## Category 5: Standing-rules clarity

- Check that scope-specific standing rules are stated (the file-edit protocol, versioning convention, defensive-coding pattern that applies to this domain).
- Check that propagating rules (tone, fact-checking discipline) are referenced as applying but not exhaustively re-pasted, since they live in user-level memory. Flag heavy duplication as a maintenance smell, but treat it as a minor flag, not a blocker.
- Flag rules that are stated so vaguely the subordinate cannot act on them ("be careful with the files"). Propose a concrete, testable phrasing.

## Common failure modes and their fixes

- **Vague dataset reference** ("work with the projection model"): replace with the concrete path and the specific tabs or objects.
- **Missing expected-first-response**: add a line stating what the subordinate confirms or produces on turn 1.
- **Em dash present**: replace with the appropriate punctuation; never leave it.
- **AI-tone filler**: delete or replace with plain language.
- **No out-of-scope boundary**: add the files or domains the subordinate must not touch.
- **Proceed-regardless framing**: add the confirm-before-acting instruction and name the assumption to confirm.
- **Over-duplicated propagating rules**: trim to a one-line reference; keep only scope-specific rules in full.

## Output format

Return the review in this shape:

```
## Warm-transfer review: [prompt label]

**Verdict: PASS** (or **NEEDS REVISION**)

1. Completeness: [pass / flag + fix]
2. Tone rules: [pass / flag + fix]
3. Dataset specificity: [pass / flag + fix]
4. Open-question framing: [pass / flag + fix]
5. Standing-rules clarity: [pass / flag + fix]

**Suggested edits:** [the specific rewrites, or "none needed"]
```

Give a NEEDS REVISION verdict if any category in completeness, tone rules, or dataset specificity is flagged, since those three cause the most damage on launch. Open-question framing and standing-rules clarity flags can be advisory if everything else passes; say so explicitly when you let one through.

## Anti-patterns to avoid

- Do not rewrite the whole prompt unsolicited. Flag and propose targeted edits; let the user decide.
- Do not pass a prompt that contains an em dash. That is a hard rule, never advisory.
- Do not invent the missing dataset paths yourself; flag the gap and ask the user to supply them.
- Do not pad the review with praise. State pass or flag and move on.

## Test triggers

Examples that SHOULD fire this skill:

- "Here's the kickoff prompt I drafted for the new Developer. Is it ready to launch?"
- "Review this handoff prompt before I paste it into the new session."
- "Sanity-check this subordinate prompt for completeness and tone before I send it."

Examples that should NOT fire this skill:

- "Write me a kickoff prompt for a new Developer." (that is `bridge-handoff-authoring`; there is nothing drafted to review yet)
- "Review this Power Query code for bugs." (a code review, not a kickoff-prompt review)
- "Did the Developer integrate the last ask?" (that is `check-off-protocol`)
