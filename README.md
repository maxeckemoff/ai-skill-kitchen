# AI Skill Kitchen

A small, growing collection of LLM agent skills and shared markdowns that I've built and found useful enough to share. Skills here are designed primarily for Claude (Claude Code, Cowork, the Claude Agent SDK), but the patterns and prompts often translate to other LLM frameworks with light adaptation.

For the pattern these skills implement, see [ARCHITECTURE.md](./ARCHITECTURE.md).

## What's inside

These seventeen skills form a toolkit for operating a multi-session Cowork architecture, where one human orchestrator dispatches work across role-specialized agent sessions (Manager, Architect, Developer, Schema Expert, specialists) that coordinate through shared markdown bridge files, plus a growing set of tool-specific field practice and execution-convention skills for the concrete tools those sessions use day to day. They are grouped by role below.

### Core multi-session orchestration

| Skill | What it does | Status |
|---|---|---|
| [bridge-handoff-authoring](./bridge-handoff-authoring) | Scaffolds the warm-transfer kickoff prompt and initial bridge for a new subordinate session, including a sidebar identity code. | Released |
| [relay-baton](./relay-baton) | Emits the relay artifacts that pass next-action state between sessions: the response-tail baton, bridge batons into a target's Current Instruction, and dependency-ordered fan-out sequences. | Released |
| [check-off-protocol](./check-off-protocol) | Runs the post-integration close-out after a delivery is confirmed live: log it, clear or update the bridge ask, surface follow-ups. | Released |
| [pre-launch-warm-transfer-review](./pre-launch-warm-transfer-review) | Reviews a drafted kickoff prompt before launch across five categories and returns a pass / needs-revision verdict. | Released |
| [architect-to-developer-ask-authoring](./architect-to-developer-ask-authoring) | Turns a freeform description into a structured, ticket-numbered implementation ask in the bridge. | Released |
| [session-rename-helper](./session-rename-helper) | Composes a sidebar label per the identity convention and gives the rename click-path, or a batch-rename Coder MD. | Released |
| [bridge-relocation-shell](./bridge-relocation-shell) | Relocates a bridge or handoff set to a new folder, leaving identity-confirm forwarding shells, with a CHECK-FIRST pass that flags write-targets. | Released |
| [bridge-append-freshness-check](./bridge-append-freshness-check) | Pre-append discipline for multi-writer bridges: re-read the section, anchor the insert on a structural landmark not a remembered adjacent entry, then append. | Released |

### Context and session management

| Skill | What it does | Status |
|---|---|---|
| [cowork-progressive-disclosure-helper](./cowork-progressive-disclosure-helper) | Alerts Cowork sessions on context pressure and walks through a 6-level intervention ladder before automatic compaction. | Released |
| [bounded-source-interrogation](./bounded-source-interrogation) | Profiles a large external source (big Sheet, export, COQL pull) for structure, counts, and a sample without loading it whole, to prevent context saturation. | Released |
| [live-source-watch](./live-source-watch) | Watches a per-session list of Drive docs, URLs, and local files by modifiedTime / mtime / hash and surfaces only the deltas as a one-line heads-up. | Released |
| [usage-check-on-prompt](./usage-check-on-prompt) | Reports a compact Claude session and weekly usage line via the claude-usage MCP, at session start and on request. | Released |

### Tool-specific field practice

| Skill | What it does | Status |
|---|---|---|
| [chrome-field-practice](./chrome-field-practice) | Field-tested diagnostics for browser automation with Claude in Chrome: a tab-visibility precheck, an ordered diagnosis ladder for a click that does nothing, and the discipline of tagging every claim MEASURED or INFERRED so a guess never quietly becomes a rule. | Released |

### Meta (skills about the kitchen itself)

| Skill | What it does | Status |
|---|---|---|
| [skill-extraction-spotter](./skill-extraction-spotter) | Watches a session for recurring work worth codifying as a skill and sketches a candidate, then hands it to skill-creator. | Released |
| [skill-install-sync](./skill-install-sync) | Diffs the local Kitchen against the skills loaded in a session and reports install, update, and stale candidates with actions. | Released |
| [versioned-in-place](./versioned-in-place) | Revises a durable doc in place: new version on top, prior versions kept below in a SUPERSEDED block. | Released |

### Execution conventions

| Skill | What it does | Status |
|---|---|---|
| [stunt-double-apply](./stunt-double-apply) | Runs a sanctioned write-mode (`--apply`) script past the auto-mode permission classifier using a fixed stand-in name the human orchestrator has already approved in their own settings. | Released |

More to come. The intent is to expand this kitchen over time with skills, prompts, and patterns that have earned their keep in real work.

## Installing a skill

Each skill ships as a `.skill` bundle at the repo root, alongside its source folder:

1. Download the `[skill-name].skill` file from the repo root.
2. Open Claude Desktop (or your Claude environment of choice).
3. Either drag the file onto the Claude window, or open Settings → Skills → Install from file.
4. The skill registers and becomes available in matching sessions automatically.

If you want to read or modify a skill before installing, the source (`SKILL.md`, `README.md`) lives in the matching `[skill-name]/` folder.

## Contributing or forking

Each skill is independent. Fork the repo, modify the skill folder you care about, repackage with your preferred tooling, and use.

Pull requests are welcome and go through a plain review before merge, the way any small open-source repo should be handled:

- No PR is merged unread. Every changed file gets opened and read, not diffed-and-skimmed, before merge, specifically for anything that reaches outside the repo (network calls, shell commands, credential handling) or that does not match what the PR description says it does.
- `scripts/quick_validate.py` (in the `skill-creator` skill, or your own equivalent) runs on every skill folder before merge: valid frontmatter, kebab-case name, no stray executable bundled without explanation.
- Contributions that add a bundled script or binary get the most scrutiny. A markdown-only change (a new SKILL.md section, a reference file, a corrected claim) is inherently lower risk than one that adds code.
- For `chrome-field-practice` specifically: field observations do not need a PR at all. Open an issue with the MEASURED or INFERRED tag, what was observed, and how to reproduce it. Corroborated findings get folded into the skill directly by the maintainer, following the promotion rule described in the skill itself.

This is a hobby-scale project maintained by one person, not a security team, so Anthropic's own guidance, install skills only from trusted sources, still applies. Read what you install.

## License

MIT. Use, modify, redistribute. Attribution appreciated but not required.

## About

Maintained by [@maxeckemoff](https://github.com/maxeckemoff). Skills are products of real workflow problems, not synthetic demos.
