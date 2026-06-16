# bridge-relocation-shell

A Claude Cowork skill that relocates a bridge or handoff document set from one project folder to another and leaves forwarding shells behind, so no session breaks when the canonical path moves.

## Why it exists

In a multi-project org, bridges get re-homed as projects split and merge. The copy is easy; the hazard is the sessions whose bootstraps and memory still point at the old path. This skill standardizes the safe move: relocate, forward, confirm, and update the maps, so a relocation never silently strands a session.

It is the relocate/retire verb, paired with `bridge-handoff-authoring` (authors new bridges) and `check-off-protocol` (post-integration close-out).

## What it does

1. Separates in-scope files (the moving project's channels) from out-of-scope files (other projects' channels that stay).
2. Copies the in-scope set to the new canonical folder, preserving `_plans/handoff` and `_logs` structure.
3. Replaces each old file with a forwarding shell at the same filename: a moved-content header, the new path, and an identity-confirm acknowledgement block.
4. Leaves a folder breadcrumb listing what moved, where, and what stayed.
5. Updates auto-memory and the memory index with the new location.
6. Flags ORG-MGR to update the Session Registry, Bridge Index, and Org Chart.

It never hard-deletes the originals; the shells forward, and deletion is a separate, explicitly confirmed step taken only after every consuming session has acknowledged the move.

## The migration mechanism

The acknowledgement block in each shell is the point: a session that lands on the old path identifies itself, reads the relocated doc, updates its memory to the new path, and records a confirmation line. That self-redirect is what makes the relocation safe rather than a silent break.

## Reference asset

The skill ships a default shell template and acknowledgement block. The exact house version is being supplied by FPA-OUT (who ran the first live relocation); prefer theirs when present.

## Compatibility

Works in any Cowork session with file access to the old and new folders. No external dependencies.

## License

MIT.
