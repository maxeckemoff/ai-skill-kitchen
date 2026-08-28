# Zoho Analytics-specific gotchas

These are illustrations of a CLASS of problem, kept separate because they are application-specific, not general Chrome behavior. Load this only when the current target is Zoho Analytics.

- A view description silently rejects input over 250 characters, with an inline red message and no toast. Check the field's own validation state, not just whether the save call returned.
- A dialog re-centers when closed and reopened. This is the fix for the off-screen-button case in SKILL.md's diagnosis ladder (step 3).
- Menus render into a portal with a high z-index and their own class. Search the whole document for them, not just the widget's subtree.
- The app leaves an invisible full-viewport `freezeLayer` behind after some failed operations, at `opacity: 0` with a high z-index. It blocks every click while being invisible in screenshots. This is the concrete case behind SKILL.md's diagnosis-ladder step 2 (an invisible overlay on top).

If you are automating a different application and find an analogous gotcha, do not add it here. Start a new per-application appendix file instead (for example `references/<application-name>-appendix.md`), and add one pointer line to it from SKILL.md's "Further reference" section.
