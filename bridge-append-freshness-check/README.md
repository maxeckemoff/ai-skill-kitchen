# bridge-append-freshness-check

A Claude Cowork skill that enforces a safe pre-append discipline for multi-writer bridge files, so a new entry never lands in the wrong section or clobbers context another session wrote.

## Why it exists

Bridge files are written by several sessions asynchronously. The common failure, surfaced from a live incident, is anchoring an append to an entry you remember ("insert after the last one I saw"). Between your read and your write, another session may have added entries you never saw, so an adjacent-entry anchor silently misplaces your entry or an exact-text match fails and clobbers the section. This skill is the append-time half of bridge freshness; the session-level re-read is covered by the bridge-freshness rule.

## The discipline

Three steps before every append to a shared bridge:

1. Re-read the target section from disk in full (not your in-context copy).
2. Locate the insertion point by a structural anchor, a section header, the "newest at top" convention line, or a specific ID/codename, never by matching a remembered adjacent entry.
3. Append, then re-read to confirm it landed correctly. Treat a "file changed since read" error as this exact failure mode: re-read and re-anchor.

## Structural anchors it provides

Worked anchors for the common bridge shapes: an Activity Log with newest-at-top, a Current Instruction section, an Open Questions list, a plain append-only log (newest at bottom), and thread-tagged entries anchored by codename. Each is a landmark that does not move as entries accumulate, which is what makes it immune to interleaving, stale context, and sync lag.

## How it fits

- The bridge-freshness rule and `cowork-progressive-disclosure-helper` cover the session level (re-read before acting).
- `bridge-append-freshness-check` (this skill) covers the write level (append safely).
- `bridge-handoff-authoring` authors new bridges; this is for writing into existing, shared ones.

## Compatibility

Works in any Cowork session that writes shared coordination files. No external dependencies.

## License

MIT.
