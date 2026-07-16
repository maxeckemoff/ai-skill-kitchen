---
name: bridge-append-freshness-check
description: "A pre-append discipline for multi-writer bridge files: before adding an entry, re-read the target section from disk and locate the insertion point by a structural anchor (a section header, the newest-at-top convention line, a specific ID or codename), never by matching an adjacent entry you remember, which silently misses entries other sessions wrote in between and lands the new entry in the wrong section or clobbers context. Use before appending to any shared bridge or coordination doc multiple sessions write, or when the user says append to the bridge, add a bridge entry, log this to the bridge, or update the Current Instruction. Emits a three-step pre-append checklist and example structural anchors for common bridge shapes (Activity Log with newest-at-top, a Current Instruction section, Open Questions, and plain append-only logs). Complements the session-level bridge-freshness re-read; this is the append-time half."
---

# Bridge append freshness check

Bridge files are multi-writer: several sessions append to the same Activity Log, Current Instruction, or Open Questions section, asynchronously. The common failure is anchoring an append to an entry you remember seeing ("insert after the last entry, which was X"). Between your last read and your write, another session may have written entries you never saw, so an adjacent-entry anchor silently lands your entry in the wrong place, or an exact-text match fails and you clobber the section. This skill is the append-time discipline that prevents that. It complements the session-level bridge-freshness rule (re-read the bridge before acting); this covers the moment of writing.

## The three-step pre-append checklist

Run these every time before appending to a multi-writer bridge:

1. **Re-read the target section from disk, in full.** Not from your in-context copy from earlier in the session, other sessions may have written since. Read the actual current section.
2. **Locate the insertion point by a STRUCTURAL anchor, never an adjacent-entry text match.** A structural anchor is a stable landmark that does not move as entries accumulate: a section header, the convention line under it, or a specific ID/codename. Insert relative to that landmark. Do not anchor on "the entry I remember being at the top/bottom."
3. **Append, then re-read to confirm.** After writing, re-read the section and confirm your entry landed in the right place and nothing was displaced. If the write tool reports "file changed since read," that is exactly this failure mode surfacing, re-read and retry against the current content.

## Structural anchors by bridge shape

- **Activity Log, newest at top**: anchor on the `## Activity Log` header plus its `[newest at top, signed by author]` convention line. Insert your entry immediately after that convention line so it becomes the new top entry. Never anchor on the specific previous top entry; another session may have added one above it.
- **Current Instruction section**: anchor on the `## Current Instruction` header. Replace or update the content within that section (this section holds the one active directive by convention); do not append a second instruction below an unresolved one without flagging it.
- **Open Questions**: anchor on the `## Open Questions` header and add your bullet at the top of the list, so it is seen first.
- **Append-only log, newest at bottom**: the structural anchor is the true end of file. Re-read to get the real last line (do not trust a remembered tail), then append at EOF.
- **A specific thread**: when entries carry a codename or ID, anchor on that token (for example the thread codename) to place a reply next to its thread rather than by position.

## Why adjacent-entry anchors fail

- Multi-writer interleaving: entries arrive between your read and your write.
- Stale in-context copy: your memory of the section is a snapshot; the file moved on.
- Sync coherency: on synced folders (OneDrive and similar), your view can lag the real file, so a remembered "last entry" may already be superseded on disk.

A structural anchor is immune to all three because the header and convention line do not move as entries accumulate.

## Relationship to the other skills

- `cowork-progressive-disclosure-helper` and the bridge-freshness rule cover the SESSION level: re-read the bridge before you act on it.
- `bridge-append-freshness-check` (this skill) covers the WRITE level: how to append safely once you are ready to write.
- `bridge-handoff-authoring` authors new bridges; this skill is about writing into existing, shared ones.

## Anti-patterns to avoid

- Do not anchor an append on an adjacent entry you remember; use a structural landmark.
- Do not append from your in-context copy without re-reading the section from disk first.
- Do not assume your last-seen top entry is still the top; another session may have written above it.
- Do not force a write after a "file changed since read" error; re-read and re-anchor against current content.
- Do not use em dashes or AI-tone phrasing in bridge entries; they are durable records other sessions read.

## Test triggers

Examples that SHOULD fire this skill:

- "Append my status to the shared bridge Activity Log." (multi-writer; run the checklist first)
- "Log this to the bridge and update the Current Instruction for the other session."
- "Add an Open Questions bullet to the coordination doc several sessions write to."

Examples that should NOT fire this skill:

- "Write a brand-new bridge file for a new subordinate." (that is `bridge-handoff-authoring`; there are no other writers yet)
- "Re-read the bridge before you answer my status question." (that is the session-level bridge-freshness re-read, not an append)
- "Append a line to my personal single-writer notes file." (no other writers, so no interleaving risk)
