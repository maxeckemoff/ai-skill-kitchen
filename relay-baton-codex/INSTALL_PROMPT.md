# Paste-ready installation prompt template

The published version of this file pins an immutable source commit. Until that commit is recorded, replace `<PINNED-COMMIT-SHA>` and `<CHECKOUT-PATH>` before use.

```text
Fetch `https://github.com/maxeckemoff/ai-skill-kitchen` at immutable commit `<PINNED-COMMIT-SHA>` into a new local checkout at `<CHECKOUT-PATH>`. Do not use the moving branch tip as the installation source. Install the portable Relay Baton for Codex from `<CHECKOUT-PATH>/relay-baton-codex`.

First read relay-baton-codex/README.md, relay-baton-codex/SKILL.md, relay-baton-codex/install.py, and both Python files under relay-baton-codex/scripts. Verify that the source contains no runtime records, credentials, usage snapshots, Codex configuration, private reports, or real baton data. Ask me one required choice before installation: "skill only" or "skill plus global FULL signatures." Do not infer the global option.

After I choose, run relay-baton-codex/install.py with the matching option. Preserve my existing Codex AGENTS.md: the installer may append or update only its own marked section and must not replace unrelated content. Honor my CODEX_HOME when set. Keep timestamped skill and AGENTS backups outside skill discovery.

Run relay-baton-codex/scripts/test_codex_session_signature.py using synthetic fixtures. Then run the installed generator against this task's own native Codex ID, using a short seat label I choose, and explain its output. Report the installed path, whether global instructions were enabled, test results, and any tzdata requirement.

Orient me briefly to: FULL versus explicitly requested CONDENSED signatures; the DRAFTED, EMITTED, DELIVERED, SUPERSEDED, and STALE baton lifecycle; why cache behavior, plan allowance windows, and current context occupancy are separate; why provider credit units and Standard API benchmarks are not billed spend; and when CONDENSED is more efficient for routine work. Do not promise that dummy pings preserve cache or save usage.

Do not use another person's task ID, copy their metrics, change unrelated Codex configuration, or send/publish anything.
```
