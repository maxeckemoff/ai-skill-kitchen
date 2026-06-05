# cowork-progressive-disclosure-helper

A Claude skill that replaces Cowork's surprise automatic compaction with deliberate, user-driven session management. When a session approaches context pressure or hits a natural break point, the skill alerts you with a structured heads-up and offers three options: continue, checkpoint, or bifurcate into a subordinate sister session.

## Why it exists

Cowork's default behavior at context limits is to silently summarize earlier messages into an opaque compressed form. This works, but you lose control over what survives. For high-fidelity work (tax, compliance, data analysis, anything where specific facts matter) automatic compaction can drop the wrong details.

This skill flips the model: you stay informed about pressure and choose what to preserve, summarize, or spin off into a new session.

## How alerting works

The skill fires at four escalating thresholds (~50%, ~65%, ~80%, ~90% of estimated context usage), plus on activity triggers (heavy tool calls, multiple file reads, large web fetches) and natural transition triggers (topic shifts, completed deliverables, scope changes). It fires each threshold only once per session to avoid being noisy.

You can also invoke it explicitly any time by asking about context, compaction, session length, or bifurcation.

## What the alert looks like

A compact appendix to the response, not a wall of text:

```
---
### Session pressure heads-up

Estimate: approximately X% used (rough).
Trigger: [one-line reason for alert].
Recommendation: [continue | checkpoint | bifurcate].

[1-2 sentence rationale.]

If you want to bifurcate: tell me which scope to spin off and I will produce a handoff doc.
If you want to checkpoint: tell me and I will produce a fidelity-preserving summary.
If you want to continue: no action needed, I will alert again at the next threshold.
---
```

## The six-level intervention ladder

The skill surfaces a graduated set of options ranging from no-action to full session reorganization. You pick whichever level fits the moment, or override the skill's recommendation up or down.

**Level 0: Continue.** Do nothing. Accept eventual auto-compaction. Best when pressure is moderate and you're mid-task.

**Level 1: Inline recap.** A 3-to-5 sentence "where we are" snapshot appended to the response. Not saved externally. Best at the first alert threshold (~50%) so you have a clean orientation point in your scrollback.

**Level 2: External checkpoint.** A structured state summary you save outside the session. The work continues in place. Best at milestone moments when you want a recoverable state record but aren't ready to move work elsewhere.

**Level 3: Bifurcate (single split).** One specific scope spins off into a sister session with a handoff document. The current session continues with what remains. Best when one well-defined sub-task is mature enough to live on its own.

**Level 4: Multi-way split.** The session decomposes into a thin parent (or "index session") plus N children, one per scope. Each child gets a handoff; the parent retains a compact index of what went where. Best when several scopes have accumulated and the cleanest answer is to fan them out.

**Level 5: Full reorganization.** The current session becomes donor material. A fresh tree is started in a project with a new 