# check-off-protocol

A Claude Cowork skill that runs the standardized post-integration sequence after you confirm to a Manager session that you have integrated a Developer subordinate's delivery.

## Why it exists

When a Developer hands back a deliverable and you integrate it (often by pasting code into production and confirming in chat), the same housekeeping fires every time: read what was delivered, record it in the permanent tracker, close or update the bridge ask, and capture any follow-ups. Skipping a step leaves the record out of sync, a bridge showing an ask that is actually done, an OPEN_TOPICS that never recorded the change, a follow-up nobody captured. This skill runs that sequence in a fixed order so nothing is dropped.

## The trigger

The trigger is *your confirmation of integration*, not the Developer's delivery. The skill fires when you say "integrated", "merged", "applied", "it's live", "done", "checked off", or similar, after a Developer has reported a deliverable through a bridge.

## The four-step sequence

1. **Read the Developer's latest bridge entry**: identify the T-number, what changed, caveats, and anything flagged open. If more than one ask is in flight, the skill asks which one you integrated rather than assuming.
2. **Append to OPEN_TOPICS.md**: a terse, completed-state record with the T-number, date, and version marker, pointing to the bridge for detail. Uses the pre-written wording from the original ask if it exists.
3. **Clear or update the bridge's Current Instruction**: cleared when the ask is fully resolved, rewritten to the remaining work when partial. A Manager-signed Activity Log entry is appended either way.
4. **Surface follow-ups**: anything the Developer flagged as open or next-up, each tagged as blocker, nice-to-have, or new scope, with a recommendation on whether it needs a new ask, a new subordinate, or can wait.

## Fully resolved vs. partial

An ask is treated as fully resolved only when the scope was met in full, the Developer recorded no remainder, and your confirmation covers the whole ask. If any one is uncertain, the skill keeps the ask open and marks it partial, on the principle that leaving an ask open one extra cycle is cheaper than losing track of unfinished work.

## How it fits with the sibling skills

- `architect-to-developer-ask-authoring` opens the cycle by writing the ask (and pre-writing the OPEN_TOPICS wording this skill later uses).
- `check-off-protocol` (this skill) closes the cycle after you integrate.
- `bridge-handoff-authoring` and `pre-launch-warm-transfer-review` handle standing up and vetting new sessions.
- `cowork-progressive-disclosure-helper` manages context pressure across the whole architecture.

## Compatibility

Works in any Cowork session with a bridge file and a project tracker. No external dependencies, no scripts, no API calls. Pure instructions for how Claude should run the close-out.

## License

MIT.
