import { defineStore } from 'pinia';
import { computed, onBeforeMount, ref, watch } from 'vue';
import { fetchSermons } from '../util/SupaBase/Tables/Sermons';

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

        const { data, error } = await fetchSermons(search.value, limit.value, page.value);

        if (error) {
            alert('Their  is a problem getting the data, because of poor connection or no internet connection');
            loading.value = false;
            return;
        }

        if (!data.length) {
            NoMoreData.value = true;
            loading.value = false;
            return;
        }

        if (!isFresh) sermons.value = [...sermons.value, ...(data as Array<any>)];
        else sermons.value = data as Array<any>;
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
