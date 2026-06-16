---
name: skill-install-sync
description: "Compares the local Skill Kitchen folder against the skills currently loaded in this Cowork session and reports what is out of sync. Use when the user says sync my skills, which skills need installing, are my installed skills up to date, check for skill drift, did my skill update take, or after building or renaming a skill. Surfaces three categories: install candidates (in the Kitchen folder but not loaded this session), update candidates (loaded and in the Kitchen but the content or description differs), and stale installs (a former Kitchen skill still loaded under an old or renamed identity that no longer exists in the Kitchen). Ignores non-Kitchen skills such as document or plugin skills. Output is a short report with copy-pastable install, reinstall, and uninstall actions. Read-only; it does not install or remove anything itself."
---

# Skill install sync

Skills are built and renamed in the Kitchen folder, but the session you are in may have an older set loaded: a new skill not yet installed, a skill whose content changed since you installed it, or a skill still loaded under a name you have since renamed away. This skill diffs the Kitchen against what is loaded and tells you exactly what to install, reinstall, or remove.

It pairs with `skill-extraction-spotter` (which proposes new skills) and `skill-creator` (which builds them): once a skill exists in the Kitchen, this skill keeps the running sessions in step with it.

## What this skill can and cannot see

- It CAN read the local Skill Kitchen folder (skill folders, their `SKILL.md` frontmatter, and the `.skill` bundles).
- It CAN read the available-skills list in the current session (the loaded skill names and descriptions are in context).
- It CANNOT read the byte-hash of an already-installed bundle from inside the session. So "content differs" is detected by comparing the Kitchen `SKILL.md` description and body against the loaded skill's description, which is a reliable proxy for drift but not a true hash check. Say so when reporting an update candidate.

## Step 1: Enumerate the Kitchen skills

List the skill folders in the Kitchen (default: the user's "Claude Skill Kitchen" folder; ask if the path is unknown). For each folder that contains a `SKILL.md`, read the frontmatter `name` and `description`, and note whether a matching `[name].skill` bundle exists at the Kitchen root. This is the source-of-truth set.

## Step 2: Enumerate the loaded skills

From the available-skills list in the current session, collect the loaded skill names and their descriptions. Some of these are not Kitchen skills (document skills like docx or pdf, plugin skills, onboarding skills); keep them in a separate "out of scope" bucket so they are never flagged as stale.

## Step 3: Classify

Compare the two sets by skill name:

- **Install candidate**: present in the Kitchen, not loaded in the session. The user built or has not yet installed it here.
- **Update candidate**: present in both, but the Kitchen `SKILL.md` description or body differs from the loaded skill's description. Flag as a probable content drift (proxy, not a hash check).
- **Stale install**: loaded in the session and clearly a Kitchen-family skill, but no longer present in the Kitchen under that name. The common cause is a rename: the old name is still installed while the new name lives in the Kitchen. Pair a stale install with the renamed replacement when you can identify it.
- **Out of scope**: loaded but not a Kitchen skill. List briefly so the user sees they were considered, but do not propose removing them.

Be conservative about "stale": only flag a loaded skill as stale if it plausibly came from the Kitchen (matches the Kitchen's naming family or is a known former Kitchen name). Never flag document, plugin, or system skills as stale.

## Step 4: Output

Produce a short report with copy-pastable actions:

```
## Skill sync: Kitchen vs this session

**Install candidates** (build is in the Kitchen, not loaded here):
- [name]: install `[name].skill` from the Kitchen root (Settings > Skills > Install from file, or drag the .skill onto the window).

**Update candidates** (loaded, but the Kitchen version looks newer):
- [name]: reinstall `[name].skill` to pick up changes. (Detected by description/body diff, not a byte hash; reinstall to be safe.)

**Stale installs** (loaded, not in the Kitchen, likely renamed away):
- [old-name]: remove in Settings > Skills. Replaced by [new-name] (install that if not loaded).

**Out of scope** (not Kitchen skills, left alone): [short list]

Nothing else is out of sync.
```

Keep it scannable. If a category is empty, say "none" rather than padding.

## Anti-patterns to avoid

- Do not install or uninstall anything yourself; this skill is read-only and produces actions for the user to run.
- Do not flag non-Kitchen skills (docx, pdf, plugin, onboarding, system) as stale. They come from other sources.
- Do not claim a true hash match you cannot perform; describe update detection as a description/body proxy.
- Do not guess the Kitchen path; default to the known folder and ask if unsure.
- Do not use em dashes or AI-tone phrasing in the report.

## Test triggers

Examples that SHOULD fire this skill:

- "Sync my skills, I just built a couple and want to know what to install here."
- "Are my installed skills up to date with the Kitchen, or is anything stale?"
- "I renamed a skill; is the old one still loaded somewhere I should remove?"

Examples that should NOT fire this skill:

- "Build me a new skill that does X." (that is `skill-creator`)
- "Is this recurring work worth turning into a skill?" (that is `skill-extraction-spotter`)
- "Install this specific .skill file for me." (a direct install action, not a sync/diff request; and installation is a user action anyway)
