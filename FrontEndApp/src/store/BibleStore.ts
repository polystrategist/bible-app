import { useClipNoteStore } from './ClipNotes';
import { defineStore } from 'pinia';
import { computed, onBeforeMount, onMounted, ref, watch } from 'vue';
import { setScrollTopState } from '../util/AutoScroll';
import SESSION from '../util/session';
import { bibleBooks } from '../util/books';
import { useSettingStore } from './settingStore';

type BookInterface = { title: string; short_name: string; book_number: number; chapter_count: number };
const StorageKeyOfChapterVerseSelected = 'selected-chapter-verse-storage';
const StorageSelectedVersions = 'stored-selected-versions';

export const useBibleStore = defineStore('useBibleStore', () => {
    const settingStore = useSettingStore();
    const selectedBook = ref<BookInterface>({
        title: 'Genesis',
        short_name: 'Gen',
        book_number: 10,
        chapter_count: 50,
    });
    const clipNoteStore = useClipNoteStore();
    const DefaultSelectedVersion = `King James Version - 1769.SQLite3`;
    const selectedBibleVersions = ref<Array<string>>([`King James Version - 1769.SQLite3`]);
    const selectedBookNumber = ref<number>(10);
    const selectedChapter = ref<number>(1);
    const selectedVerse = ref<number>(1);
    const verses = ref<Array<any>>([]);
    const chapterHighlights = ref<Array<any>>([]);
    const allHighlights = ref<Array<any>>([]);
    const highlightPage = ref(1);
    const highlightSearch = ref<string | null>(null);
    const highlightLimit = ref<number>(50);
    const renderVerses = computed(() => {
        return verses.value.map((v) => {
            const theVersions = v.version.map((ver: any) => {
                const key = `${ver.version.replace('.SQLite3', '')}_${v.book_number}_${v.chapter}_${v.verse}`;
                const highlight = (chapterHighlights.value as any)[key];
                return {
                    text: highlight ? highlight.content : ver.text,
                    version: ver.version,
                    key,
                };
            });

            return {
                book_number: v.book_number,
                chapter: v.chapter,
                verse: v.verse,
                version: theVersions,
            };
        });
    });

    watch(
        () => selectedBibleVersions.value,
        (newData) => {
            SESSION.set(StorageSelectedVersions, newData);
        }
    );

    async function getHighlights(
        args: { page: number; search: string | null; limit: number } = {
            page: highlightPage.value,
            search: highlightSearch.value,
            limit: highlightLimit.value,
        }
    ) {
        allHighlights.value = await window.browserWindow.getHighlights(JSON.stringify(args));
    }

    async function getChapterHighlights() {
        const args = {
            book_number: selectedBookNumber.value,
            chapter: selectedChapter.value,
        };
        chapterHighlights.value = await window.browserWindow.getChapterHighlights(JSON.stringify(args));
    }

    async function getVerses() {
        const arg = {
            bible_versions: selectedBibleVersions.value,
            book_number: selectedBookNumber.value,
            selected_chapter: selectedChapter.value,
        };
        await getChapterHighlights();
        await clipNoteStore.getChapterClipNotes(selectedBookNumber.value, selectedChapter.value);
        selectedBook.value = getBook(selectedBookNumber.value);
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

    function getBook(b_num: number) {
        return bibleBooks[bibleBooks.findIndex((book) => book.book_number == b_num)];
    }

    onBeforeMount(async () => {
        const selectedVersions = SESSION.get(StorageSelectedVersions);
        if (selectedVersions) selectedBibleVersions.value = selectedVersions;
        recallSavedChapter();
        await getVerses();
    });

    onMounted(async () => {
        AutoScrollSavedPosition();
        await getHighlights();
    });

    return {
        highlightLimit,
        highlightPage,
        highlightSearch,
        getHighlights,
        allHighlights,
        AutoScrollSavedPosition,
        verses,
        DefaultSelectedVersion,
        selectedBibleVersions,
        selectedBook,
        selectedBookNumber,
        selectedVerse,
        selectedChapter,
        getVerses,
        chapterHighlights,
        async selectBook(book: BookInterface) {
            selectedBook.value = book;
            selectedBookNumber.value = book.book_number;
            if (book.chapter_count < selectedChapter.value) selectedChapter.value = book.chapter_count;
            if (book.title == 'Daniel' && settingStore.showDeuterocanonical) selectedBook.value.chapter_count = 14;
            selectedVerse.value = 1;
            saveVersesToStorage();
            await getVerses();
        },
        async selectChapter(chapter: number) {
            selectedChapter.value = chapter;
            saveVersesToStorage();
            await getVerses();
        },
        async selectVerse(book_number: number, chapter: number, verse: number) {
            selectedBookNumber.value = book_number;
            selectedChapter.value = chapter;
            selectedVerse.value = verse;
            saveVersesToStorage();
            await getVerses();
        },
        getSelectedData: computed(() => {
            const bookChosen = bibleBooks[bibleBooks.findIndex((book) => book.book_number == selectedBookNumber.value)];
            return {
                book: bookChosen.title,
                chapter: selectedChapter,
            };
        }),
        getBook,
        renderVerses,
        isBookExist: (book_number: number) => {
            const findBookIndex = bibleBooks.findIndex((book) => book.book_number == book_number);
            return findBookIndex > -1;
        },
        getBookShortName: (book_number: number) => {
            return bibleBooks[bibleBooks.findIndex((book) => book.book_number == book_number)];
        },
    };
});
