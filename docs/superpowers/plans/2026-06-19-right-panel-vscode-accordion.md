# Right Panel VS Code-style Accordion — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the Read Bible right sidebar into a VS Code-style resizable accordion — stacked collapsible sections (Bookmarks, Highlights, Clip Notes, Dictionary) that you toggle by clicking their title bar, with draggable dividers between open sections.

**Architecture:** A pure sizing helper computes each section's pixel height; a Pinia store holds per-section `{expanded, size}` with persistence; a presentational `AccordionSection` renders one header+body; and `RightSidePanel` orchestrates them — measuring its height, rendering sections + dividers, and handling divider drags. Built new alongside the old files, then the old files are swapped out and deleted so typecheck stays green after every task.

**Tech Stack:** Vue 3 (`<script setup>` + TS), Pinia, `@vueuse/core` (`useElementSize`), `naive-ui`, UnoCSS/Windi classes, `@vicons/fluent`. Spec: [docs/superpowers/specs/2026-06-19-right-panel-vscode-accordion-design.md](../specs/2026-06-19-right-panel-vscode-accordion-design.md).

## Global Constraints

- **Working directory for all commands:** `D:\Projects\Personal\Believers-Sword\FrontEndApp`.
- **No JS unit-test runner exists** in the front-end (`package.json` scripts are `dev`, `build`, `typecheck`, `preview`). Adding one is a non-goal. The per-task test cycle is therefore: **`npm run typecheck` (`vue-tsc --noEmit`) must pass with no errors**, plus the worked-example reasoning / manual app checks each task specifies. Do not introduce vitest/jest.
- **Do NOT run `git commit` or `git push`.** Per project preference the user commits manually. Each task ends after its verification step — stop there.
- **Keep typecheck green after every task.** New files are added before old ones are removed.
- **i18n:** section titles pass through `$t(...)`. The keys `Bookmarks`, `Highlights`, `Clip Notes`, `dictionary`, `references` already exist (used by the current code).
- **Left sidebar (books/chapters) is out of scope** — do not touch `LeftSideBar.vue` or its pane.
- **Naming (exact, used across tasks):**
  - Layout helper: `computeLayout(containerHeight: number, sections: PanelSectionState[]): Record<string, number>`; constants `HEADER_HEIGHT=32`, `DIVIDER_HEIGHT=4`, `MIN_BODY_HEIGHT=64`, `MIN_OPEN_HEIGHT=96`; type `PanelSectionState = { key: string; expanded: boolean; size: number }`. File: `src/Views/ReadBible/RightSideBar/panelLayout.ts`.
  - Registry: `rightPanelSections: RightPanelSection[]`, `visibleRightPanelSections(): RightPanelSection[]`, type `RightPanelSection = { key: string; title: string; component: Component; defaultExpanded: boolean; defaultSize: number; show: boolean }`. File: `src/Views/ReadBible/RightSideBar/sections.ts`.
  - Store: default export `useRightSidePanelStore` (pinia id `'useRightSidePanelStore'`) exposing `states`, `isExpanded(key)`, `sizeOf(key)`, `toggle(key)`, `commitSizes(pxByKey: Record<string, number>)`. File: `src/store/useRightSidePanelStore.ts`.
  - Components: `AccordionSection.vue`, `RightSidePanel.vue` in `src/Views/ReadBible/RightSideBar/`.

---

## File Structure

**Create:**
- `src/Views/ReadBible/RightSideBar/panelLayout.ts` — pure sizing helper + constants + `PanelSectionState`.
- `src/Views/ReadBible/RightSideBar/sections.ts` — section registry.
- `src/store/useRightSidePanelStore.ts` — per-section state + persistence.
- `src/Views/ReadBible/RightSideBar/AccordionSection.vue` — one collapsible section (presentational).
- `src/Views/ReadBible/RightSideBar/RightSidePanel.vue` — orchestrator.

