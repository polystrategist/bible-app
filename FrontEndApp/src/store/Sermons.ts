import { defineStore } from 'pinia';
import { ref, onBeforeMount } from 'vue';
import { fetchSermons } from '../util/SupaBase/Tables/Sermons';

export const userSermonStore = defineStore('useSermonStore', () => {
    const sermons = ref<Array<any>>([]);

    async function getSermons(search: string = '', limit: number = 50, page: number = 1) {
        const { data, error } = await fetchSermons(search, limit, page);

        if (error) {
            throw error.message;
        }

        sermons.value = data as Array<any>;
    }

    onBeforeMount(() => {
        getSermons();
    });

    return {
        sermons,
    };
});
