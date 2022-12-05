import { session } from 'electron';
import { defineStore } from 'pinia';
import { computed, onBeforeMount, onMounted, ref, watch } from 'vue';
import { setScrollTopState } from '../util/AutoScroll';
import SESSION from '../util/session';
import { bibleBooks } from '../Views/ReadBible/books';

type BookInterface = { title: string; short_name: string; book_number: number; chapter_count: number };
const StorageKeyOfChapterVerseSelected = 'selected-chapter-verse-storage';
const StorageSelectedVersions = 'stored-selected-versions';

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

    watch(
        () => selectedBibleVersions.value,
        (newData) => {
            SESSION.set(StorageSelectedVersions, newData);
        }
    );

    async function getVerses() {
        const arg = {
            bible_versions: selectedBibleVersions.value,
            book_number: selectedBookNumber.value,
            selected_chapter: selectedChapter.value,
        };

        verses.value = await window.browserWindow.getVerses(JSON.stringify(arg));
    }

    function saveVersesToStorage() {
        SESSION.set(StorageKeyOfChapterVerseSelected, {
            book_number: selectedBookNumber.value,
            chapter: selectedChapter.value,
            verse: selectedVerse.value,
        });

        SESSION.set('saved-selected-book', selectedBook.value);
    }

    function recallSavedChapter() {
        const chapterSaved = SESSION.get(StorageKeyOfChapterVerseSelected);
        if (chapterSaved) {
            selectedBookNumber.value = chapterSaved.book_number;
            selectedChapter.value = chapterSaved.chapter;
            selectedVerse.value = chapterSaved.verse;
        }

        const savedSelectedBook = SESSION.get('saved-selected-book');
        if (savedSelectedBook) selectedBook.value = savedSelectedBook;
    }

    function AutoScrollSavedPosition(millisecond = 300) {
        setTimeout(() => {
            setScrollTopState('view-chapter-container', 'the-selected-chapter-element', 10);
            setScrollTopState('view-books-container', 'the-selected-book-element', 10);
            setScrollTopState('view-verses-container', 'the-selected-verse', 50);
        }, millisecond);
    }

    onBeforeMount(() => {
        const selectedVersions = SESSION.get(StorageSelectedVersions);
        if (selectedVersions) selectedBibleVersions.value = selectedVersions;
        recallSavedChapter();
        getVerses();
    });

    onMounted(() => {
        AutoScrollSavedPosition();
    });

    return {
        AutoScrollSavedPosition,
        verses,
        DefaultSelectedVersion,
        selectedBibleVersions,
        selectedBook,
        selectedBookNumber,
        selectedVerse,
        selectedChapter,
        getVerses,
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
        selectVerse(book_number: number, chapter: number, verse: number) {
            selectedBookNumber.value = book_number;
            selectedChapter.value = chapter;
            selectedVerse.value = verse;
            saveVersesToStorage();
            getVerses();
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
