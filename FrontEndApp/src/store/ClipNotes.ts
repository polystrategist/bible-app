import { defineStore } from 'pinia';
import { ref, onMounted } from 'vue';

export const useClipNoteStore = defineStore('useClipNoteStore', () => {
    const clipNotes = ref([]);
    const chapterClipNotes = ref({});

    async function getClipNotes(
        args: { page: number; search: string | null; limit: number } = { page: 1, search: null, limit: 30 }
    ) {
        clipNotes.value = await window.browserWindow.getClipNotes(JSON.stringify(args));
    }

    async function getChapterClipNotes(book_number: number, chapter: number) {
        chapterClipNotes.value = await window.browserWindow.getChapterClipNotes(JSON.stringify({ book_number, chapter }));
    }

    async function storeClipNote(args: { book_number: number; chapter: number; verse: number; content: string; color: string }) {
        const stored = await window.browserWindow.storeClipNote(JSON.stringify(args));
        console.log(stored);
        return stored;
    }

    onMounted(() => {
        getClipNotes();
    });

    return {
        chapterClipNotes,
        getChapterClipNotes,
        getClipNotes,
        clipNotes,
        storeClipNote,
    };
});