**Modify:**
- `src/Views/ReadBible/ReadBible.vue` — render `RightSidePanel`; (optional) relax right-pane clamp.
- `src/Views/ReadBible/RightSideBar/Bookmarks/Bookmarks.vue` — unwrap from `RightSideBarContainer`.
- `src/Views/ReadBible/RightSideBar/Highlights/Highlights.vue` — unwrap.
- `src/Views/ReadBible/RightSideBar/ClipNotes/ClipNotes.vue` — unwrap.

**Delete (after swap):**
- `src/Views/ReadBible/RightSideBar/RightSideBar.vue`
- `src/Views/ReadBible/RightSideBar/RightSideBar.ts`
- `src/Views/ReadBible/RightSideBar/BottomContents/BottomContents.vue`
- `src/store/useRightSideStore.ts`
- `src/components/ReadBible/RightSideBarContainer.vue`

---

### Task 1: Pure sizing helper (`panelLayout.ts`)

**Files:**
- Create: `src/Views/ReadBible/RightSideBar/panelLayout.ts`

**Interfaces:**
- Produces: `PanelSectionState`, `computeLayout(containerHeight, sections)`, and constants `HEADER_HEIGHT`, `DIVIDER_HEIGHT`, `MIN_BODY_HEIGHT`, `MIN_OPEN_HEIGHT`. Consumed by Task 5.
- Consumes: nothing.

- [ ] **Step 1: Write the helper**

Create `src/Views/ReadBible/RightSideBar/panelLayout.ts`:

```ts
export interface PanelSectionState {
    key: string;
    expanded: boolean;
    /** px-scaled weight; relative size used to split height among open sections */
    size: number;
}

export const HEADER_HEIGHT = 32; // collapsed section / header bar height (px)
export const DIVIDER_HEIGHT = 4; // draggable divider between two open sections (px)
export const MIN_BODY_HEIGHT = 64; // minimum body height for an open section (px)
export const MIN_OPEN_HEIGHT = HEADER_HEIGHT + MIN_BODY_HEIGHT; // 96

/** Number of places where two consecutive sections in the stack are both open. */
function countOpenAdjacencies(sections: PanelSectionState[]): number {
    let count = 0;
    for (let i = 1; i < sections.length; i++) {
        if (sections[i].expanded && sections[i - 1].expanded) count++;
    }
    return count;
}

/**
 * Compute the pixel height for every section.
 * - Collapsed sections take exactly HEADER_HEIGHT.
 * - Open sections split the remaining height proportional to their `size`
 *   weights, each at least MIN_OPEN_HEIGHT. Open heights always sum to the
 *   available space when there is room above the per-section minimum.
 * Pure — no DOM — so it can be reasoned about directly.
 */
export function computeLayout(
    containerHeight: number,
    sections: PanelSectionState[]
): Record<string, number> {
    const result: Record<string, number> = {};
    const open = sections.filter((s) => s.expanded);

    for (const s of sections) {
        if (!s.expanded) result[s.key] = HEADER_HEIGHT;
    }
    if (open.length === 0) return result;

    const collapsedCount = sections.length - open.length;
    const reserved =
        collapsedCount * HEADER_HEIGHT + countOpenAdjacencies(sections) * DIVIDER_HEIGHT;
    const minTotal = open.length * MIN_OPEN_HEIGHT;
    const available = Math.max(minTotal, containerHeight - reserved);
    const extra = available - minTotal; // >= 0
    const totalWeight = open.reduce((sum, s) => sum + Math.max(s.size, 1), 0);

    let used = 0;
    open.forEach((s, i) => {
        if (i === open.length - 1) {
            result[s.key] = available - used; // remainder → exact fit
        } else {
            const share = Math.round((Math.max(s.size, 1) / totalWeight) * extra);
            result[s.key] = MIN_OPEN_HEIGHT + share;
            used += result[s.key];
        }
    });
    return result;
}
```

