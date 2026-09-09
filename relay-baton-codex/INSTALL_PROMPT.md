# Paste-ready installation and orientation prompt

This prompt pins the reviewed source commit `3571c5050c1bbd53b29360f4ded827ec821bf974`.

```text
Fetch `https://github.com/maxeckemoff/ai-skill-kitchen` at immutable commit `3571c5050c1bbd53b29360f4ded827ec821bf974` into a new private local checkout outside any existing repository. Choose and report the absolute checkout path. Verify that HEAD is exactly the pinned commit; do not use a moving branch tip as the installation source. Install the portable Relay Baton for Codex from the checkout's `relay-baton-codex` directory.

First read relay-baton-codex/README.md, relay-baton-codex/SKILL.md, relay-baton-codex/install.py, and both Python files under relay-baton-codex/scripts. Verify that the source contains no runtime records, credentials, usage snapshots, Codex configuration, private reports, or real baton data. Ask me one required choice before installation: "skill only" or "skill plus global FULL signatures." Do not infer the global option.

After I choose, run relay-baton-codex/install.py with the matching option. Preserve my existing Codex AGENTS.md: the installer may append or update only its own marked section and must not replace unrelated content. Honor my CODEX_HOME when set. Keep timestamped skill and AGENTS backups outside skill discovery.

Run relay-baton-codex/scripts/test_codex_session_signature.py and relay-baton-codex/scripts/test_dispatch_policy.py using synthetic fixtures. Then run the installed generator against this task's own native Codex ID, using a short seat label I choose, and explain its output. Report the installed path, whether global instructions were enabled, test results, and any tzdata requirement.

Orient me briefly to: FULL versus explicitly requested CONDENSED signatures; the default prompt-row intersection of last 24 hours and newest 20; the exact `relay-baton-codex full-history` phrase that expands the next reply only; why that phrase is skill routing rather than a built-in slash command; the DRAFTED, EMITTED, SENT, DELIVERED, SUPERSEDED, STALE, FAILED, and UNCERTAIN baton lifecycle; why cache behavior, plan allowance windows, and current context occupancy are separate; why provider credit units and Standard API benchmarks are not billed spend; and when CONDENSED is more efficient for routine work. Explain that Codex credit billing covers cache creation processing inside full-rate noncached input, reused cached input is 0.1x, `cache-write unmeasured*` preserves the raw field without claiming actual creation volume, and direct API price semantics are a separate benchmark. Confirm that cumulative metrics and original prompt numbers do not change when display rows are bounded. Do not promise that dummy pings preserve cache or save usage.

Also explain direct dispatch: existing Codex tasks may be messaged only after my explicit authorization or a trusted saved preference; recipients must resolve uniquely; the exact prompt and actual tool result are persisted; SENT is not DELIVERED; FAILED and UNCERTAIN are recorded honestly; UNCERTAIN blocks automatic retry; and no receipt-only loop is created. Show that Claude Code, Cowork, imported-Claude-history-only, and unknown-surface destinations produce a fenced manual relay labeled PREPARED_MANUAL rather than native-Codex SENT. Existing-task authorization does not grant new-task, email, Slack, publication, or public-posting permission. Cowork auto-injection is outside this initial implementation, and no universal claim should be made about every Claude environment's available tools.

Do not use another person's task ID, copy their metrics, change unrelated Codex configuration, or send/publish anything.
```
