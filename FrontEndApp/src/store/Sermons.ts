import { defineStore } from 'pinia';
import { computed, onBeforeMount, ref, watch } from 'vue';

type StringNumberType = string | number | null;
export type SERMON_TYPE = {
    id: string | number;
    youtube_video_id: StringNumberType;
    thumbnail: string | undefined;
    title: StringNumberType;
    created_at: StringNumberType;
    language: StringNumberType;
    description: StringNumberType;
    added_by: StringNumberType;
    is_published: boolean;
};
export const userSermonStore = defineStore('useSermonStore', () => {
    const sermons = ref<Array<SERMON_TYPE>>([]);
    const loading = ref<boolean>(false);
    const limit = ref(50);
    const page = ref(1);
    const search = ref<null | string>(null);
    const NoMoreData = ref(false);

    async function getSermons(isFresh = false) {
        if (isFresh) {
            NoMoreData.value = false;
            sermons.value = [];
            page.value = 1;
            loading.value = false;
        }

        if (loading.value == true || NoMoreData.value) return;
        loading.value = true;

        // Sermon fetching is not yet implemented in the new backend
        NoMoreData.value = true;
        loading.value = false;
    }

    watch(
        () => page.value,
        async () => {
            await getSermons();
        }
    );

    onBeforeMount(async () => {
        await getSermons();
    });

    return {
        getSermons,
        sermons,
        loading,
        hasNext: computed(() => limit.value == sermons.value.length),
        hasPrevious: computed(() => page.value > 1),
        search,
        page,
        limit
    };
});
