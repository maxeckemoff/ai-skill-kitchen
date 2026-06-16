---
name: session-rename-helper
description: "Generates the correct Cowork session label for a subordinate and the steps to apply it, following the user's Identity Convention v1.0 (ID grammar PROJECT, optional SUBSCOPE, ROLE, optional number; label format 'ID [Descriptor]'). Use when the user says rename this session, what should I call this session, label this session, set the sidebar name, give this session an identity, or asks to batch-rename sessions. Takes a project code, optional subscope, role, and descriptor and returns the exact label string plus the in-app right-click rename click-path. Optionally produces a Coder Instructions MD for batch renames by editing the per-session JSON title files on disk while Claude Desktop is closed, with the required safety cautions. Does not itself edit files; it produces the label and the rename steps."
---

# Session rename helper

Cowork sidebar labels are how the org chart stays legible: a session's label should encode who it is at a glance. This skill turns a project, role, and descriptor into the exact label string per the user's Identity Convention, and gives the steps to apply it. For one session it produces an in-app rename click-path; for many sessions it can produce a Coder Instructions MD that edits the on-disk title files in a batch.

This is a sibling of `bridge-handoff-authoring` (which embeds an identity code into a new session's kickoff and gives a one-off rename step). This skill is the dedicated rename verb: it owns label composition and batch rename, and applies equally to sessions that already exist, not just newly spawned ones.

## The Identity Convention (v1.0)

Canonical source: `AI Org Chart\Identity_Convention.md`. The skill must generate labels in exactly this format; if the convention file is reachable, read it and prefer it over this summary.

- **ID grammar**: `PROJECT[-SUBSCOPE]-ROLE[-N]`
  - `PROJECT`: short uppercase project or org-group code (for example `VAT`, `GCP`, `FPA`, `SKL`, `ORG`, `COMMS`).
  - `SUBSCOPE` (optional): a narrower area inside the project (for example `PROJ` in `FPA-PROJ`).
  - `ROLE`: the role code (for example `MGR`, `ARCH`, `DEV`, `CODER`, `BLD`, `OUT`, `DATA`, `WRITER`).
  - `N` (optional): a disambiguating number when two sessions would otherwise share an ID (for example `GCP-DEV-2`).
- **Label format**: `ID [Descriptor]`, where Descriptor is a short human-readable task or scope in square brackets. Examples: `SKL-BLD [Skill Builder]`, `FPA-PROJ-ENG [Projection engine]`, `GCP-DEV-2 [AvaTax connector]`.
- Codes are uppercase and hyphenated; the descriptor is plain prose in brackets.

## Step 1: Gather inputs

Collect (or infer from session context, then confirm):

- **Project code** (required).
- **Subscope** (optional).
- **Role** (required).
- **Descriptor** (required): the short human-readable scope for the brackets.
- For a batch: the list of sessions with their target IDs and descriptors.

If a project or role code is not already established in the convention, ask rather than inventing one; new codes should be registered in the convention, not coined ad hoc.

## Step 2: Compose the ID and label

Assemble `PROJECT[-SUBSCOPE]-ROLE[-N]`, then `ID [Descriptor]`. Add the `-N` suffix only when needed to disambiguate from an existing session with the same base ID; check the session registry (`AI Org Chart\Session_Registry.md`) if reachable. Keep the descriptor short enough to read in the sidebar.

Output the final label string verbatim and ready to paste.

## Output A (default): single-session rename

Produce the label plus the in-app click-path:

```
Label: ID [Descriptor]

To apply:
1. In the Cowork sidebar, right-click (or open the "..." menu on) this session.
2. Choose Rename.
3. Paste:  ID [Descriptor]
4. Press Enter.
```

This is the default and the safe path. First-prompt instructions do NOT set the sidebar label (confirmed empirically), so the rename is always a manual or disk-level action, never something the session does to itself.

## Output B (optional): batch rename via a Coder Instructions MD

When the user wants to rename many sessions at once, produce a Coder Instructions MD (per the standing Coder Instructions MD pattern) that edits the per-session title files on disk. Mechanism (confirmed by ORG-CODER recon):

- Claude Desktop is an MSIX package, so its per-session state lives under a virtualized path:
  `%LOCALAPPDATA%\Packages\Claude_<packageid>\LocalCache\Roaming\Claude\local-agent-mode-sessions\<workspace>\<space>\`
  containing one `<local_id>.json` per session with a title field.
- The `<packageid>` segment (for example `Claude_pzs8sxrjxfjjc`) is machine and version specific. Do NOT hardcode it. The MD must locate it, for example by globbing `%LOCALAPPDATA%\Packages\Claude_*\LocalCache\Roaming\Claude\local-agent-mode-sessions\` and confirming the session JSONs are there.
- The title field key should be confirmed by reading one JSON first (the recon found the session title stored in the per-session JSON); the MD edits that field to the new label.

The Coder Instructions MD must include these safety cautions as hard requirements:

1. **Claude Desktop must be fully closed before editing.** Edits to a live session file may be overwritten or ignored. Relaunch after.
2. **Never run `Stop-Process` (or `taskkill`) against `claude*`.** The Coder is itself running inside a Claude process/terminal; killing by name can kill the Coder's own session. Ask the user to quit the app from its tray/UI instead, and have the MD verify the process is gone before editing rather than forcing it.
3. **Back up every JSON before editing** (copy the whole `local-agent-mode-sessions` tree to a timestamped backup folder first), so a bad edit is recoverable.
4. **Edit only the title field**, preserve the rest of each JSON byte-for-byte (load, change one field, write back with the same encoding), and validate each file still parses as JSON before relaunch.
5. Map each `<local_id>.json` to its intended new label via a table the MD includes (id -> label), so the Coder is not guessing which file is which.

Produce the MD under `_handoff/coder_instructions/[name]_[date].md`, list the id-to-label table, give the locate-package-id step, the backup step, the per-file edit with expected output, and a relaunch-and-verify step. Tell the Coder to report back via the bridge.

## When to produce A vs B

- One or a few sessions, or the user is at the keyboard: Output A (click-path). Simpler and zero-risk.
- Many sessions at once, or a systematic relabel after an architecture change: offer Output B, but only with the cautions above, and confirm the user has a moment to close the app.

## Anti-patterns to avoid

- Do not invent project or role codes. Use the convention; if a code is missing, ask and register it.
- Do not tell a session to rename itself via its first prompt; that does not work.
- Do not hardcode the MSIX package id; locate it.
- Do not kill processes by the name `claude`; that can take down the Coder's own session.
- Do not batch-edit JSONs without a backup and without the app closed.
- Do not use em dashes or AI-tone phrasing in labels, click-paths, or the Coder MD.

## Test triggers

Examples that SHOULD fire this skill:

- "What should I call this session? It's the Developer for the GCP BI work."
- "Rename this session to our identity convention; it's the FP&A projection engine."
- "I need to batch-rename eight sessions to the new codes. Give me something the Coder can run."

Examples that should NOT fire this skill:

- "Spin up a new Developer subordinate and write its kickoff." (that is `bridge-handoff-authoring`; this skill renames, it does not author kickoffs or bridges)
- "Rename this file from cat.txt to dog.txt." (a filesystem rename, not a session label)
- "What's our identity convention?" (a question about the convention doc, not a request to compose or apply a label)
