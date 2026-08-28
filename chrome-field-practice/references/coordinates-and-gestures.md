# Coordinate drift, batching, and gesture ordering

Load this when clicks are landing in the wrong place, a batch spans a re-render, or a drag-and-drop is not registering.

## Coordinate handling (MEASURED)

The tool's click coordinates and the page's CSS pixel coordinates are related by a scale factor that differs per window and changes when the window resizes or the page zoom differs. Observed viewport widths in one session: 2327, 2220, 1295. Observed page zoom on one window: about 65 percent (`innerWidth` 2220 against `outerWidth` 1454).

Calibration recipe:

```js
window.__cal=[]; window.__h=e=>window.__cal.push([e.clientX,e.clientY]);
document.addEventListener('mousemove', window.__h, true);
```

Hover two known tool coordinates, then read `window.__cal` and solve for the scale factor. Note that `mousemove` only fires when the pointer actually moves; hovering the same point twice yields one sample, not two.

Rules:

- Never reuse a coordinate across a re-render. A stale coordinate once triple-clicked into a tab strip and created two empty dashboard tabs.
- Re-read element positions from the DOM after every save, dialog open, or layout change.
- Re-calibrate after any window resize.

## Batching and gestures

- `browser_batch` is the right default and much faster than single calls. Coordinates inside a batch refer to the screenshot taken BEFORE the call, so never batch across a re-render.
- Hover-then-click in the same batch is often required; a lone click may only register as a hover.
- The first click after a navigation is frequently swallowed.
- Drag-and-drop from a list into a shelf often fails, while checkbox-then-drag-the-chip works.
- For destructive or layout-changing gestures: one at a time, save, verify, then proceed. Never batch placements.
