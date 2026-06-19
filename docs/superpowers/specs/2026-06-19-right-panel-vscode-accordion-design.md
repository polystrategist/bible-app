# Right Panel — VS Code-style Resizable Accordion

**Date:** 2026-06-19
**Repo:** Desktop app (Electron + Vue) — `D:\Projects\Personal\Believers-Sword`
**Area:** `FrontEndApp/src/Views/ReadBible/RightSideBar/`

## Summary

Replace the Read Bible right sidebar's "one view at a time" icon-rail model with a
VS Code-style **resizable accordion**: views become stacked, collapsible sections.
Clicking a section's title bar expands/collapses it; several sections can be open at
once and share the panel's vertical height; a draggable divider between two open
sections reallocates space between them. The whole-panel show/hide toggle and the
panel-width resize stay exactly as they are today.

## Goals

- Each view (Bookmarks, Highlights, Clip Notes, Dictionary) is a collapsible section
  with a clickable title-bar header (chevron + uppercase name).
- Multiple sections can be open simultaneously ("open all panels").
- Open sections share the available height; a divider between two adjacent open
  sections is draggable to give one more room.
- Collapsed sections shrink to just their header.
- Expanded/collapsed state and per-section sizes persist across reloads.
- Keep the existing whole-panel show/hide (TitleBar `PanelRight` button →
  `settingStore.showRightSidebar`) and the left↔center↔right panel-width resize.

## Non-goals (YAGNI)

- Drag-to-reorder sections.
- Moving sections between the left and right sides.
- Changing the left sidebar (books/chapters navigation) — it is navigation, not
  stackable panels, and stays as-is.
- A new JS unit-test framework (none exists in the front-end today).

## Current state (before)

- `ReadBible.vue` — outer 3-pane vertical `splitpanes`: Left │ Center (ViewVerses +
  notes BottomPanel) │ Right. Right pane shown via `v-if="settingStore.showRightSidebar"`,
  clamped to `min 15 / max 30` (%), sizes persisted to SESSION. A `:key` forces remount
  on sidebar toggle.
- `RightSideBar.vue` — a 48px activity-bar icon rail (Bookmarks / Highlights / Clip
  Notes, plus Dictionary / References) on the far edge; only one primary view shows at a
  time. A separate inner horizontal `splitpanes` reveals a "bottom pane" for
  Dictionary/Reference. State lives in `useRightSideStore`
  (`showBottomPane`, `lastSelectedBottomMenu`, `rightSidePaneSplitStartUpValue`) and is
  used **only** by this component.
- `RightSideBar.ts` — `rightSideBarMenus` / `rightSideBarBottomMenu` (icons + titles).
- Bookmarks/Highlights/ClipNotes each wrap themselves in
  `components/ReadBible/RightSideBarContainer.vue`, which draws its own title header
  (`text-[11px] font-700 uppercase tracking-widest opacity-60`) + body slot.
- Dictionary/Reference render bare inside `BottomContents.vue`. Dictionary is
  self-contained (own search box → `window.browserWindow.searchDictionary` /
  `getDefinitions`); nothing external triggers it.

## Architecture (after)

Three units, each with one clear job.

### 1. `AccordionSection.vue` (new, presentational)

