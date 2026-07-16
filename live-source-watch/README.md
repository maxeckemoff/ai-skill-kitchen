# live-source-watch

A Claude Cowork skill that watches a small per-session list of external sources (Google Drive Docs and Sheets, public URLs, local files) and surfaces only what changed since last check, as a compact one-line heads-up.

## Why it exists

Several sessions already run this by hand: a pre-flight glance at a few live docs to see if anything moved. This skill codifies it, cheaply. The trigger is a `modifiedTime` / mtime / content-hash comparison, not a full read, so a session stays current on its inputs without re-ingesting them every turn.

## How it works

- **Cheap trigger, lazy content.** Drive Docs and Sheets compare `modifiedTime` (from the Drive connector's `get_file_metadata`); local files compare mtime; URLs compare a content hash. Only sources that tripped the trigger, and only if content-diff is opted in, get a one-line what-changed and an open link. Whole bodies are never surfaced.
- **Local JSON state file.** Last-seen modifiedTime/hash per source lives in a local JSON file kept off deep OneDrive-synced paths, not in session memory.
- **Configurable cadence.** Every prompt start by default, gated by a per-source recheck throttle (default 10 minutes; `0` means every prompt). On-demand ("check my sources") always rechecks now. The throttle bounds cost even for larger lists.

## Scope (v1)

Built against the existing Drive connector plus a local state file, no new MCP, per the locked SKL-VATR scoping. Drive and local files are tier 1; public URLs via fetch-plus-hash are tier 2. Zoho Connect is out of scope for v1. The VATR pilot fixture (two Drive Docs plus one local file) exercises both access paths.

## Graceful degradation

If the Drive connector is not connected, it skips the Drive-tier sources, still checks local files and URLs, and says so once rather than erroring. A single failing source is reported and skipped; the check does not abort.

## How it fits

- `live-source-watch` (this skill) keeps a session current on its live inputs.
- `bounded-source-interrogation` is the companion for reading a large source cheaply when you do need its content.
- `usage-check-on-prompt` is the sibling session-start reporter for Claude usage.

## Compatibility

Works in any Cowork session with the Drive connector connected (for Drive sources) and local file access. No new MCP; uses a local state file.

## License

MIT.
