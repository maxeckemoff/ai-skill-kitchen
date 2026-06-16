---
name: bridge-relocation-shell
description: "Relocates a Cowork bridge or handoff document set from one project folder to another and leaves forwarding shells behind, so sessions whose bootstraps still point at the old path self-redirect and self-update. Use when the user says relocate this bridge, move the handoff to another folder, clean one project's docs out of another project, leave a shell or pointer or forwarding stub, point the old docs to the new ones, or have each session confirm it read the new location and updated memory. Copies in-scope files to the new canonical folder preserving the _plans/handoff and _logs structure, replaces each old file (same filename, content cleared) with a shell header plus the new path plus an identity-confirm acknowledgement block, writes a folder breadcrumb, updates auto-memory and the memory index, and flags ORG-MGR to update the registry, bridge index, and org chart. Does not hard-delete originals. Distinguishes in-scope files from other projects' channels that stay."
---

# Bridge relocation shell

As the org's projects split and merge, bridge and handoff documents get re-homed from one project folder to another. Doing it by hand is error-prone: the danger is not the copy, it is the sessions whose bootstraps and memory still point at the old path and silently break. This skill standardizes the safe relocation: copy to the new home, replace each old file with a forwarding shell that carries an identity-confirm acknowledgement, breadcrumb the old folder, update memory, and flag the org coordinator to update the maps. Originals are never hard-deleted; the shells forward.

This is the relocate/retire verb in the toolkit. It pairs with `bridge-handoff-authoring` (which authors NEW bridges) and `check-off-protocol` (post-integration). Different verb, different inputs, so it is its own skill.

## Step 1: Determine scope

Identify exactly which files move and which stay. The common case is pulling one project's channels out of a shared folder while leaving other projects' channels in place.

- **In-scope**: the specific bridge/handoff/log files for the project being re-homed. Name them.
- **Out-of-scope**: other projects' channels in the same old folder. They stay untouched. List them explicitly so nothing is swept along.

If you cannot tell which files belong to the moving project, ask rather than guessing; a wrong move breaks another project's sessions.

## Step 2: Copy to the new canonical folder

Copy the in-scope files to the new folder, preserving the structure (`_plans/handoff/`, `_logs/`, etc.). The new location is the canonical one after this. Do not modify the copied content beyond what the relocation requires.

## Step 2.5: CHECK-FIRST classification (do this before any shelling)

A shell forwards a READER, but it does not fix something that WROTE to the old path. Before shelling anything, find what still points at the moving files and classify each reference, so write-targets are not silently broken (this is the v1.1 gap surfaced by the GCP relocation, where staying files wrote to a moving path; the FP&A move did not hit it because its staying files were reader-only).

1. Grep every staying file, plus known consumer bootstraps and configs, for references to the moving paths or filenames.
2. Classify each hit:
   - **doc-read**: only reads the moved file. A forwarding shell handles it; no extra action.
   - **write-target**: writes to or depends on the old path as a live target (a bootstrap that opens it for append, a script that writes there, a configured output path). A shell will NOT save it; it needs a consumer-path update, an explicit leave-this-file-unshelled decision, or an accept-divergence call.
   - **ambiguous**: cannot tell from the reference whether it reads or writes. Treat as needing a look.
3. Output a per-file disposition list (file -> the hit -> classification -> proposed action) BEFORE shelling, and GATE: get owner approval for every write-target and ambiguous hit. Only doc-read hits proceed automatically.

The breadcrumb's list of files that STAY (Step 4) is exactly the set to grep here; the two steps dovetail.

## Step 3: Replace each old text file with a forwarding shell

At each OLD text file, replace the content with a SHELL at the SAME FILENAME (do not rename), so existing pointers still resolve. Use FPA-OUT's house template (verbatim, parameterized). Placeholders: `{FILENAME}` original filename kept as-is; `{NEW_CANONICAL_PATH}` full path to the relocated file; `{REASON}` one-line why; `{OLD_PROJECT}` old project folder; `{NEW_FOLDER}` new canonical folder; `{CLUSTER}` cluster name; `{DATE}` YYYY-MM-DD.

```
# [ SHELL - CONTENT MOVED ]  {FILENAME}

> **THIS FILE IS A SHELL. Its working content has been cleared and relocated.**
> **Canonical version (read this):** `{NEW_CANONICAL_PATH}`
> Relocated {DATE}, {REASON}. If a {CLUSTER} bridge/handoff file is missing from `{OLD_PROJECT}`, it now lives under `{NEW_FOLDER}`.
> Do NOT add working content to this shell - edit the file at the new path.

## Action required of any session that opens this shell
1. Identify yourself by your current identity (your own awareness of who you are).
2. Open and read the relocated document at the new path above.
3. Update your own memory with the new {CLUSTER} handoff location.
4. Append ONE confirmation line in the block below (do not edit others lines).

### Acknowledgements (append below)
- <your-identity> - read relocated {FILENAME} and updated memory - <YYYY-MM-DD>
```