- [ ] **Step 2: Verify the worked examples by tracing the code**

Confirm each by hand (these are the contract):
- `computeLayout(500, [])` → `{}`.
- One collapsed only: `computeLayout(500, [{key:'a',expanded:false,size:200}])` → `{a:32}`.
- One open: `computeLayout(500, [{key:'a',expanded:true,size:200}])` → open=1, reserved=0, minTotal=96, available=500, last section → `available - used(0)` = **`{a:500}`**.
- Two open equal weights: `computeLayout(500, [{key:'a',expanded:true,size:100},{key:'b',expanded:true,size:100}])` → reserved = 1 adjacency × 4 = 4; minTotal=192; available=496; extra=304; a (not last): 96 + round(0.5×304)=96+152=248; b (last): 496−248=**248**. Sum 496 = available. ✓
- Open + collapsed: `computeLayout(500, [{key:'a',expanded:true,size:100},{key:'b',expanded:false,size:100},{key:'c',expanded:true,size:100}])` → b=32; adjacencies=0 (b between them is collapsed) so reserved = 1×32 = 32; minTotal=192; available=468; extra=276; a: 96+round(0.5×276)=96+138=234; c (last): 468−234=**234**. ✓
- Cramped: `computeLayout(100, [{key:'a',expanded:true,size:100},{key:'b',expanded:true,size:100}])` → minTotal=192 > (100−4); available=max(192, 96)=192; extra=0; a=96, b=192−96=**96** (overflow scrolls inside each body). ✓

- [ ] **Step 3: Typecheck**

Run: `npm run typecheck`
Expected: no errors.

- [ ] **Step 4: Stop (do not commit — user commits manually).**

---

### Task 2: Section registry (`sections.ts`)

**Files:**
- Create: `src/Views/ReadBible/RightSideBar/sections.ts`

**Interfaces:**
- Consumes: the existing view components `Bookmarks.vue`, `Highlights.vue`, `ClipNotes.vue`, `Dictionary.vue`, `Reference.vue`.
- Produces: `RightPanelSection`, `rightPanelSections`, `visibleRightPanelSections()`. Consumed by Tasks 3 and 5.

- [ ] **Step 1: Write the registry**

Create `src/Views/ReadBible/RightSideBar/sections.ts`:

```ts
import type { Component } from 'vue';
import Bookmarks from './Bookmarks/Bookmarks.vue';
import Highlights from './Highlights/Highlights.vue';
import ClipNotes from './ClipNotes/ClipNotes.vue';
import Dictionary from './BottomContents/Dictionary/Dictionary.vue';
import Reference from './BottomContents/Reference/Reference.vue';

export interface RightPanelSection {
    key: string;
    title: string; // i18n key
    component: Component;
    defaultExpanded: boolean;
    defaultSize: number;
    show: boolean;
}

export const rightPanelSections: RightPanelSection[] = [
    { key: 'bible-bookmarks', title: 'Bookmarks', component: Bookmarks, defaultExpanded: true, defaultSize: 200, show: true },
    { key: 'bible-highlights', title: 'Highlights', component: Highlights, defaultExpanded: false, defaultSize: 200, show: true },
    { key: 'bible-clip-notes', title: 'Clip Notes', component: ClipNotes, defaultExpanded: false, defaultSize: 200, show: true },
    { key: 'dictionary', title: 'dictionary', component: Dictionary, defaultExpanded: false, defaultSize: 200, show: true },
    { key: 'references', title: 'references', component: Reference, defaultExpanded: false, defaultSize: 200, show: false },
];

export const visibleRightPanelSections = (): RightPanelSection[] =>
    rightPanelSections.filter((s) => s.show);
```

- [ ] **Step 2: Typecheck**

Run: `npm run typecheck`
Expected: no errors (all five `.vue` imports resolve — paths verified against the repo).

- [ ] **Step 3: Stop (do not commit).**

---

### Task 3: Per-section store (`useRightSidePanelStore.ts`)

