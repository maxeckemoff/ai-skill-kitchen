# skill-install-sync

A Claude Cowork skill that diffs the local Skill Kitchen folder against the skills loaded in the current session, so you know exactly what to install, reinstall, or remove.

## Why it exists

Skills are built and renamed in the Kitchen, but a given session may be running an older set: a freshly built skill not yet installed here, a skill whose content changed since you installed it, or a skill still loaded under a name you renamed away. This skill surfaces those gaps and hands you copy-pastable actions to close them.

The motivating cases: a newly built skill sitting in the Kitchen but not loaded in a manager session, and an old pre-rename skill name still loaded alongside its renamed replacement.

## What it reports

- **Install candidates**: in the Kitchen, not loaded here.
- **Update candidates**: loaded and in the Kitchen, but the Kitchen version looks newer (detected by a description and body comparison, since the session cannot read an installed bundle's byte hash).
- **Stale installs**: loaded, no longer in the Kitchen, usually an old name left behind by a rename. Paired with the renamed replacement when identifiable.
- **Out of scope**: loaded skills that are not Kitchen skills (document, plugin, system). Listed but never flagged for removal.

## What it does not do

It is read-only. It never installs or removes anything; it produces the actions for you to run in Settings. It is honest about the one thing it cannot see from inside a session, an installed bundle's hash, and treats update detection as a content-diff proxy, recommending a reinstall when in doubt.

## How it fits with the sibling skills

- `skill-extraction-spotter` proposes a new skill.
- `skill-creator` builds it into the Kitchen.
- `skill-install-sync` (this skill) keeps your running sessions in step with the Kitchen.

## Compatibility

Works in any Cowork session that can read the Skill Kitchen folder. No external dependencies.

## License

MIT.
