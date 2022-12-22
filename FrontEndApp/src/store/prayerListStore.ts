import { defineStore } from 'pinia';
import { ref } from 'vue';

export const usePrayerListStore = defineStore('prayerListStoreId', () => {
    const prayerList = ref<Array<any>>([]);
    const donePrayerList = ref<Array<any>>([]);

    async function savePrayerItem(
        { title, content, group }: { title: string | null; content: string; group: null | string },
        key: string | null = null
    ) {
        const findIndex = prayerList.value.findIndex((item) => item.key == key);
        const data = {
            title,
            content,
            group,
        };

        if (findIndex > -1)
            prayerList.value[findIndex] = {
                ...data,
                key,
            };
        else
            prayerList.value.push({
                ...data,
                key: Date.now() + '',
            });
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
        } catch (e) {
            console.log('removePrayerItem', e);
        }
    }

    return {
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
