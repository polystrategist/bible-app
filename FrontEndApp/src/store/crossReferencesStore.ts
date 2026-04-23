import { defineStore } from 'pinia';
import { ref } from 'vue';

export type CrossReference = {
    to_book: number;
    to_chapter: number;
    to_verse_start: number;
    to_verse_end: number;
    votes: number;
};

export const useCrossReferencesStore = defineStore('crossReferences', () => {
    const references = ref<CrossReference[]>([]);
    const isLoading = ref(false);
    const currentKey = ref('');

    async function fetchReferences(book_number: number, chapter: number, verse: number) {
        const key = `${book_number}_${chapter}_${verse}`;
        if (currentKey.value === key) return;
        currentKey.value = key;
        isLoading.value = true;
        try {
            references.value = await window.browserWindow.getCrossReferences({ book_number, chapter, verse });
        } finally {
            isLoading.value = false;
        }
    }

    function clear() {
        references.value = [];
        currentKey.value = '';
    }

    return { references, isLoading, fetchReferences, clear };
});