**Files:**
- Create: `src/store/useRightSidePanelStore.ts`

**Interfaces:**
- Consumes: `rightPanelSections` (Task 2), `SESSION` (`../util/session`).
- Produces: default export `useRightSidePanelStore` with `states`, `isExpanded(key)`, `sizeOf(key)`, `toggle(key)`, `commitSizes(pxByKey)`. Consumed by Task 5.

- [ ] **Step 1: Write the store**

Create `src/store/useRightSidePanelStore.ts`:

```ts
import { defineStore } from 'pinia';
import { onBeforeMount, ref, watch } from 'vue';
import SESSION from '../util/session';
import { rightPanelSections } from '../Views/ReadBible/RightSideBar/sections';

interface SectionState {
    expanded: boolean;
    size: number; // px-scaled weight
}

const STORAGE_KEY = 'right-panel-accordion-state-v1';

function buildDefaults(): Record<string, SectionState> {
    const out: Record<string, SectionState> = {};
    for (const s of rightPanelSections) {
        out[s.key] = { expanded: s.defaultExpanded, size: s.defaultSize };
    }
    return out;
}

export default defineStore('useRightSidePanelStore', () => {
    const states = ref<Record<string, SectionState>>(buildDefaults());

    function ensureKey(key: string) {
        if (!states.value[key]) {
            const def = rightPanelSections.find((s) => s.key === key);
            states.value[key] = {
                expanded: def?.defaultExpanded ?? false,
                size: def?.defaultSize ?? 1,
            };
        }
    }

    function isExpanded(key: string): boolean {
        return states.value[key]?.expanded ?? false;
    }

    function sizeOf(key: string): number {
        return states.value[key]?.size ?? 1;
    }

    function toggle(key: string) {
        ensureKey(key);
        states.value[key].expanded = !states.value[key].expanded;
    }

    /** Re-base the given open sections' weights to their current pixel heights. */
    function commitSizes(pxByKey: Record<string, number>) {
        for (const [key, px] of Object.entries(pxByKey)) {
            ensureKey(key);
            states.value[key].size = px;
        }
    }

    onBeforeMount(() => {
        const saved = SESSION.get(STORAGE_KEY) as Record<string, SectionState> | null;
        if (saved && typeof saved === 'object') {
            for (const s of rightPanelSections) {
                const v = saved[s.key];
                if (v && typeof v.expanded === 'boolean' && typeof v.size === 'number') {
                    states.value[s.key] = { expanded: v.expanded, size: v.size };
                }
            }
        }
    });

    watch(states, (val) => SESSION.set(STORAGE_KEY, val), { deep: true });

    return { states, isExpanded, sizeOf, toggle, commitSizes };
});
```

Note: `onBeforeMount` inside a `defineStore` setup mirrors the existing `useRightSideStore.ts` pattern — keep it consistent.

- [ ] **Step 2: Typecheck**

Run: `npm run typecheck`
Expected: no errors.

- [ ] **Step 3: Stop (do not commit).**

---

### Task 4: Presentational section (`AccordionSection.vue`)

**Files:**
- Create: `src/Views/ReadBible/RightSideBar/AccordionSection.vue`

**Interfaces:**
- Consumes: `naive-ui` `NIcon`, `@vicons/fluent` `ChevronRight24Regular`.
- Produces: a component with props `{ title: string; expanded: boolean }`, emit `toggle`, default slot (body) and `actions` slot. Consumed by Task 5.

- [ ] **Step 1: Write the component**

Create `src/Views/ReadBible/RightSideBar/AccordionSection.vue`:

