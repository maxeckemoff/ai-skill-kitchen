---
name: live-source-watch
description: "Watches a per-session list of external sources (Google Drive Docs and Sheets, a couple of public URLs, and local files) for changes and surfaces only the deltas as a compact one-line heads-up. Use at prompt start, or when the user says check my sources, what changed, watch this doc, or is anything new. Cheap trigger is modifiedTime (Drive) or filesystem mtime or a URL content hash; on a hit it optionally reads back a one-line what-changed and an open link, never the whole source. Reads and writes a local JSON state file (source id to last-seen modifiedTime plus optional content hash) kept off deep OneDrive paths. Cadence is every-prompt with a per-source recheck throttle (default 10 minutes; 0 means every prompt), and on-demand always bypasses the throttle. Degrades quietly if the Drive connector is not connected."
---

# Live source watch

This skill reproduces the manual pre-flight several sessions already run by hand: at the start of a prompt, glance at a small watch-list of external sources and say, in one line, which ones changed since last check. It is trigger-cheap (a modifiedTime or mtime or hash comparison), lazy on content (only the changed items get a one-line what-changed), and stateful (a local JSON file remembers what it last saw), so a session stays current on its live inputs without re-reading them every turn.

Scope is locked from the SKL-VATR scoping bridge. Build v1 against the existing Drive connector plus a local state file; no new MCP.

## The watch-list

A per-session watch-list, not one global list. Each entry:

- `id`: the source identifier. For Drive, the file ID. For a local file, its full path. For a URL, the URL.
- `type`: `drive_doc`, `drive_sheet`, `local_file`, or `url`.
- `label`: a short human name for the one-line output.
- `throttle_minutes`: per-source recheck throttle (default 10; `0` means check every prompt).
- `content_diff`: opt-in boolean; when true, on a change also fetch a one-line what-changed. Default false (trigger-only).

A representative pilot fixture (three sources) exercises both access paths: two Drive Docs (by file ID, elided here as `DRIVE_DOC_ID_A` and `DRIVE_DOC_ID_B`) and one local file (a project handoff `.md` referenced by full path). Set the near-deadline sources to `throttle_minutes: 0` so they behave as a live pre-flight does today.

## The change signal (cheap trigger, lazy content)

- **Drive Docs and Sheets**: the trigger is `modifiedTime` from the Drive connector's `get_file_metadata`. VATR-MGR confirmed empirically (SKL-VATR bridge, 2026-06-16) that `get_file_metadata` returns a usable `modifiedTime` and `read_file_content` returns the body. Compare the current `modifiedTime` against the state file's last-seen value; if newer, it changed.
- **Local files**: the trigger is filesystem mtime. Caveat (from the OneDrive coherency work): mtime on OneDrive-synced paths has multi-device skew, so treat a changed mtime as a candidate and, if `content_diff` is on, confirm with a content hash rather than trusting mtime alone.
- **URLs**: fetch the page and hash the content; compare the hash. No modifiedTime available, so the hash is the trigger.

On a hit, and only if `content_diff` is on for that source, read the body (Drive `read_file_content`, local read, or the fetched URL) and produce a one-line what-changed (which section or sheet tab moved), plus the open link. Never surface the whole changed body. Never diff the whole list, only the items that tripped the trigger (lazy).

## Cadence and throttling

- Default: run at every prompt start, gated per source by `throttle_minutes`. On a given prompt, only sources whose last check is older than their throttle are re-polled; the rest are skipped. This keeps every-prompt responsiveness while bounding cost (a 10-minute throttle caps even a 20-source list at one poll per source per 10 minutes regardless of prompt frequency).
- `throttle_minutes: 0` on a source means check it every prompt with no skip (use for a few live sources near deadlines).
- On-demand ("check my sources", "what changed") always bypasses the throttle and rechecks everything now.
- Rough ceiling: a session-start metadata poll is comfortable up to roughly 20 to 25 Drive files; beyond that, raise throttles or move the large list to a scheduled check.

## State file

Keep last-seen state in a local JSON file, not in session memory (memory is point-in-time and unreliable for this).

- Shape: `{ "<source_id>": { "last_modified": "<iso>", "last_hash": "<optional>", "last_checked": "<iso>" }, ... }`.
- Location: a stable LOCAL path, NOT a deep OneDrive-synced path (the partial-write and MAX_PATH lessons). Default convention: `C:\ClaudeArchive\watch_state\<project-or-session>_watch_state.json`. A per-project `_watch_state.json` at a shallow project path is also acceptable. The skill reads it at the start and writes it back after polling.
- On first run for a source (no state), record current modifiedTime/hash and report it as "now watching", not as a change.

## Output shape

Compact by default. At prompt start, if nothing changed, stay silent or a single quiet line; if something changed, one line plus a short list:

```
[N watched sources changed since last check]
- <label> - changed <when> - <one-line what-changed if content_diff on> - <open link>
- <label> - changed <when> - <open link>
```

Full digest only on explicit request. Mirror the pre-flight "heads suffice" rule: the point is a pointer, not the content.

## Graceful degradation

- If the Drive connector is not connected in this session, do not error. Skip the Drive-tier sources, still check local files and URLs, and note once that Drive sources are unavailable until the connector is connected.
- If a single source errors (permission, deleted), report it as an error line for that source and keep going; do not abort the whole check.

## Anti-patterns to avoid

- Do not read whole sources to detect change; use modifiedTime, mtime, or hash. Content reads are only for the changed items with `content_diff` on.
- Do not store state in session memory; use the local JSON file.
- Do not put the state file on a deep OneDrive-synced path.
- Do not poll every source on every prompt regardless of throttle; respect per-source throttles (except on-demand).
- Do not surface full changed bodies; one-line what-changed plus a link.
- Do not use em dashes or AI-tone phrasing in the output line.

## Test triggers

Examples that SHOULD fire this skill:

- (Prompt start with a watch-list configured) poll due sources and, if any changed, emit the one-line heads-up.
- "Check my sources, did anything change?"
- "Watch the VAT weekly notes doc and the FAQ doc for me."

Examples that should NOT fire this skill:

- "Read this Google Sheet and summarize every row." (that is a full read, and for large sheets is exactly what `bounded-source-interrogation` exists to avoid)
- "How much usage do I have left?" (that is `usage-check-on-prompt`)
- "Relocate this bridge to another folder." (that is `bridge-relocation-shell`)
