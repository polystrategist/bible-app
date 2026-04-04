import { defineStore } from 'pinia';
import { ref } from 'vue';

// Study space feature has been removed.
// This store is kept as a minimal stub so existing imports don't break.

export type SPACE_STUDY_SCHEMA = {
    id: number | string | 0;
    title: string;
    description: string;
    created_at?: string;
    updated_at?: string;
};

export default defineStore('useSpaceStudyStore', () => {
    const showSpaceStudy = ref(false);
    const lists = ref<Array<SPACE_STUDY_SCHEMA>>([]);
    const selectedSpaceStudy = ref<SPACE_STUDY_SCHEMA | null>(null);

    return {
        showSpaceStudy,
        lists,
        selectedSpaceStudy,
    };
});
