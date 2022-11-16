import { defineStore } from 'pinia';
import { ref } from 'vue';

type BookInterface = { title: string; short_name: string; book_number: number; chapter_count: number };

export const useSelectionStore = defineStore('useSelectionStore', () => {
    const selectedBook = ref<BookInterface>({
        title: 'Genesis',
        short_name: 'Gen',
        book_number: 10,
        chapter_count: 50,
    });

    const selectedBookNumber = ref<number>(10);
    const selectedChapter = ref<number>(1);
    const selectedVerse = ref<number>(1);

    return {
        selectedBook,
        selectedBookNumber,
        selectedVerse,
        selectedChapter,
        selectBook(book: BookInterface) {
            selectedBook.value = book;
            selectedBookNumber.value = book.book_number;
            if (book.chapter_count < selectedChapter.value) selectedChapter.value = book.chapter_count;
            selectedVerse.value = 1;
        },
        selectChapter(chapter: number) {
            selectedChapter.value = chapter;
        },
        selectVerse(verse: number) {
            selectedVerse.value = verse;
        },
    };
});