The acknowledgement block is the migration mechanism: each session that lands on the shell self-redirects, updates its memory, and records that it did. That is what makes the move safe rather than a silent break.

**Must-keep element, and shell drift (FPA-OUT field note).** The one element that must survive is the canonical-path pointer (`{NEW_CANONICAL_PATH}`). Sessions that redirect through a shell sometimes rewrite it into a terser "MOVED - redirect" stub, or just append an acknowledgement; both are fine. Do not assume the shell stays byte-stable, and do not restore a session's terser stub back to the full template as long as the canonical pointer is intact.

**OneDrive mtime caveat.** Shells in OneDrive-synced folders inherit multi-device mtime skew, so a file's modified-time is not reliable evidence of when it was relocated or last touched. The dated entries INSIDE the file (the relocation date in the header, the acknowledgement dates) are authoritative over the filesystem mtime.

**Binary and asset folders (FPA-OUT field note).** Files that cannot carry a markdown shell (deck .pptx, images, other binaries) do NOT get per-file shells. Leave ONE folder-level redirect README (for example `_DECKS_RELOCATED_README.md`) in that folder pointing at the new location. Per-file shells for text docs; one folder-level redirect for binary or asset folders.

## Step 4: Leave a folder breadcrumb

Write a `_RELOCATED_README.md` (or `_[CLUSTER]_RELOCATED_README.md`) in the old folder using FPA-OUT's house breadcrumb format (verbatim, parameterized). Placeholders: `{CLUSTER}`, `{NEW_PROJECT}`, `{OLD_PROJECT}`, `{NEW_FOLDER}`, `{DATE}`, `{SESSION-LIST}` the cluster's session ids, `{CANONICAL-FILE-GLOBS}` what moved, `{OTHER-CLUSTER}` the staying owner, `{STAYING-FILE-LIST}` the explicit files that remain.

```
# {CLUSTER} files relocated -> "{NEW_PROJECT}" ({DATE})

We are separating pure {CLUSTER} work out of the {OLD_PROJECT} folder. The {CLUSTER} bridge and all {CLUSTER} handoff files now live at:

    {NEW_FOLDER}

**If you are a {CLUSTER} session ({SESSION-LIST}) and a bridge or handoff file you expect is missing here, CHECK "{NEW_PROJECT}" FIRST.**

Canonical {CLUSTER} files there include: {CANONICAL-FILE-GLOBS}.

The files that REMAIN in this folder are {OTHER-CLUSTER}, not {CLUSTER}: {STAYING-FILE-LIST}.

NOTE: the {CLUSTER} originals may still be present in THIS folder pending final cleanup; treat the copies in "{NEW_PROJECT}" as canonical going forward.
```

The `{STAYING-FILE-LIST}` here is the same set the CHECK-FIRST pass (Step 2.5) greps for references into the moving set; the breadcrumb and the classification dovetail.

## Step 5: Update auto-memory

Add a `reference` memory entry ("the X bridge set now lives in NEW_FOLDER; check there first if a bridge looks missing") plus a one-line `MEMORY.md` index pointer. This keeps your own future self from chasing the old path.

## Step 6: Flag the org coordinator

Signal ORG-MGR (via the appropriate ORG bridge) to update the Session Registry, the Bridge Index, and the Org Chart with the new locations. The relocation is not fully landed until those maps reflect it.

## Do not hard-delete the originals

The shells preserve the old paths as forwarders. Deleting them would break any session that has not yet re-read and self-updated. Deletion is a separate, explicitly confirmed step taken only after every consuming session has acknowledged the move (the acknowledgement lines tell you when that is true).

## Anti-patterns to avoid

- Do not move out-of-scope files. Other projects' channels in the same folder stay.
- Do not shell a write-target without owner approval. A shell forwards readers only; run the Step 2.5 CHECK-FIRST pass and gate write-target and ambiguous hits first.
- Do not put per-file markdown shells in a binary/asset folder; use one folder-level redirect README there.
- Do not rename files during the move; the shell must sit at the original filename to forward correctly.
- Do not hard-delete originals as part of this skill; leave forwarding shells.
- Do not skip the acknowledgement block; it is what prevents silent breakage.
- Do not forget to flag ORG-MGR; an unmapped relocation is a half-done one.
- Do not use em dashes or AI-tone phrasing in shells, breadcrumbs, or memory entries.

## Test triggers

Examples that SHOULD fire this skill:

- "Relocate the FP&A bridge set out of the VAT engine folder into the FP&A project, and leave forwarding shells."
- "Move these handoff docs to the new folder and have each session confirm it read the new location and updated memory."
- "Clean the COMMS docs out of Maintain VAT Engine; point the old paths at the new ones."

Examples that should NOT fire this skill:

- "Spin up a new bridge for a new subordinate." (that is `bridge-handoff-authoring`)
- "Delete these old files." (this skill leaves forwarding shells; hard deletion is a separate confirmed step)
- "Rename this session to the identity convention." (that is `session-rename-helper`)
