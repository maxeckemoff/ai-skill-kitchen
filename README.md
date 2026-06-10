# AI Skill Kitchen

A small, growing collection of LLM agent skills and shared markdowns that I've built and found useful enough to share. Skills here are designed primarily for Claude (Claude Code, Cowork, the Claude Agent SDK), but the patterns and prompts often translate to other LLM frameworks with light adaptation.

## What's inside

These six skills form a toolkit for operating a multi-session Cowork architecture, where one human dispatches work across role-specialized agent sessions (Manager, Architect, Developer, Schema Expert, specialists) that coordinate through shared markdown bridge files.

| Skill | What it does | Status |
|---|---|---|
| [cowork-progressive-disclosure-helper](./cowork-progressive-disclosure-helper) | Alerts Cowork sessions on context pressure and walks you through a 6-level intervention ladder (recap, checkpoint, dispatch, multi-way split, full reorganization) before automatic compaction takes over. Decides when a scope is ready to split off. | Released |
| [bridge-handoff-authoring](./bridge-handoff-authoring) | Scaffolds the warm-transfer kickoff prompt and initial bridge file for a new subordinate session: role assignment, sidebar identity code, scope, dataset orientation, recipes, standing rules, expected first response. | Released |
| [architect-to-developer-ask-authoring](./architect-to-developer-ask-authoring) | Turns a freeform description into a structured, ticket-numbered implementation ask in the bridge: scope, semantic constraints, in/out-of-scope files, deliverable format, pre-written tracker update. | Released |
| [pre-launch-warm-transfer-review](./pre-launch-warm-transfer-review) | Reviews a drafted kickoff prompt before launch across five categories (completeness, tone rules, dataset specificity, open-question framing, standing-rules clarity) and returns a pass / needs-revision verdict. | Released |
| [check-off-protocol](./check-off-protocol) | Runs the post-integration close-out after you confirm a delivery is live: read the bridge entry, log to the project tracker, clear or update the bridge ask, surface follow-ups. | Released |
| [skill-extraction-spotter](./skill-extraction-spotter) | Watches an active session for work worth codifying as a reusable skill, then surfaces a short recommendation with sketched SKILL.md frontmatter and hands an accepted candidate to skill-creator. | Released |

More to come. The intent is to expand this kitchen over time with skills, prompts, and patterns that have earned their keep in real work.

## Installing a skill

Each skill ships as a `.skill` bundle at the repo root, alongside its source folder:

1. Download the `[skill-name].skill` file from the repo root.
2. Open Claude Desktop (or your Claude environment of choice).
3. Either drag the file onto the Claude window, or open Settings → Skills → Install from file.
4. The skill registers and becomes available in matching sessions automatically.

If you want to read or modify a skill before installing, the source (`SKILL.md`, `README.md`) lives in the matching `[skill-name]/` folder.

## Contributing or forking

Each skill is independent. Fork the repo, modify the skill folder you care about, repackage with your preferred tooling, and use. If you build improvements that are broadly useful, pull requests are welcome.

## License

MIT. Use, modify, redistribute. Attribution appreciated but not required.

## About

Maintained by [@maxeckemoff](https://github.com/maxeckemoff). Skills are products of real workflow problems, not synthetic demos.