- **Props:** `title: string`, `expanded: boolean`.
- **Slots:** default = body content; `actions` = optional right-aligned header controls.
- **Emits:** `toggle` when the header is clicked.
- **Renders:** a fixed-height header bar (~32px) — rotating chevron + uppercase title
  (reuse today's `RightSideBarContainer` header styling) + `actions` slot — and, when
  expanded, the body slot inside a `flex-1 min-h-0 overflow` container.
- **A11y:** header is a `<button>`, `aria-expanded` reflects state, Enter/Space toggles.
- Knows nothing about sizing — height is controlled by the parent.

### 2. `RightSidePanel.vue` (rewrite of `RightSideBar.vue`)

- The orchestrator and only stateful view piece.
- Measures its own height with `useElementSize` (`@vueuse/core`).
- Iterates the section registry in order; for each, renders an `AccordionSection`
  bound to the store's expanded state and the content component for that key.
- Renders a draggable divider **between adjacent open sections only**.
- Applies a computed pixel height to each section (see Sizing).
- Drag handled with pointer events; updates store sizes (and persists).
- No icon rail; no inner `splitpanes`.

### 3. `useRightSideStore.ts` (refactored)

- Holds per-section state: `{ key, expanded: boolean, size: number }` keyed by section,
  preserving registry order.
- **Actions:** `toggle(key)`, `setSize(key, px)` / `applyDragDelta(i, deltaPx)`.
- **Persistence:** SESSION, same pattern as today (new storage keys, e.g.
  `right-panel-accordion-state`). Old keys (`showRightSideBottomPane`,
  `lastSelectedBottomMenu`, `storageRightSideSplitPaneSizes`) are no longer read.
- Drops the old tab-era fields.

### Section registry (`RightSideBar.ts`, repurposed)

Ordered list of `{ key, title (i18n key), component, show? }`:

| key               | title       | component       | default expanded | show  |
|-------------------|-------------|-----------------|------------------|-------|
| `bible-bookmarks` | Bookmarks   | `Bookmarks.vue` | **true**         | true  |
| `bible-highlights`| Highlights  | `Highlights.vue`| false            | true  |
| `bible-clip-notes`| Clip Notes  | `ClipNotes.vue` | false            | true  |
| `dictionary`      | dictionary  | `Dictionary.vue`| false            | true  |
| `references`      | references  | `Reference.vue` | false            | false |

(`references` keeps today's `show: false`.)

## Sizing math

A **pure** helper keeps the layout logic testable without a DOM:

```
computeLayout(containerHeight, sections, opts) -> Map<key, pixelHeight>
  HEADER = 32         // collapsed/header height
  MIN_BODY = 64       // min body height for an open section
  collapsed -> HEADER
  open sections split (containerHeight - sum(collapsedHeaders) - dividers)
    proportional to their stored `size` weights, each >= HEADER + MIN_BODY
  if total exceeds container, shrink open sections toward their minimums in order
```

- **Drag** between open section *i* and *i+1*: transfer delta px between the two,
  clamped so neither drops below `HEADER + MIN_BODY`. Persist new sizes.
- **Re-flow** on container resize (height or width change via the panel-width splitter
  or window resize): re-run `computeLayout`; correct any stale/invalid stored sizes.
- **All collapsed:** no open sections, no dividers; header bars stack at the top, empty
  space below.
- **One open:** it fills all remaining space; no divider rendered.

## Behavior

- Click header → toggle that section; chevron rotates; heights re-flow with a short CSS
  transition.
- Persisted state (`expanded` + `size` per section) restored on load.
- New section key not in stored state → default from registry (collapsed unless noted).
- Whole-panel show/hide unchanged (TitleBar button → `settingStore.showRightSidebar`).

## Changes to existing files

- **`ReadBible.vue`** — right `<Pane>` hosts `RightSidePanel`. Optionally relax the
  right-pane clamp from `min 15 / max 30` to about `min 12 / max 45` for freer width
  resize. Outer `splitpanes` and notes pane untouched.
- **`RightSideBar.ts`** — becomes the section registry (drop icon fields).
- **`Bookmarks.vue` / `Highlights.vue` / `ClipNotes.vue`** — unwrap from
  `RightSideBarContainer`; render inner scrollable content directly (the
  `AccordionSection` supplies the header + body container).
- **`RightSideBarContainer.vue`** — delete (only those 3 referenced it).
- **`BottomContents.vue`** — delete; Dictionary/Reference rendered directly as sections.
- **`Dictionary.vue` / `Reference.vue`** — unchanged internally; rendered as section
  bodies.

## Error handling / edge cases

- Container height 0 (pre-measure on mount): defer layout until `useElementSize`
  reports a non-zero height; render headers meanwhile.
- Stored sizes that no longer fit (panel shrunk): re-normalize on the next layout pass.
- Stored state referencing a removed key: ignored.
- Section toggled off-screen short: `MIN_BODY` clamp guarantees a usable body.

## Testing & verification

No JS unit-test runner exists in the front-end, so:

- `computeLayout()` written as a pure function — verifiable by reasoning / a throwaway
  script.
- `npm run typecheck` (`vue-tsc --noEmit`) must pass.
- Manual verification in the running Electron app (`npm run dev`):
  1. Toggle each section open/closed; confirm chevron + re-flow.
  2. Open 2+ sections; drag the divider; confirm only the two neighbors resize and
     respect the min body height.
  3. Reload; confirm expanded state and sizes persist.
  4. Drag the panel-width splitter and resize the window; confirm sections re-flow.
  5. Toggle the whole panel via the TitleBar button; confirm show/hide still works.

## Rollout notes

- Per project preference, the implementer does **not** auto-commit; the user commits.
- Update `docs/desktop.md` (desktop repo) if it documents the right-sidebar structure.
