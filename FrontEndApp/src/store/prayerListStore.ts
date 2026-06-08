import { defineStore } from 'pinia';
import { ref, onBeforeMount } from 'vue';
import { debouncedRunSync } from '../util/Sync/sync';

export const usePrayerListStore = defineStore('prayerListStoreId', () => {
    const prayerList = ref<Array<any>>([]);
    const donePrayerList = ref<Array<any>>([]);

    /**
     * Get all the prayer List
     */
    async function getPrayerLists() {
        const lists = await window.browserWindow.getPrayerLists();
        for (const list of lists) {
            if (list.status == 'done') donePrayerList.value.push(list);
            else prayerList.value.push(list);
        }
    }

    /** Clear and re-fetch all prayer lists. Safe to call multiple times. */
    async function loadPrayerLists() {
        prayerList.value = [];
        donePrayerList.value = [];
        await getPrayerLists();
    }

    /**
     * Use This to Reset Data
     * @param status
     */
    async function resetPrayerItemList(status: 'ongoing' | 'done') {
        await window.browserWindow.resetPrayerListItems(
            JSON.stringify({
                status,
                data: status == 'ongoing' ? prayerList.value : donePrayerList.value,
            })
        );
    }

    async function deletePrayerItem(key: string | number) {
        const deleteItem = await window.browserWindow.deletePrayerListItem(key);
    }

    /**
     * Use this to save a prayer item
     * @param prayerItem
     * @param key
     */
    async function savePrayerItem(
        {
            title,
            content,
            group,
            status,
        }: { title: string | null; content: string; group: null | string; status: null | 'ongoing' | 'done' },
        key: string | null = null
    ) {
        const theKey = key ? key : Date.now() + '';
        const data = {
            title,
            content,
            group,
            status: status ? status : 'ongoing',
            key: theKey,
        };

        await window.browserWindow.savePrayerItem(JSON.stringify(data));
        // Re-fetch from the DB so a status change moves the item between the
        // ongoing/answered lists correctly (the redesigned page is a single list
        // with a Mark Answered toggle, not two draggable columns).
        await loadPrayerLists();
        debouncedRunSync();
    }

    /**
     * Flip a prayer between ongoing and answered. Persists + reloads + syncs.
     */
    async function toggleStatus(item: {
        key: string;
        title?: string | null;
        content?: string;
        group?: string | null;
        status?: string | null;
    }) {
        await savePrayerItem(
            {
                title: item.title ?? null,
                content: item.content ?? '',
                group: item.group ?? null,
                status: item.status === 'done' ? 'ongoing' : 'done',
            },
            item.key
        );
    }

    /**
     * This will remove prayer item
     * @param key this is the ID or key of the prayer item.
     */
    async function removePrayerItem(key: null | string) {
        try {
            const findIndex = prayerList.value.findIndex((item) => item.key == key);
            if (findIndex > -1) prayerList.value.splice(findIndex, 1);
            const doneIndex = donePrayerList.value.findIndex((item) => item.key == key);
            if (doneIndex > -1) donePrayerList.value.splice(doneIndex, 1);

            await deletePrayerItem(key as string);
            debouncedRunSync();
        } catch (e) {
            console.error('removePrayerItem', e);
        }
    }

    /**
     * Reorder prayer items within a status group.
     * Passes the new ordered keys to the Electron backend so it can update
     * each item's `index` field and write sync log entries.
     */
    async function reorderPrayerList(status: 'ongoing' | 'done', orderedKeys: string[]) {
        await window.browserWindow.reorderPrayerListItems(
            JSON.stringify({ status, orderedKeys })
        );
        debouncedRunSync();
    }

    onBeforeMount(async () => {
        await loadPrayerLists();
    });

    return {
        resetPrayerItemList,
        removePrayerItem,
        savePrayerItem,
        toggleStatus,
        reorderPrayerList,
        loadPrayerLists,
        prayerList,
        donePrayerList,
        setPrayerList: (data: Array<any>) => {
            prayerList.value = data;
        },
        setDonePrayerList: (data: Array<any>) => (donePrayerList.value = data),
    };
});
