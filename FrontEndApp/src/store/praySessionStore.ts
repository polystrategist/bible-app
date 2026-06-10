import { defineStore } from 'pinia';
import { ref } from 'vue';

/** A prayer being prayed through in a focus session. */
export interface SessionPrayer {
    key: string;
    title?: string | null;
    content?: string;
    group?: string | null;
    created_at?: string;
}

/**
 * Controls the full-screen "Start Pray" overlay. The overlay is mounted once and
 * teleported to <body>, so it covers the whole app (no sidebar/menu) regardless
 * of the routed view. `open()` seeds the ongoing prayers + a start index.
 */
export const usePraySessionStore = defineStore('praySessionStoreId', () => {
    const visible = ref(false);
    const prayers = ref<SessionPrayer[]>([]);
    const startIndex = ref(0);

    function open(list: SessionPrayer[], index = 0) {
        if (!list.length) return;
        prayers.value = list;
        startIndex.value = Math.min(Math.max(index, 0), list.length - 1);
        visible.value = true;
    }

    function close() {
        visible.value = false;
        prayers.value = [];
        startIndex.value = 0;
    }

    return { visible, prayers, startIndex, open, close };
});
