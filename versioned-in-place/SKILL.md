---
name: versioned-in-place
description: "Revises a durable, non-log document (kickoff, brief, spec, standing doc, canon) in place by prepending the new version with a version header and a one-line change summary, and pushing the prior content into a [SUPERSEDED] block below a horizontal rule, kept for historical context. Use when the user says version this in place, revise but keep the old version, supersede the current version, update this spec but keep history, or bump the version of a standing doc. Distinct from log files, which append entries rather than stacking whole documents. Includes criteria for when to version versus plain-overwrite versus append, the version-header and SUPERSEDED-block conventions, the change-summary format, and an anti-pattern list (ephemeral drafts, and files that carry their own external versioning such as code under git or .pq semver headers)."
---

# Versioned in place

Durable coordination documents (kickoff prompts, briefs, specs, standing docs, a canon) get revised as understanding changes. Overwriting loses the history of why; spinning up vN files litters the folder. This skill revises in place: the new version sits on top with a header and a one-line change summary, and the prior version is preserved below in a `[SUPERSEDED]` block. One file, full history, newest first.

This is the revise verb for standing documents. It is distinct from log files (which append timestamped entries) and from relocation (`bridge-relocation-shell`).

## When to version vs overwrite vs append

Decide first; not every edit should stack a version.

- **Version in place** when the file is a durable, referenced document (kickoff, brief, spec, standing doc, canon, convention) AND the change is a meaningful revision someone might later need to compare against. This is the case this skill handles.
- **Plain overwrite** (no version block) when the change is trivial (a typo, a path fix) or the document is an ephemeral draft no one will need the prior state of. Versioning here is just clutter.
- **Append, do not version**, when the file is a log (activity log, bridge Activity Log, changelog). Logs grow by adding entries at the top or bottom; they do not stack whole-document versions.

If unsure whether a doc is durable enough to version, ask; default to versioning for anything other sessions read as canon.

## The structure

Produce the file in this shape (newest version on top):

```markdown
# [Document Title] (v[N], [YYYY-MM-DD])

> Revised by [EDITOR-ID] on [YYYY-MM-DD]. Change summary: [one line: what this version adds, changes, or removes versus v[N-1]]. Prior version retained below the rule as v[N-1], superseded but kept for historical context.

[the new, current content]

---

## [SUPERSEDED] v[N-1] ([YYYY-MM-DD])
Change summary at the time: [its one-liner]

[the previous version's content, verbatim]

---

## [SUPERSEDED] v[N-2] ([YYYY-MM-DD])
[...older versions stack below, most recent superseded first...]
```

Each revision: lift the current top content into a new `[SUPERSEDED] v[N-1]` block directly under the rule (above any older superseded blocks), then write the new v[N] content and header on top. The superseded stack is ordered most-recent-first.

## The version header and change summary

- **Header**: `# [Title] (v[N], [date])`. Increment N from the highest version present; if the doc has no version yet, the current state becomes v1 and your revision becomes v2.
- **Change summary**: one line in the version note, naming what changed versus the prior version (adds / changes / removes). Sign it with the editor identity and the date. This is the changelog; keep it to a line, not a narrative.
- Use the user's date (their local date), not a session-start date.

## Managing the superseded stack

- Keep meaningful versions; do not stack a new version for every trivial save.
- If the stack grows long (several superseded versions deep), offer to archive the oldest blocks to a separate `[Title]_history.md` and leave a pointer, so the live doc stays readable. Do this only with the user's ok.

## Anti-patterns to avoid

- Do not version ephemeral drafts or trivial fixes; overwrite those.
- Do not version files that carry their own external versioning: code under git, or files with a semver header like the VAT engine `.pq` files. Those have a versioning system already; stacking a second one inside the file conflicts with it.
- Do not version log files; append to them instead.
- Do not drop the prior content; the whole point is to retain it. If it is truly obsolete, archive it with a pointer rather than deleting silently.
- Do not reorder or rewrite superseded blocks; they are historical record. Only add new ones on top of the stack.
- Do not use em dashes or AI-tone phrasing in the header or change summary.

## Test triggers

Examples that SHOULD fire this skill:

- "Revise this kickoff prompt but keep the old version below for history."
- "Bump this spec to v3 in place and supersede the current one."
- "Update the standing brief and stack the prior version underneath."

Examples that should NOT fire this skill:

- "Add an entry to the bridge activity log." (a log appends; it does not stack document versions)
- "Fix this typo in the doc." (a trivial overwrite; no version block needed)
- "Bump the semver header in this .pq query." (that file has external versioning; do not add a second scheme inside it)
