# AI Skill Kitchen (we cook)

A small, growing collection of LLM agent skills and shared markdowns that I've built and found useful enough to share. Skills here are designed primarily for Claude (Claude Code, Cowork, the Claude Agent SDK), but the patterns and prompts often translate to other LLM frameworks with light adaptation.

## What's inside

| Skill | What it does | Status |
|---|---|---|
| [cowork-progressive-disclosure-helper](./cowork-progressive-disclosure-helper) | Alerts Claude Cowork sessions on context pressure and walks you through a 6-level intervention ladder (recap, checkpoint, bifurcate, multi-way split, full reorganization) before automatic compaction takes over. | Released |

More to come. The intent is to expand this kitchen over time with skills, prompts, and patterns that have earned their keep in real work.

## Installing a skill

Each skill folder contains a `.skill` file you can install directly into Claude:

1. Download the `.skill` file from the skill's folder.
2. Open Claude Desktop (or your Claude environment of choice).
3. Either drag the file onto the Claude window, or open Settings â Skills â Install from file.
4. The skill registers and becomes available in matching sessions automatically.

If you want to read or modify a skill before installing, the source (`SKILL.md`, `README.md`, and any scripts) lives alongside the `.skill` bundle in the same folder.

## Contributing or forking

Each skill is independent. Fork the repo, modify the skill folder you care about, repackage with your preferred tooling, and use. If you build improvements that are broadly useful, pull requests are welcome.

## License

MIT. Use, modify, redistribute. Attribution appreciated but not required.

## About

Maintained by [@maxeckemoff](https://github.com/maxeckemoff). Skills are products of real workflow problems, not synthetic demos.
