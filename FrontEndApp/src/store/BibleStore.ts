import { defineStore } from 'pinia';
import { computed, onBeforeMount, ref } from 'vue';
import SESSION from '../util/session';
import { bibleBooks } from '../Views/ReadBible/books';

type BookInterface = { title: string; short_name: string; book_number: number; chapter_count: number };
const StorageKeyOfChapterSelected = 'selected-chapter-storage';

export const useBibleStore = defineStore('useBibleStore', () => {
    const selectedBook = ref<BookInterface>({
        title: 'Genesis',
        short_name: 'Gen',
        book_number: 10,
        chapter_count: 50,
    });

    const DefaultSelectedVersion = 'KJV1769+.SQLite3';
    const selectedBibleVersions = ref<Array<string>>(['KJV1769+.SQLite3']);
    const selectedBookNumber = ref<number>(10);
    const selectedChapter = ref<number>(1);
    const selectedVerse = ref<number>(1);
    const verses = ref<any>(null);

    async function getVerses() {
        const arg = {
            bible_versions: selectedBibleVersions.value,
            book_number: selectedBookNumber.value,
            selected_chapter: selectedChapter.value,
        };

        verses.value = await window.browserWindow.getVerses(JSON.stringify(arg));
    }

    function saveVersesToStorage() {
        SESSION.set(StorageKeyOfChapterSelected, {
            book_number: selectedBookNumber.value,
            chapter: selectedChapter.value,
        });

        SESSION.set('saved-selected-book', selectedBook.value);
    }

    function recallSavedChapter() {
        const chapterSaved = SESSION.get(StorageKeyOfChapterSelected);
        if (chapterSaved) {
            selectedBookNumber.value = chapterSaved.book_number;
            selectedChapter.value = chapterSaved.chapter;
        }

        const savedSelectedBook = SESSION.get('saved-selected-book');
        if (savedSelectedBook) selectedBook.value = savedSelectedBook;
    }

    onBeforeMount(() => {
        recallSavedChapter();
        getVerses();
    });

    return {
        verses,
        DefaultSelectedVersion,
        selectedBibleVersions,
        selectedBook,
        selectedBookNumber,
        selectedVerse,
        selectedChapter,
        selectBook(book: BookInterface) {
            selectedBook.value = book;
            selectedBookNumber.value = book.book_number;
            if (book.chapter_count < selectedChapter.value) selectedChapter.value = book.chapter_count;
            selectedVerse.value = 1;
            saveVersesToStorage();
            getVerses();
        },
        selectChapter(chapter: number) {
            selectedChapter.value = chapter;
            saveVersesToStorage();
            getVerses();
        },
        selectVerse(verse: number) {
            selectedVerse.value = verse;
        },
        getSelectedData: computed(() => {
            const bookChosen = bibleBooks[bibleBooks.findIndex((book) => book.book_number == selectedBookNumber.value)];
            return {
                book: bookChosen.title,
                chapter: selectedChapter,
            };
        }),
    };
});
