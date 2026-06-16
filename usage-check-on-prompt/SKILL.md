---
name: usage-check-on-prompt
description: "Reports current Claude usage as a compact one-line status by calling the get_claude_usage MCP tool. Fires once at session start by default, and on request when the user asks how much usage is left, what their session or weekly usage is, or whether they are near a limit; optionally at one meaningful seam in a long session. Output format: [Usage: session X% (resets in Yh Zm), weekly W% (resets Sat 1AM)]. Handles the no_token and auth_expired cases by surfacing a one-line claude update needed note instead of failing, and stays silent if the get_claude_usage tool is not registered in this environment. The user can opt out for the session by saying stop reporting usage. Read-only; it only reports."
---

# Usage check on prompt

This skill gives Max ambient awareness of his Claude usage without opening the tray app: a single compact line at session start, and on demand when he asks. It reads usage through the `get_claude_usage` MCP tool and never does anything but report.

## Dependency: the claude-usage MCP

This skill calls one MCP tool, `get_claude_usage`, served by the local `claude-usage` MCP. That MCP must be registered in the environment the skill runs in.

- It was registered for Claude Code via `claude mcp add --scope user`. That scope does NOT automatically reach Cowork sessions. If `get_claude_usage` is not in the current session's tools, the MCP is not registered here.
- When the tool is absent, this skill stays SILENT (it does not nag on every prompt). At most, if the user explicitly asks for usage and the tool is missing, say once: "Usage reporting needs the claude-usage MCP registered in this environment (see the install instructions)." Do not retry every turn.
- The Coder Instructions MD that ships this skill includes the Cowork-side registration step, so once that runs the tool becomes available.

## When to fire

- **Session start (default)**: once, at the end of the first response, append the usage line. Do not interrupt the user's actual request; add it after answering.
- **On request**: whenever the user asks how much usage is left, their session or weekly percentage, or whether they are near a limit.
- **One seam (optional)**: in a long session, you may report once more at a natural break if usage has moved a lot. Do not report on every prompt.

## How to call and format

Call `get_claude_usage`. Map its response (`{session_pct, weekly_pct, session_reset_in, weekly_reset, model_breakdowns}`) to one line:

```
[Usage: session X% (resets in Yh Zm), weekly W% (resets Sat 1AM)]
```

Use the reset strings the tool returns; do not compute your own. If `model_breakdowns` is present and the user asks for detail, you may expand to a second line listing per-model percentages, but the default is the single line.

## Error handling (never crash, never fabricate)

- **no_token or auth_expired**: emit `[Usage: unavailable - run `claude update` to refresh Claude auth]`. One line, no stack trace.
- **tool not registered here**: stay silent by default (see the dependency section). Only mention it if the user explicitly asked for usage.
- **stale or rate-limited**: the MCP is responsible for caching (30s default); take whatever it returns. If it returns an explicit stale flag, you may append "(cached)".
- **Never invent numbers.** If you cannot get a real reading, say it is unavailable; do not guess a percentage.

## Opt-out

If the user says "stop reporting usage", "no usage line", or similar, suspend the session-start report for the rest of the session. Still answer a direct "what's my usage" on request.

## Anti-patterns to avoid

- Do not report on every prompt. Session start, on request, and at most one extra seam.
- Do not interrupt the user's request; append the line after answering.
- Do not crash or dump errors; degrade to the one-line unavailable note.
- Do not print the OAuth token or any credential detail.
- Do not fabricate usage numbers when the tool fails.
- Do not use em dashes or AI-tone phrasing in the status line.

## Test triggers

Examples that SHOULD fire this skill:

- (Session start, no user phrasing needed) append the usage line after the first response.
- "How much usage do I have left this week?"
- "Am I close to my session limit right now?"

Examples that should NOT fire this skill:

- "Install the usage monitor tray app." (that is a Coder install task, not this reporting skill)
- "What does the usage MCP return?" (a question about the MCP spec, not a request for the current reading)
- Every subsequent prompt in a session after the start line already fired (respect the once-per-session default).
