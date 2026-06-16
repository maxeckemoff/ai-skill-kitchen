# versioned-in-place

A Claude Cowork skill that revises a durable document in place: the new version goes on top with a header and a one-line change summary, and the prior version is preserved below in a `[SUPERSEDED]` block.

## Why it exists

Standing documents (kickoffs, briefs, specs, a canon) keep changing. Overwriting loses the history of why a decision was made; creating v2, v3 files litters the folder and splits the source of truth. This skill keeps one file with the full history stacked newest-first.

## What it produces

- A version header: `# Title (vN, date)`.
- A one-line change summary naming what the version adds, changes, or removes, signed with the editor identity and date.
- The new current content on top, a horizontal rule, then each prior version in a `[SUPERSEDED] vN-1 (date)` block, most recent superseded first.

## When it applies

- **Version in place**: durable, referenced documents undergoing a meaningful revision. This skill's job.
- **Plain overwrite**: trivial fixes and ephemeral drafts (no version block).
- **Append**: log files grow by entries, not by stacking document versions.

## What it will not do

It does not version files that already carry their own versioning, code under git or `.pq` files with a semver header, because stacking a second scheme inside conflicts with the first. It does not version logs, and it never silently drops the prior content; if a version is truly obsolete it offers to archive it with a pointer rather than delete it.

## How it fits

It is the revise verb for standing docs, alongside `bridge-handoff-authoring` (author), `bridge-relocation-shell` (relocate/retire), and `check-off-protocol` (post-integration).

## Compatibility

Works in any Cowork session with file access. No external dependencies.

## License

MIT.
