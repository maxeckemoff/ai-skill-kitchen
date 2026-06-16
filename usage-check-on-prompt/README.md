# usage-check-on-prompt

A Claude Cowork skill that reports current Claude usage as a compact one-line status, so you have ambient awareness of your session and weekly limits without opening a tray app.

## Why it exists

Running many sessions, it is easy to hit a usage limit unaware. This skill surfaces a single line at session start and on demand, reading real numbers through a local MCP rather than guessing.

## What it shows

```
[Usage: session X% (resets in Yh Zm), weekly W% (resets Sat 1AM)]
```

It fires once at session start (appended after the first response, never interrupting), and any time you ask how much usage is left. In a long session it may report once more at a natural break, but never on every prompt.

## Dependency

It calls the `get_claude_usage` tool from the local `claude-usage` MCP. That MCP is registered for Claude Code at user scope, which does not automatically reach Cowork; the Coder Instructions MD that ships this skill includes the Cowork-side registration. If the tool is not registered in the current environment, the skill stays silent rather than nagging.

## Failure behavior

It never crashes or fabricates. On expired auth it emits a one-line "run `claude update`" note; if the tool is missing it stays quiet; it never prints the OAuth token. Say "stop reporting usage" to suspend the session-start line.

## How it fits

It is the consumer of the `claude-usage` MCP (built separately per the MCP spec). It pairs with the tray app `usage-monitor-for-claude` for users who want both a tray view and an inline line.

## Compatibility

Works in any Cowork session where the `claude-usage` MCP is registered. No other dependencies.

## License

MIT.
