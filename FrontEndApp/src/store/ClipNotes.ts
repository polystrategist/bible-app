import { defineStore } from 'pinia';
import { ref, onMounted } from 'vue';

export const useClipNoteStore = defineStore('useClipNoteStore', () => {
    const clipNotes = ref<Array<any>>([]);
    const chapterClipNotes = ref({});

    const clipNotesPage = ref(1);
    const clipNotesSearch = ref<null | string>(null);
    const clipNotesLimit = ref(20);

    async function getClipNotes(
        args: { page: number; search: string | null; limit: number } = {
            page: clipNotesPage.value,
            search: clipNotesSearch.value,
            limit: clipNotesLimit.value,
        }
    ) {
        clipNotes.value = await window.browserWindow.getClipNotes(JSON.stringify(args));
    }

    async function getChapterClipNotes(book_number: number, chapter: number) {
        chapterClipNotes.value = await window.browserWindow.getChapterClipNotes(JSON.stringify({ book_number, chapter }));
    }

    async function storeClipNote(args: { book_number: number; chapter: number; verse: number; content: string; color: string }) {
        const stored = await window.browserWindow.storeClipNote(JSON.stringify(args));
        await getClipNotes();
        return stored;
    }

    async function deleteClipNote(args: { book_number: number; chapter: number, verse: number }) {
        const isDeleted = await window.browserWindow.deleteChapterClipNotes(JSON.stringify(args));
        await getClipNotes();
        return isDeleted;
    }

    onMounted(async () => {
        await getClipNotes();
    });

    return {
        deleteClipNote,
        chapterClipNotes,
        getChapterClipNotes,
        getClipNotes,
        clipNotes,
        storeClipNote,
        clipNotesPage,
        clipNotesLimit,
        clipNotesSearch,
    };
});
