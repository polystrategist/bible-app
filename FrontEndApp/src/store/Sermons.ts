import { defineStore } from 'pinia';
import { ref, onBeforeMount, watch, computed } from 'vue';
import { fetchSermons } from '../util/SupaBase/Tables/Sermons';

export const userSermonStore = defineStore('useSermonStore', () => {
    const sermons = ref<Array<any>>([]);
    const loading = ref<boolean>(false);
    const limit = ref(5);
    const page = ref(1);
    const search = ref<null | string>(null);

    async function getSermons(isReplace = false) {
        loading.value = true;

        if (isReplace) page.value = 1;

        setTimeout(async () => {
            const { data, error } = await fetchSermons(search.value, limit.value, page.value);

            if (error) throw error.message;

            if (!isReplace) sermons.value = [...sermons.value, ...(data as Array<any>)];
            else sermons.value = data as Array<any>;

            loading.value = false;
        }, 1000);
    }

    watch(
        () => page.value,
        (val) => {
            getSermons();
        }
    );

    onBeforeMount(() => {
        getSermons();
    });

    return {
        getSermons,
        sermons,
        loading,
        hasNext: computed(() => limit.value == sermons.value.length),
        hasPrevious: computed(() => page.value > 1),
        search,
        page,
        limit,
    };
});
