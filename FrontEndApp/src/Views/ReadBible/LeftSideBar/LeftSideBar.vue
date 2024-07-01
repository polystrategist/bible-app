<script setup lang="ts">
import { useBibleStore } from '../../../store/BibleStore';
import { useSettingStore } from '../../../store/settingStore';
import { bibleBooks } from '../../../util/books';
const selectionStore = useBibleStore();
const settings = useSettingStore();
</script>
<template>
    <div class="h-full pr-5px flex select-none">
        <div id="view-books-container" class="pl-20px py-10px pr-5px h-full overflow-x-auto overflowing-div w-full">
            <template v-for="(book, i) in bibleBooks" :key="book.book_number">
                <div
                    v-show="book.deuterocanonical === false || (book.deuterocanonical && settings.showDeuterocanonical)"
                    class="px-10px py-5px hover:bg-[var(--primary-color-light)] dark:hover:bg-[var(--primary-color-light)] dark:hover:bg-opacity-25 hover:bg-opacity-20 cursor-pointer rounded-md whitespace-nowrap truncate"
                    :class="{
                        'bg-[var(--primary-color)] !hover:bg-[var(--primary-color)] text-black hover:text-black font-700':
                            selectionStore.selectedBookNumber == book.book_number,
                    }"
                    :id="book.book_number == selectionStore.selectedBookNumber ? 'the-selected-book-element' : ''"
                    @click="selectionStore.selectBook(book)"
                >
                    {{ $t(book.title) }}
                </div>
            </template>
        </div>
        <div id="view-chapter-container" class="pl-5px py-10px h-full overflow-x-auto overflowing-div min-w-60px text-center">
            <div
                v-for="chapter in selectionStore.selectedBook.chapter_count"
                :key="chapter"
                class="py-5px hover:bg-[var(--primary-color-light)] dark:hover:bg-opacity-25 hover:bg-opacity-20 cursor-pointer rounded-md flex items-center justify-center w-full max-w-40px"
                :class="{
                    'bg-[var(--primary-color)] !hover:bg-[var(--primary-color)] text-black hover:text-black font-700':
                        selectionStore.selectedChapter == chapter,
                }"
                :id="chapter == selectionStore.selectedChapter ? 'the-selected-chapter-element' : ''"
                @click="selectionStore.selectChapter(chapter)"
            >
                {{ chapter }}
            </div>
        </div>
    </div>
</template>
../../../store/books
