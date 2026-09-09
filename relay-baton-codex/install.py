#!/usr/bin/env python3
"""Install the portable Relay Baton for Codex skill without replacing user instructions."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import shutil
from pathlib import Path


START = "<!-- relay-baton-codex:start -->"
END = "<!-- relay-baton-codex:end -->"


def global_block(generator: Path) -> str:
    return f"""{START}
## Portable Codex session signature

For substantive final responses, run the native generator immediately before answering:
`python \"{generator.as_posix()}\" --seat \"<assigned-seat>\"`

If task-ID environment variables are unavailable, pass the current native Codex task UUID with `--session`. Include the generated FULL output unchanged, followed by `Next prompt`, `Decision needed`, or `Thread terminal`. Prompt rows default to the intersection of the last 24 hours and newest 20 prompt runs; cumulative metrics and original prompt numbers remain unchanged. If the user says `relay-baton-codex full-history`, add `--full-history` for the next reply only, then return to the bounded default. This is a recognized skill phrase, not a built-in Codex slash command or persistent setting. Preserve the rendered line `For all prompt rows on your next reply, say: relay-baton-codex full-history.` Explicit keep-alive pings are exempt. Missing data remains unavailable; benchmark figures are Standard API equivalents rather than spend. Do not reuse another task's metrics. A baton is `EMITTED` only after its exact block is durably persisted; a displayed or prepared block alone is `DRAFTED`.

Directly message an existing Codex task only when the user explicitly authorizes it or a trusted saved preference already does. Verify a unique accessible task ID, persist the self-contained prompt, and record the native tool's actual outcome. Tool success is `SENT`, not `DELIVERED`; definitive failure is `FAILED`; uncertainty is `UNCERTAIN` and blocks automatic retry. Claude Code, Cowork, imported-Claude-history-only, and unknown-surface recipients use a fenced manual relay labeled `PREPARED_MANUAL`, never native-Codex `SENT`. Do not create receipt-only loops. Existing-task authorization does not authorize new-task creation, email, Slack, publication, or public posting.
{END}"""


def merge_marked_block(path: Path, block: str) -> None:
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    if START in original or END in original:
        if original.count(START) != 1 or original.count(END) != 1:
            raise RuntimeError(f"Cannot safely update malformed marker block in {path}")
        before, rest = original.split(START, 1)
        _, after = rest.split(END, 1)
        merged = before.rstrip() + "\n\n" + block + after
    else:
        merged = original.rstrip() + ("\n\n" if original.strip() else "") + block + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(merged, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--enable-global-signatures",
        action="store_true",
        help="merge the optional signature rule into ~/.codex/AGENTS.md",
    )
    args = parser.parse_args()

    package_root = Path(__file__).resolve().parent
    source = package_root
    if not (source / "SKILL.md").is_file():
        raise SystemExit(f"Missing skill source: {source}")

    destination = Path.home() / ".agents" / "skills" / "relay-baton-codex"
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser()
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup_root = codex_home / "skill-backups" / "relay-baton-codex" / stamp
    if destination.exists():
        backup = backup_root / "skill"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(destination, backup)
        print(f"Backed up existing skill to {backup}")

    shutil.copytree(source, destination, dirs_exist_ok=True)
    print(f"Installed skill at {destination}")

    if args.enable_global_signatures:
        agents_path = codex_home / "AGENTS.md"
        if agents_path.exists():
            backup_root.mkdir(parents=True, exist_ok=True)
            agents_backup = backup_root / "AGENTS.md.before-global-merge"
            shutil.copy2(agents_path, agents_backup)
            print(f"Backed up existing global instructions to {agents_backup}")
        generator = destination / "scripts" / "codex_session_signature.py"
        merge_marked_block(agents_path, global_block(generator))
        print(f"Merged global signature instruction into {agents_path}")
    else:
        print("Global signatures remain disabled; skill installation only.")

    print("Open a fresh Codex task to refresh skill discovery.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
