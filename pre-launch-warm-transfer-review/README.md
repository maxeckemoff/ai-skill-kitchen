# pre-launch-warm-transfer-review

A Claude Cowork skill that reviews a drafted warm-transfer kickoff prompt before it is sent to a new subordinate session, and returns a pass or needs-revision verdict with specific edits.

## Why it exists

A kickoff prompt that is missing a dataset path, carries an em dash, or never tells the new session what to confirm before acting will produce a subordinate that starts on the wrong foot, and the cost shows up a full window-switch later. This skill is the cheap sanity check that catches those problems before launch instead of after.

## What it checks

The review runs five fixed categories:

1. **Completeness**: role assignment, bridge path, scope, dataset orientation, recipes, standing rules, expected first response, and start instruction are all present.
2. **Tone-rule presence**: no em dashes, no AI-tone giveaways, no authority-undercutting hedging. The em-dash check is a hard fail, never advisory.
3. **Dataset specificity**: concrete paths, IDs, connectors, and table names instead of vague references like "the data" or "the usual place". When the bridge file is available, it cross-checks the prompt against the bridge's Canonical Sources.
4. **Open-question framing**: the prompt tells the subordinate to confirm unknowns and surface ambiguity before acting, rather than charging ahead.
5. **Standing-rules clarity**: scope-specific rules are stated concretely; propagating rules are referenced, not over-duplicated.

## The verdict

A flag in completeness, tone rules, or dataset specificity produces a NEEDS REVISION verdict, because those three cause the most damage at launch. Flags in open-question framing or standing-rules clarity can be advisory if everything else passes, and the skill says so explicitly when it lets one through.

## Output

The skill returns a compact, numbered review: pass or flag per category, then the suggested edits. It proposes targeted rewrites rather than rewriting the whole prompt, and it never invents missing dataset paths; it flags the gap for the user to fill.

## How it fits with the sibling skills

- `bridge-handoff-authoring` produces the kickoff prompt.
- `pre-launch-warm-transfer-review` (this skill) reviews it before launch.
- `cowork-progressive-disclosure-helper` decides when a split is warranted in the first place.
- `architect-to-developer-ask-authoring` and `check-off-protocol` cover the steady-state asks and post-integration sequence once the session exists.

## Compatibility

Works in any Cowork session. No external dependencies, no scripts, no API calls. Pure instructions for how Claude should review the prompt.

## License

MIT.
