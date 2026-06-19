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
