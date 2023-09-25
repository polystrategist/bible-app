import { defineStore } from 'pinia';
import { computed, onBeforeMount, ref } from 'vue';
import { getDownloadedBible } from '../util/Modules/Controller/FeBibleController';
import SESSION from '../util/session';
import { bibleBooks } from '../util/books';

type BookInterface = { title: string; short_name: string; book_number: number; chapter_count: number };
const StorageKeyOfChapterSelected = 'selected-chapter-storage';

export const useModuleStore = defineStore('useModuleStore', () => {
    const bibleLists = ref<Array<any>>([]);

    async function getBibleLists() {
        bibleLists.value = await getDownloadedBible();
    }

    onBeforeMount(() => {
        getBibleLists();
    });

    return {
        bibleLists,
        getBibleLists,
    };
});
