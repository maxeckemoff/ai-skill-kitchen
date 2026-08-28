---
name: chrome-field-practice
description: "Field-tested diagnostic practice for browser automation with Claude in Chrome: a tab-visibility precheck before any click, drag, or screenshot, plus an ordered diagnosis ladder for a page that stops responding. Use whenever a session is about to click, fill a form, drag-and-drop, screenshot, or otherwise automate a web page, and especially when it already looks broken: a screenshot times out or comes back blank, a click reaches the element but nothing happens, a hover-menu will not open, a drag will not register, or the renderer looks frozen. Complements, not replaces, the claude-in-chrome skill: that one governs which mcp__claude-in-chrome__* tools to load; this one governs what to verify before trusting page state and how to diagnose failures once those tools are loaded. Claims are tagged MEASURED or INFERRED from field logs. The skill grows by logging new observations and promoting corroborated ones into rules, never by silently upgrading a guess into a fact."
---

# Claude in Chrome: field practice

One governing rule before anything else: every claim in this skill is tagged **MEASURED** (directly observed and reproduced) or **INFERRED** (reasoned but not independently verified). Keep the tag when you act on a claim, and never promote an INFERRED claim to a flat rule without saying so. A plausible-but-wrong cause got written down as fact once (section 4, below) and cost hours. That is the entire reason this skill exists.

This skill complements the `claude-in-chrome` skill, it does not replace it. That skill governs which `mcp__claude-in-chrome__*` tools to load before starting. This skill governs what to check before trusting what those tools report, and how to diagnose it when a page stops cooperating.

## 1. Precheck: is the tab actually visible? (MEASURED)

Run this in the target tab before any click, drag, hover, or screenshot:

```js
JSON.stringify({vis: document.visibilityState, focus: document.hasFocus()})
```

If `vis` is `"hidden"`, stop. Do not retry the gesture, and do not just increase timeouts. Tell the user instead.

This matters because a hidden tab produces every symptom of a broken web app while nothing is actually broken:

- `Page.captureScreenshot` times out after 30 seconds, repeatedly.
- Hover-revealed menus never open. The click reaches the right element (`document.elementFromPoint` returns the icon itself, nothing in the way) and the app does nothing, because the menu path needs a paint cycle a hidden tab does not get.
- Drag feedback does not render.
- Meanwhile DOM reads, `elementFromPoint`, JS execution, and API calls all keep working perfectly, which is exactly what makes this look like an application bug instead of a tab-state problem.

Give the user these causes, in order of likelihood, if the tab comes back hidden:

1. The tab is not the active tab in its window.
2. The window is on another virtual desktop (Windows: Ctrl+Win+Arrow).
3. The window is minimized.
4. The window is fully occluded by another window.

INFERRED, well-supported: this is Chrome's own tab-lifecycle throttling. Not an extension, not the site, and not Energy Saver alone (see section 4).

## 2. When a click does nothing, diagnose in this order

1. **Is the tab hidden?** Run the precheck above first, every time. Most "broken" clicks are this.
2. **Is something invisible on top?** Run `document.elementFromPoint(x, y)` at the page coordinate and see what actually comes back. A full-viewport transparent overlay is a common culprit and will not show up in a screenshot. (Concrete example in `references/zoho-analytics-appendix.md`.)
3. **Is the target off-screen?** A dialog centered for a tall viewport can place its button below a shrunken one. `getBoundingClientRect` will still report a plausible-looking position. Fix: close and reopen the dialog so it re-centers. Do not keep clicking the same spot.
4. **Is the element hover-gated?** Some toolbars only mount on hover and will not appear in a screenshot even while present. Find them through the DOM, then hover-then-click in the same batch.
5. **Did the hover actually fire?** If the pointer is already sitting at that coordinate, no `mousemove` event fires and hover state may never engage. Move somewhere else first, then hover.

Work this list top to bottom before trying the gesture again. Retrying a gesture that cannot work is the expensive mistake this skill exists to prevent.

## 3. Screenshots are not evidence (MEASURED)

In this environment, screenshots have, on separate occasions: timed out entirely; returned a frame missing an element the DOM confirmed was visible and correctly positioned; and returned at a different effective scale than the previous capture in the same tab.

