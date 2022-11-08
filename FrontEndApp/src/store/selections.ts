import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSelectionStore = defineStore('useSelectionStore', () => {
    const selectedBook = ref<null | number>(null);
    const selectedChapter = ref<null | number>(null);
    const selectedVerse = ref<null | number>(null);

    return {
        selectedBook,
        selectedVerse,
        selectedChapter,
    };
});