```vue
<script setup lang="ts">
import { NIcon } from 'naive-ui';
import { ChevronRight24Regular } from '@vicons/fluent';

defineProps<{
    title: string;
    expanded: boolean;
}>();

const emit = defineEmits<{ (e: 'toggle'): void }>();
</script>

<template>
    <div class="flex flex-col min-h-0 overflow-hidden">
        <button
            type="button"
            class="h-8 min-h-8 w-full select-none flex items-center gap-1 px-2 border-b border-gray-200 dark:border-dark-600 hover:bg-gray-200/60 dark:hover:bg-dark-700 transition-colors"
            :aria-expanded="expanded"
            @click="emit('toggle')"
        >
            <NIcon
                size="14"
                class="transition-transform duration-150 opacity-60"
                :class="expanded ? 'rotate-90' : ''"
            >
                <ChevronRight24Regular />
            </NIcon>
            <span class="text-[11px] font-700 uppercase tracking-widest opacity-60">
                {{ title }}
            </span>
            <span class="ml-auto flex items-center" @click.stop>
                <slot name="actions" />
            </span>
        </button>
        <div v-show="expanded" class="flex-1 min-h-0 overflow-hidden">
            <slot />
        </div>
    </div>
</template>
```

- [ ] **Step 2: Typecheck**

Run: `npm run typecheck`
Expected: no errors (confirms `ChevronRight24Regular` resolves).

- [ ] **Step 3: Stop (do not commit).**

---

### Task 5: Orchestrator (`RightSidePanel.vue`)

**Files:**
- Create: `src/Views/ReadBible/RightSideBar/RightSidePanel.vue`

**Interfaces:**
- Consumes: `visibleRightPanelSections` (Task 2), `useRightSidePanelStore` (Task 3), `computeLayout`/`MIN_OPEN_HEIGHT`/`PanelSectionState` (Task 1), `AccordionSection` (Task 4), `@vueuse/core` `useElementSize`.
- Produces: the `RightSidePanel` component. Consumed by Task 6.

- [ ] **Step 1: Write the component**

Create `src/Views/ReadBible/RightSideBar/RightSidePanel.vue`:

```vue
<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue';
import { useElementSize } from '@vueuse/core';
import { useMessage } from 'naive-ui';
import { visibleRightPanelSections } from './sections';
import AccordionSection from './AccordionSection.vue';
import useRightSidePanelStore from '../../../store/useRightSidePanelStore';
import { computeLayout, MIN_OPEN_HEIGHT, type PanelSectionState } from './panelLayout';

const store = useRightSidePanelStore();
const sections = visibleRightPanelSections();

const containerRef = ref<HTMLElement | null>(null);
const { height: containerHeight } = useElementSize(containerRef);

const sectionStates = computed<PanelSectionState[]>(() =>
    sections.map((s) => ({
        key: s.key,
        expanded: store.isExpanded(s.key),
        size: store.sizeOf(s.key),
    }))
);

const heights = computed(() => computeLayout(containerHeight.value, sectionStates.value));

function hasDividerAfter(index: number): boolean {
    return (
        index < sections.length - 1 &&
        store.isExpanded(sections[index].key) &&
        store.isExpanded(sections[index + 1].key)
    );
}

// ----- divider drag -----
let dragKeyA = '';
let dragKeyB = '';
let startY = 0;
let startA = 0;
let startB = 0;

function onDividerDown(e: PointerEvent, index: number) {
    dragKeyA = sections[index].key;
    dragKeyB = sections[index + 1].key;
    startY = e.clientY;
    const h = heights.value;
    startA = h[dragKeyA];
    startB = h[dragKeyB];
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
    window.addEventListener('pointermove', onDividerMove);
    window.addEventListener('pointerup', onDividerUp);
}

function onDividerMove(e: PointerEvent) {
    const delta = e.clientY - startY;
    const sum = startA + startB;
    const newA = Math.min(Math.max(startA + delta, MIN_OPEN_HEIGHT), sum - MIN_OPEN_HEIGHT);
    const newB = sum - newA;
    // Re-base ALL open sections to px so weights stay in consistent units.
    const current = heights.value;
    const pxByKey: Record<string, number> = {};
    for (const s of sections) {
        if (store.isExpanded(s.key)) pxByKey[s.key] = current[s.key];
    }
    pxByKey[dragKeyA] = newA;
    pxByKey[dragKeyB] = newB;
    store.commitSizes(pxByKey);
}

function onDividerUp() {
    window.removeEventListener('pointermove', onDividerMove);
    window.removeEventListener('pointerup', onDividerUp);
}

onBeforeMount(() => {
    // Preserve prior behavior: some child views read window.message.
    window.message = useMessage();
});
</script>

<template>
    <div
        ref="containerRef"
        class="h-full w-full flex flex-col overflow-hidden bg-gray-100 dark:bg-dark-600"
    >
        <template v-for="(section, index) in sections" :key="section.key">
            <AccordionSection
                :title="$t(section.title)"
                :expanded="store.isExpanded(section.key)"
                class="flex-shrink-0"
                :style="{ height: heights[section.key] + 'px' }"
                @toggle="store.toggle(section.key)"
            >
                <component :is="section.component" />
            </AccordionSection>
            <div
                v-if="hasDividerAfter(index)"
                class="h-1 min-h-1 flex-shrink-0 cursor-row-resize bg-transparent hover:bg-[var(--primary-color)] transition-colors"
                @pointerdown="onDividerDown($event, index)"
            ></div>
        </template>
    </div>
</template>
```

