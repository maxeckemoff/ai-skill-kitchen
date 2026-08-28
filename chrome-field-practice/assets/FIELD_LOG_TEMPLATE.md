# Claude in Chrome: field practice log

Durable, append-only log of field observations about Claude in Chrome browser automation, feeding the `chrome-field-practice` skill. This is where new learning lands first; it graduates into the skill's actual rules only when the threshold below is crossed.

Copy this template to the path named in the skill's "Keeping this skill current" section (or wherever your maintainer directs) the first time you have something to log. Do not re-log what the skill already codifies; log what is new since.

## How to append

New entry format, newest at top. Re-read this file from disk before appending (anchor on the "## Entries" header below, not on the entry you remember being last; another session may have written since):

```
### YYYY-MM-DD [session or role identifier]
**Tag:** MEASURED | INFERRED
**Claim:** one or two sentences.
**Evidence:** what was actually observed, or the reasoning if inferred.
**Relation to existing rules:** corroborates <rule>, contradicts <rule>, or new.
```

## Promotion threshold

A finding graduates from this log into the skill's SKILL.md or a reference file when either:

- three independent observations corroborate it, or
- one clean, reproducible measurement contradicts an existing rule outright.

Below that bar it stays here as a candidate. When a threshold is crossed, edit the skill's source, re-run its validation and packaging scripts, and hand the rebuilt `.skill` file to whoever owns install. Mark the entry PROMOTED here, with the date and which rule it became, rather than deleting it.

## Demotion

If a rule in the skill stops reproducing, do not delete it from SKILL.md or its references. Strike it in place with the date and the reason (the `versioned-in-place` convention: old text kept, visibly marked superseded). Log the demotion here too, so the log and the skill tell the same story.

## Entries

(none yet)
