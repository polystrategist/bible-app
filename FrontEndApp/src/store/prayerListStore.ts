import { defineStore } from 'pinia';
import { ref, onBeforeMount } from 'vue';

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
        const findIndex = prayerList.value.findIndex((item) => item.key == key);
        const data = {
            title,
            content,
            group,
            status: status ? status : 'ongoing',
            key: theKey,
        };

        const saveData = await window.browserWindow.savePrayerItem(JSON.stringify(data));
        if (findIndex > -1) prayerList.value[findIndex] = data;
        else {
            if (data.status != 'done') prayerList.value.push(data);
        }
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
            if (doneIndex > -1) donePrayerList.value.splice(findIndex, 1);

            await deletePrayerItem(key as string);
        } catch (e) {
            console.log('removePrayerItem', e);
        }
    }

    onBeforeMount(async () => {
        await getPrayerLists();
    });

    return {
        resetPrayerItemList,
        removePrayerItem,
        savePrayerItem,
        prayerList,
        donePrayerList,
        setPrayerList: (data: Array<any>) => {
            prayerList.value = data;
        },
        setDonePrayerList: (data: Array<any>) => (donePrayerList.value = data),
    };
});