- [ ] **Step 2: Typecheck**

Run: `npm run typecheck`
Expected: no errors.

- [ ] **Step 3: Stop (do not commit).** Not yet wired into the layout, so no visible change.

---

### Task 6: Wire into layout & remove old panel

**Files:**
- Modify: `src/Views/ReadBible/ReadBible.vue`
- Delete: `src/Views/ReadBible/RightSideBar/RightSideBar.vue`, `src/Views/ReadBible/RightSideBar/RightSideBar.ts`, `src/Views/ReadBible/RightSideBar/BottomContents/BottomContents.vue`, `src/store/useRightSideStore.ts`

**Interfaces:**
- Consumes: `RightSidePanel` (Task 5).
- Produces: the live accordion panel inside the Read Bible layout.

- [ ] **Step 1: Swap the import in `ReadBible.vue`**

In `src/Views/ReadBible/ReadBible.vue`, change:

```ts
import RightSideBar from './RightSideBar/RightSideBar.vue';
```
to:
```ts
import RightSidePanel from './RightSideBar/RightSidePanel.vue';
```

- [ ] **Step 2: Swap the usage in the template**

In `src/Views/ReadBible/ReadBible.vue`, change:

```vue
            <RightSideBar />
```
to:
```vue
            <RightSidePanel />
```

- [ ] **Step 3: (Optional) Relax the right-pane width clamp**

In `src/Views/ReadBible/ReadBible.vue`, change the third entry of the `splitPaneSizes` ref from:

```ts
    { min: 15, max: 30, size: 25 },
```
to:
```ts
    { min: 12, max: 45, size: 25 },
```

(Existing users keep their persisted sizes until they next drag; this only changes fresh defaults. Skip this step if you prefer to leave the width behavior exactly as-is.)

- [ ] **Step 4: Delete the now-unused old files**

```bash
rm "src/Views/ReadBible/RightSideBar/RightSideBar.vue"
rm "src/Views/ReadBible/RightSideBar/RightSideBar.ts"
rm "src/Views/ReadBible/RightSideBar/BottomContents/BottomContents.vue"
rm "src/store/useRightSideStore.ts"
```

- [ ] **Step 5: Confirm nothing else references the deleted files**

Run a search for stragglers:
```bash
grep -rn "RightSideBar\.vue\|RightSideBar'\|RightSideBar\"\|useRightSideStore\|BottomContents" src
```
Expected: no matches except inside `sections.ts` (which references the `BottomContents/Dictionary` and `BottomContents/Reference` **subfolders**, not `BottomContents.vue`). If anything else appears, fix that import before continuing.

