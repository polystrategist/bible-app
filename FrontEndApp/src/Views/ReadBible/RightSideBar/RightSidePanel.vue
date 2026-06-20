<script setup lang="ts">
import { computed, onBeforeMount, ref, shallowRef } from 'vue';
import { useElementSize } from '@vueuse/core';
import { useMessage } from 'naive-ui';
import { visibleRightPanelSections } from './sections';
import AccordionSection from './AccordionSection.vue';
import useRightSidePanelStore from '../../../store/useRightSidePanelStore';
import { computeLayout, MIN_OPEN_HEIGHT, type PanelSectionState } from './panelLayout';

const store = useRightSidePanelStore();
const sections = visibleRightPanelSections();

// shallowRef (not ref): avoids a vue-tsc overload error with useElementSize; a DOM ref needs no deep reactivity.
const containerRef = shallowRef<HTMLElement | null>(null);
const { height: containerHeight } = useElementSize(containerRef);

const sectionStates = computed<PanelSectionState[]>(() =>
    sections.map((s) => ({
        key: s.key,
        expanded: store.isExpanded(s.key),
        size: store.sizeOf(s.key),
    }))
);

// Floor the measured height: useElementSize reports fractional, slightly
// jittery values (zoom / fractional DPI). Without flooring, those sub-pixel
// fluctuations recompute section heights every frame and the height transition
// animates each one — which shows up as a constant "wiggle" in the bottom bars.
const heights = computed(() => computeLayout(Math.floor(containerHeight.value), sectionStates.value));

function hasDividerAfter(index: number): boolean {
    return (
        index < sections.length - 1 &&
        store.isExpanded(sections[index].key) &&
        store.isExpanded(sections[index + 1].key)
    );
}

// ----- divider drag -----
// While dragging, section height transitions are turned off so the divider
// tracks the pointer instantly; toggles still animate.
const dragging = ref(false);

// Animate section heights ONLY for the duration of a toggle. Otherwise idle
// re-measures (the panel height jittering across a pixel boundary) would be
// animated by the height transition and show up as a constant wiggle.
const animatingToggle = ref(false);
let toggleTimer: ReturnType<typeof setTimeout> | undefined;
function toggleSection(key: string) {
    animatingToggle.value = true;
    store.toggle(key);
    clearTimeout(toggleTimer);
    toggleTimer = setTimeout(() => {
        animatingToggle.value = false;
    }, 260);
}

let dragKeyA = '';
let dragKeyB = '';
let startY = 0;
let startA = 0;
let startB = 0;

function onDividerDown(e: PointerEvent, index: number) {
    // Idempotent: clear any stale listeners if a prior drag didn't end cleanly.
    onDividerUp();
    dragging.value = true;
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
    dragging.value = false;
    window.removeEventListener('pointermove', onDividerMove);
    window.removeEventListener('pointerup', onDividerUp);
}

onBeforeMount(() => {
    // Preserve prior behavior: some child views read window.message.
    window.message = useMessage();
});
</script>

<template>
    <!-- No background here: the parent .read-bible-right-panel Pane owns the
         (themed) background, so the accordion sections sit on one continuous
         surface that matches the title bar across all themes. -->
    <div
        ref="containerRef"
        class="h-full w-full flex flex-col overflow-hidden"
    >
        <template v-for="(section, index) in sections" :key="section.key">
            <AccordionSection
                :title="$t(section.title)"
                :icon="section.icon"
                :expanded="store.isExpanded(section.key)"
                :animate="animatingToggle && !dragging"
                class="flex-shrink-0"
                :style="{ height: heights[section.key] + 'px' }"
                @toggle="toggleSection(section.key)"
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
