# bridge-handoff-authoring

A Claude Cowork skill that scaffolds the warm-transfer kickoff prompt and initial bridge file for a new subordinate session in a multi-session agent architecture.

## Why it exists

Every time you spin up a new subordinate session (a Developer, an Architect, a domain specialist), you have to write its first message: who it is, what it owns, where its bridge file lives, what data it touches, what rules to load. The shape is the same every time, and writing it from scratch costs ten to twenty minutes per launch and invites omissions. This skill turns that into a fill-in scaffold.

## What it produces

1. **A paste-ready kickoff prompt** for the new session, covering role assignment, bridge file path, scope (in and out), dataset orientation with concrete paths, role-specific recipes, the standing rules to load immediately, and the expected first response.
2. **The initial bridge file** the kickoff points to, in the documented bridge format, if one does not already exist.

## The role vocabulary

The skill assigns one of the documented roles to each new subordinate:

- **Architect**: designs and reviews; deliverables are specs and rationales
- **Developer**: executes; deliverables are changed files, runs, tests
- **Coder**: narrower Developer scope for one-offs, minimal ceremony
- **Schema Expert**: maintains canonical reference docs; read-mostly
- **Subordinate specialist**: domain expert (FP&A Projection, Comms Analyst, etc.)
- **A new specialist**: when the scope is a genuinely new long-lived domain

Each role gets tailored kickoff content (for example, a Developer gets the execution loop and check-off expectation; a Schema Expert gets its re-audit trigger).

## Propagating vs. scope-specific rules

The skill separates two classes of standing rule. Rules that apply to every session (tone preferences, fact-checking discipline) live in user-level memory and propagate automatically, so they are not duplicated into each bridge. Rules that apply only to one subordinate's domain (a file-edit protocol, a versioning convention) go into that bridge's Standing Rules section. This avoids the maintenance cost of updating the same rule in many places.

## How it fits with the sibling skills

- `cowork-progressive-disclosure-helper` decides *when* a scope is ready to split off.
- `bridge-handoff-authoring` (this skill) *authors* the kickoff prompt and bridge.
- `pre-launch-warm-transfer-review` *reviews* the drafted prompt before launch.
- `architect-to-developer-ask-authoring` writes the *asks* that flow to a Developer subordinate once it exists.
- `check-off-protocol` handles what happens *after* the subordinate delivers and the user integrates.

## Compatibility

Works in any Cowork session. No external dependencies, no scripts, no API calls. Pure instructions for how Claude should author the handoff artifacts.

## License

MIT.