- [ ] **Step 6: Typecheck**

Run: `npm run typecheck`
Expected: no errors.

- [ ] **Step 7: Manual smoke test**

Run: `npm run dev`, open the app, go to Read Bible.
Expected: the right panel now shows stacked section headers (Bookmarks expanded; Highlights, Clip Notes, Dictionary collapsed). Clicking a header expands/collapses it; opening two shows a draggable divider. (Headers may briefly look doubled with the inner view titles — fixed in Task 7.)

- [ ] **Step 8: Stop (do not commit).**

---

### Task 7: Unwrap view components & delete `RightSideBarContainer`

**Files:**
- Modify: `src/Views/ReadBible/RightSideBar/Bookmarks/Bookmarks.vue`
- Modify: `src/Views/ReadBible/RightSideBar/Highlights/Highlights.vue`
- Modify: `src/Views/ReadBible/RightSideBar/ClipNotes/ClipNotes.vue`
- Delete: `src/components/ReadBible/RightSideBarContainer.vue`

**Interfaces:**
- Consumes: nothing new.
- Produces: each view renders only its content (the `AccordionSection` header is now the single title).

- [ ] **Step 1: Unwrap `Bookmarks.vue`**

In `src/Views/ReadBible/RightSideBar/Bookmarks/Bookmarks.vue`, remove the import line:
```ts
import RightSideBarContainer from './../../../../components/ReadBible/RightSideBarContainer.vue';
```
Then replace the `<template>` so the outer `<RightSideBarContainer :title="$t('Bookmarks')">` wrapper is gone and its inner `<div>` becomes the root:

```vue
<template>
    <div class="h-full overflow-auto overflowing-div scroll-hover-only">
        <div
            v-for="(bookmark, key) in (bookmarkStore.bookmarks as bookmarksType)"
            :key="key"
            class="relative cursor-pointer flex justify-between items-center transition-colors duration-100"
            :class="{
                'dark:bg-light-50 dark:bg-opacity-10 bg-gray-800 bg-opacity-10': selectedBookmarkKey == key,
                'dark:hover:bg-light-50 dark:hover:bg-opacity-10 hover:bg-gray-800 hover:bg-opacity-10': selectedBookmarkKey != key,
            }"
        >
            <div
                class="absolute left-0 top-0 bottom-0 w-[2px] bg-[var(--primary-color)] transition-opacity duration-150"
                :class="selectedBookmarkKey == key ? 'opacity-100' : 'opacity-0'"
            ></div>
            <div class="w-full px-3 py-2" @click="selectBookVerse(key as string, bookmark)">
                <span class="font-600 text-sm mr-1">{{ $t(bibleStore.getBook(bookmark.book_number).title) }}</span>
                <span class="opacity-60 text-sm">{{ bookmark.chapter }}:{{ bookmark.verse }}</span>
            </div>
            <div
                class="pr-3 text-gray-400 hover:text-red-500 dark:hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                @click.stop
            >
                <NPopconfirm @positive-click="deleteBookmark(bookmark)">
                    <template #trigger>
                        <NIcon size="16" class="cursor-pointer opacity-40 hover:opacity-100">
                            <TrashCan />
                        </NIcon>
                    </template>
                    {{ $t('Are You sure?') }}
                </NPopconfirm>
            </div>
        </div>
    </div>
</template>
```

- [ ] **Step 2: Unwrap `Highlights.vue`**

In `src/Views/ReadBible/RightSideBar/Highlights/Highlights.vue`, remove the import line:
```ts
import RightSideBarContainer from '../../../../components/ReadBible/RightSideBarContainer.vue';
```
Then change the template so the outer `<RightSideBarContainer :title="$t('Highlights')">` wrapper is removed and the existing `<div v-bind="containerProps" ...>` becomes the root element (keep everything inside it byte-for-byte). Concretely, replace:
```vue
    <RightSideBarContainer :title="$t('Highlights')">
        <div v-bind="containerProps" class="h-full overflowing-div scroll-hover-only">
```
with:
```vue
    <div v-bind="containerProps" class="h-full overflowing-div scroll-hover-only">
```
and remove the matching closing `</RightSideBarContainer>` (the last line before `</template>`), leaving the `</div>` that closes the `containerProps` div as the template root.

