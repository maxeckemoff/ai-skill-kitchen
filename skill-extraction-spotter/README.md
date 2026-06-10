# skill-extraction-spotter

A Claude Cowork skill that watches an active session for work worth turning into a reusable skill, and surfaces a short recommendation before the moment passes.

## Why it exists

In a multi-session, skill-driven setup, recurring work is the raw material for new skills, but nothing normally notices that material as it goes by. You solve the same shape of problem twice, move on, and solve it again next quarter. This skill closes that gap: it spots the pattern in the moment and proposes capturing it, so the toolkit grows from real, repeated work instead of guesswork.

It is the proactive front end to `skill-creator`. It does not build anything; it recognizes a candidate and hands an accepted one off to be built.

## What makes it fire

It fires at a natural seam when any of three signals appear:

- **Repetition in the session**: the same shape of work done two or more times.
- **Stated friction about recurrence**: phrases like "I do this every quarter", "every client needs this", "I keep having to".
- **A generalizable deliverable**: a finished artifact with clear inputs, outputs, and decision rules that would apply to future inputs.

It deliberately stays quiet on one-off tasks, on work an installed skill already covers, while a task is mid-flight, and on candidates it has already pitched once in the session.

## How it judges a candidate

Before recommending, it checks that the pattern recurs (or credibly will), generalizes across varying inputs, carries decision rules worth encoding, has a describable trigger, and is worth the maintenance a durable skill demands. Thin or one-off patterns are filtered out.

## What you get

A short recommendation: the pattern in one sentence, which signal fired, a proposed kebab-case name, a worth-it judgment, sketched SKILL.md frontmatter, and a rough scope. Not a full skill, just enough to accept, refine, or decline. On acceptance, it routes to `skill-creator` for the build, which then follows the normal validate-and-push path.

## How it fits with the other skills

- `skill-extraction-spotter` (this skill) notices a candidate and sketches it.
- `skill-creator` builds, validates, and packages an accepted candidate.
- The other Kitchen skills (`bridge-handoff-authoring`, `architect-to-developer-ask-authoring`, `pre-launch-warm-transfer-review`, `check-off-protocol`, `cowork-progressive-disclosure-helper`) are the orchestration toolkit this spotter helps grow.

## Compatibility

Works in any Cowork session. No external dependencies, no scripts, no API calls. Pure instructions for how Claude should watch for and surface skill candidates.

## License

MIT.
