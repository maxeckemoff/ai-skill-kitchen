# chrome-field-practice

A Claude Cowork skill that carries accumulated field practice for browser automation with Claude in Chrome, so no session has to rediscover it from scratch.

## Why it exists

A plausible-but-wrong cause once got written down as fact and cost hours (the Energy Saver misdiagnosis, kept in the skill verbatim as a caution). This skill exists to stop that from happening again: every claim it carries is tagged MEASURED or INFERRED, and it never lets an inference become a silent rule.

## What it does

1. **Tab-visibility precheck** (the highest-value single check): run before any click, drag, or screenshot. A hidden tab produces every symptom of a broken web app, most commonly a timed-out screenshot or a menu that will not open, while nothing is actually broken.
2. **An ordered diagnosis ladder** for when a click does nothing: hidden tab, invisible overlay, off-screen target, hover-gated element, or a hover that never fired, checked in that order before any retry.
3. **"Screenshots are not evidence"**: verify state through the DOM or the application's own API, never a screenshot alone.
4. Reference files, loaded only when the symptom matches: coordinate calibration and batching and gesture rules, the password-manager conjecture (explicitly labelled as such), and a per-application appendix.

## Relationship to the claude-in-chrome skill

This skill complements the `claude-in-chrome` skill rather than replacing it. That skill governs which `mcp__claude-in-chrome__*` tools to load before starting. This skill governs what to check before trusting page state, and how to diagnose things once those tools are loaded. Both are meant to fire on the same kind of request, and neither is a substitute for the other.

## How it keeps learning

A Cowork session cannot edit its own installed skill files; the on-disk copy is a read-only cache. So instead of self-modifying, any session that learns something new appends a dated, MEASURED-or-INFERRED-tagged entry to a durable field log (starter template shipped at `assets/FIELD_LOG_TEMPLATE.md`). A finding graduates from the log into the skill's actual rules once three observations corroborate it, or one clean measurement contradicts an existing rule. A rule that stops reproducing gets struck with the date and reason, never deleted, following the same convention as the `versioned-in-place` skill. Crossing either threshold means regenerating the packaged skill from source and handing it to whoever owns install, not pretending the change happened in place.

## Test triggers

See the "Test triggers" section in SKILL.md.
