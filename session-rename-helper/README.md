# session-rename-helper

A Claude Cowork skill that composes the correct sidebar label for a session and gives the steps to apply it, following the user's Identity Convention v1.0.

## Why it exists

In a multi-session org, the sidebar label is the at-a-glance identity of each session. Labels drift, new sessions need naming, and after an architecture change a batch of sessions needs relabeling. This skill turns a project, role, and descriptor into the exact label string and the steps to apply it, for one session or many.

It is the dedicated rename verb, paired with `bridge-handoff-authoring` (which embeds an identity into a brand-new session's kickoff). This skill applies to existing sessions too, and owns batch renames.

## What it produces

- **The label string** per the convention: ID grammar `PROJECT[-SUBSCOPE]-ROLE[-N]`, label format `ID [Descriptor]` (for example `FPA-PROJ-ENG [Projection engine]`).
- **Output A (default)**: the label plus an in-app right-click rename click-path. Zero risk.
- **Output B (optional)**: a Coder Instructions MD for batch renames that edits the per-session title JSON files on disk while Claude Desktop is closed.

## Safety built into the batch path

The on-disk rename only happens through a Coder Instructions MD, with hard cautions: Claude Desktop fully closed first; never kill processes named `claude` (that can take down the Coder's own session); back up every JSON before editing; change only the title field and re-validate JSON; and a per-file id-to-label table so nothing is renamed blind. The MSIX package id in the path is machine specific, so the MD locates it rather than hardcoding it.

## Convention source

The skill generates labels per `AI Org Chart\Identity_Convention.md` (v1.0) and checks `Session_Registry.md` for disambiguating number suffixes when reachable. New project or role codes are asked for and registered, not invented.

## How it fits with the sibling skills

- `bridge-handoff-authoring` names a new session at birth and embeds its identity in the kickoff.
- `session-rename-helper` (this skill) composes and applies labels for existing sessions and batches.
- `cowork-progressive-disclosure-helper`, `check-off-protocol`, `pre-launch-warm-transfer-review`, `architect-to-developer-ask-authoring`, and `skill-extraction-spotter` round out the orchestration toolkit.

## Compatibility

Works in any Cowork session. The skill itself only produces text (a label and steps); any on-disk editing is delegated to a Coder Instructions MD. No external dependencies.

## License

MIT.
