# Relay Baton for Codex

This package adds a portable Codex skill for task handoffs and native FULL session signatures. It does not depend on another person's project tree, account, configuration, telemetry snapshots, or private coordination files.

Installing the skill gives Codex the capability when the skill is selected. It does not force a signature onto every task. The installer offers a separate, explicit opt-in for a global `~/.codex/AGENTS.md` instruction.

FULL signatures provide every diagnostic section, but their output also becomes later context. Prompt rows therefore default to the intersection of the last 24 hours and newest 20 native prompt runs. Cumulative metrics still use the full observed record and prompt numbers do not change. The recipient can explicitly request CONDENSED signatures for routine work or say `relay-baton-codex full-history` to show every prompt row on the next reply only. That phrase is skill routing, not a built-in Codex slash command or a persistent setting. The optional global rule remains FULL unless the recipient later chooses a different policy. Cache lifetime is separate from plan reset windows; dummy keep-alive turns consume usage and this package makes no cache-retention promise.

## Requirements

- Codex with access to native rollout files under its own Codex home.
- Python 3.10 or newer available as `python`.
- On Windows, if Python reports that `America/New_York` is unavailable, run `python -m pip install tzdata` and retry.

The generator's Standard API benchmark supports Astra. Other models remain `unavailable`; this is intentional. Account meters also remain unavailable unless the user's own native snapshot is available.

## Install

Check out the repository at a trusted commit, open a terminal in this `relay-baton-codex` folder, and choose one mode:

```powershell
# Skill only. Recommended first installation.
python install.py

# Skill plus a global instruction requiring FULL signatures on substantive replies.
python install.py --enable-global-signatures
```

The installer copies `relay-baton-codex` to `~/.agents/skills/relay-baton-codex`. If that destination already exists, it creates a timestamped backup under `<CODEX_HOME>/skill-backups/relay-baton-codex/`, outside skill discovery. Global opt-in first backs up `AGENTS.md`, then appends or updates only a marked section; it does not replace unrelated instructions. When `CODEX_HOME` is set, the installer uses it for global instructions and backups; otherwise it uses `~/.codex`.

Restart or open a fresh Codex task after installation so skill discovery is refreshed.

## Verify

Run the synthetic tests without using any live task data:

```powershell
python scripts/test_codex_session_signature.py
```

Then, from a Codex task that has its own native records, test discovery with:

```powershell
python "$HOME/.agents/skills/relay-baton-codex/scripts/codex_session_signature.py" --seat "MY-SEAT"
```

If task-ID environment variables are unavailable, add `--session <your-native-Codex-task-UUID>`. Do not use somebody else's task ID or copied metrics.

For one invocation with every prompt row:

```powershell
python "$HOME/.agents/skills/relay-baton-codex/scripts/codex_session_signature.py" --seat "MY-SEAT" --full-history
```

The following invocation returns to the bounded default when `--full-history` is omitted.

## Privacy and scope

The package contains source, synthetic tests, and instructions only. It contains no runtime history, authentication material, usage snapshots, Codex configuration, private reports, real baton content, or account identifiers. Installation and tests are local; nothing is sent or published.

See [INSTALL_PROMPT.md](INSTALL_PROMPT.md) for the paste-ready, commit-pinned prompt that lets Codex fetch, install, and verify the skill after the recipient chooses whether global signatures should be enabled.