- Verify state through the DOM or the application's own API, never from a screenshot alone.
- After any write, confirm with the app's API (read the record back) and note that confirmation, not the screenshot, as your evidence.
- Screenshots are still useful for orientation and for reading unfamiliar UI. They are orientation, not proof.

## 4. A caution worth keeping verbatim: the Energy Saver misdiagnosis

On one occasion the symptom set in section 1 appeared, and the hypothesis adopted was Chrome's Energy Saver setting. The user disabled it, the symptoms cleared, and the theory got written down as fact.

It was almost certainly a confound. Disabling that setting required bringing the browser window to the foreground, which also un-hides the tab. The variable that actually changed was not the one that got credited. The measured cause, found later, was tab visibility (section 1).

Apply this whenever a fix involves the user touching the browser: ask whether foregrounding the window is the real variable before crediting whatever setting they happened to change. This is why every claim in this skill carries its tag, and why the log described below never lets a single observation become a rule on its own.

## Further reference (load only when the symptom matches)

- **Coordinate drift, batching, and gesture ordering**: read `references/coordinates-and-gestures.md` when clicks are landing in the wrong place, a batch spans a re-render, or a drag-and-drop is not registering.
- **Password managers and other extensions**: read `references/extensions-and-conjecture.md` when a form field is being decorated, intercepted, or autofilled, or when deciding whether to re-enable a disabled extension. Marked CONJECTURE where the source material is conjecture; do not treat that part as measured.
- **Application-specific gotchas**: read `references/zoho-analytics-appendix.md` if the current target is Zoho Analytics. This is application-specific, not general Chrome behavior, and is kept separate on purpose. If you are automating a different application and find an analogous gotcha, start a new file the same way rather than folding it in here.

## Keeping this skill current

This skill is meant to keep learning, but a Cowork session cannot edit its own installed copy: skill files on disk are a read-only cache, and anything written there is discarded. Field learning happens through a log and the skill's source files, not in place. Follow this loop:

1. **Log it.** When you observe something new, whether it corroborates a rule here, contradicts one, or is a fresh finding, append a dated entry to the durable field log (a starter template ships with this skill at `assets/FIELD_LOG_TEMPLATE.md`; the log itself lives in the project where this skill's source notes live, at `_plans/handoff/CIC_Field_Practice_Log.md`, create it there from the template if it does not yet exist, or ask where your maintainer wants it if that path is not reachable from this session). Tag the entry MEASURED or INFERRED. Never write a single observation straight into this skill's rules.
2. **Promote on threshold.** A finding graduates from the log into this skill's actual rules when either: three independent observations corroborate it, or one clean, reproducible measurement contradicts an existing rule outright. Below that bar, it stays in the log as a candidate, not a rule.
3. **Demote, do not delete.** If a rule stops reproducing, strike it in place with the date and the reason, in the style the `versioned-in-place` skill uses for standing documents: keep the old text visible and marked superseded, do not erase it. The Energy Saver story in section 4 is the worked example of why: the wrong rule was informative precisely because it was left legible, not scrubbed.
4. **Regenerate, do not pretend to self-edit.** When a promotion or demotion crosses the threshold, edit the skill's source files (not the installed copy), re-run validation and packaging, and hand the rebuilt `.skill` file to whoever owns install for this environment. Say plainly what happened: "the field log crossed the promotion threshold on X, here is the regenerated skill, please install it," not "I updated the skill."

## Test triggers

Examples that SHOULD fire this skill:

- "Why did my screenshot just time out again in that dashboard tab?"
- "The click landed but nothing happened, this menu won't open."
- "I'm about to automate this page: click through a few filters and take screenshots to confirm."
- "The page looks frozen, nothing I click is doing anything."

Examples that should NOT fire this skill:

- "What tools do I need to load to start a Claude in Chrome session?" (that is the `claude-in-chrome` tool-loading skill)
- "Summarize this webpage's content for me." (a plain read, no automation or diagnosis involved)
- "Write a script that calls the API directly instead of going through the browser." (no browser involved)