- [ ] **Step 3: Unwrap `ClipNotes.vue`**

In `src/Views/ReadBible/RightSideBar/ClipNotes/ClipNotes.vue`, remove the import line:
```ts
import RightSideBarContainer from '../../../../components/ReadBible/RightSideBarContainer.vue';
```
Then replace:
```vue
    <RightSideBarContainer :title="$t('Clip Notes')">
        <div v-bind="containerProps" class="h-full overflowing-div scroll-hover-only the-clip-notes-side-bar">
```
with:
```vue
    <div v-bind="containerProps" class="h-full overflowing-div scroll-hover-only the-clip-notes-side-bar">
```
and remove the matching closing `</RightSideBarContainer>` before `</template>`, leaving the `containerProps` div's `</div>` as the root. (Leave the `<style>` block untouched.)

- [ ] **Step 4: Delete `RightSideBarContainer.vue`**

```bash
rm "src/components/ReadBible/RightSideBarContainer.vue"
```

- [ ] **Step 5: Confirm no remaining references**

Run:
```bash
grep -rn "RightSideBarContainer" src
```
Expected: no matches.

- [ ] **Step 6: Typecheck**

Run: `npm run typecheck`
Expected: no errors.

- [ ] **Step 7: Full manual verification** (`npm run dev`, Read Bible page)

1. Each section shows a single title bar (no doubled headers); chevron points right when collapsed, down (rotated 90°) when open.
2. Click each header → it expands/collapses; Bookmarks/Highlights/Clip Notes lists and the Dictionary search all render and scroll.
3. Open two adjacent sections → a divider appears between them; drag it → only those two resize, neither shrinks below a usable minimum; other open sections are unaffected.
4. Reload the app → expanded state and dragged sizes persist.
5. Drag the left↔center↔right width splitter and resize the window → sections re-flow to fill the height.
6. Click the TitleBar right-panel toggle → the whole panel hides/shows as before.

- [ ] **Step 8: Stop (do not commit — tell the user the work is ready for them to review and commit).**

---

## Self-Review

**Spec coverage:**
- Collapsible sections with title-bar header → Task 4 (`AccordionSection`) + Task 5 (render). ✓
- Multiple open at once / "open all panels" → store per-section `expanded` (Task 3) + layout (Task 1). ✓
- Open sections share height; draggable divider between two open → Task 1 (`computeLayout`) + Task 5 (divider drag). ✓
- Collapse-to-header → `HEADER_HEIGHT` branch in `computeLayout` (Task 1). ✓
- Persisted expanded state + sizes → Task 3 (`STORAGE_KEY`, watch/load). ✓
- Keep whole-panel show/hide + width resize → untouched in `ReadBible.vue`/TitleBar; Task 6 only swaps the child + optional clamp. ✓
- Section registry (Bookmarks/Highlights/Clip Notes/Dictionary; references hidden) → Task 2. ✓
- Unwrap views; delete `RightSideBarContainer` + `BottomContents` + old `RightSideBar` + old store → Tasks 6 & 7. ✓
- Left sidebar untouched → enforced in Global Constraints. ✓
- Testing = typecheck + manual (no runner) → reflected in every task. ✓

**Placeholder scan:** No TBD/TODO; every code step shows complete content. ✓

**Type consistency:** `computeLayout`, `PanelSectionState`, `MIN_OPEN_HEIGHT`, `isExpanded`/`sizeOf`/`toggle`/`commitSizes`, `visibleRightPanelSections`, `rightPanelSections` are named identically across Tasks 1–6. ✓
