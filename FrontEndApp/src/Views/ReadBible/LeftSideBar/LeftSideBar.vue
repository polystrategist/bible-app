<script setup lang="ts">
import { bibleBooks } from './../books';
import { useBibleStore } from '../../../store/BibleStore';
const selectionStore = useBibleStore();
</script>
<template>
    <div class="h-full pr-5px flex select-none">
        <div class="pl-20px py-10px pr-5px h-full overflow-x-auto overflowing-div w-[80%]">
            <div
                v-for="(book, i) in bibleBooks"
                :key="book.book_number"
                class="px-10px py-5px hover:bg-orange-500 dark:hover:bg-[var(--primary-color-light)] dark:hover:bg-opacity-25 hover:bg-opacity-20 cursor-pointer rounded-md"
                :class="{
                    'bg-[var(--primary-color)] !hover:bg-[var(--primary-color)] text-black hover:text-black font-700':
                        selectionStore.selectedBookNumber == book.book_number,
                }"
                @click="selectionStore.selectBook(book)"
            >
                {{ book.title }}
            </div>
        </div>
        <div class="pl-5px py-10px pr-10px h-full overflow-x-auto overflowing-div w-[20%]">
            <div
                v-for="chapter in selectionStore.selectedBook.chapter_count"
                :key="chapter"
                class="px-10px py-5px w-9 hover:bg-orange-500 dark:hover:bg-[var(--primary-color-light)] dark:hover:bg-opacity-25 hover:bg-opacity-20 cursor-pointer rounded-md flex items-center justify-center w-full"
                :class="{
                    'bg-[var(--primary-color)] !hover:bg-[var(--primary-color)] text-black hover:text-black font-700':
                        selectionStore.selectedChapter == chapter,
                }"
                @click="selectionStore.selectChapter(chapter)"
            >
                {{ chapter }}
            </div>
        </div>
    </div>
</template>
