<script setup lang="ts">
import { useBibleStore } from '../../../store/BibleStore';
import { useSettingStore } from '../../../store/settingStore';
import { bibleBooks } from '../../../util/books';
import { NButton } from 'naive-ui';
const selectionStore = useBibleStore();
const settings = useSettingStore();
</script>
<template>
    <div class="h-full pr-5px flex select-none">
        <div id="view-books-container" class="pl-20px pr-5px py-4 overflow-x-auto overflowing-div w-full flex flex-col">
            <template v-for="(book, i) in bibleBooks" :key="book.book_number">
                <NButton
                    v-show="book.deuterocanonical === false || (book.deuterocanonical && settings.showDeuterocanonical)"
                    class="justify-start" :quaternary="selectionStore.selectedBookNumber != book.book_number"
                    :secondary="selectionStore.selectedBookNumber == book.book_number"
                    :type="selectionStore.selectedBookNumber == book.book_number ? 'primary' : 'default'"
                    :id="book.book_number == selectionStore.selectedBookNumber ? 'the-selected-book-element' : ''"
                    @click="selectionStore.selectBook(book)">
                    {{ $t(book.title) }}
                </NButton>
            </template>
        </div>
        <div id="view-chapter-container"
            class="pl-5px py-4 pr-5px overflow-x-auto overflowing-div min-w-60px text-center flex flex-col">
            <NButton
                v-for="chapter in settings.showDeuterocanonical ? selectionStore.selectedBook.deuterocanonical_chapter_count ?? selectionStore.selectedBook.chapter_count : selectionStore.selectedBook.chapter_count"
                :key="chapter" :quaternary="selectionStore.selectedChapter != chapter"
                :secondary="selectionStore.selectedChapter == chapter"
                :type="selectionStore.selectedChapter == chapter ? 'primary' : 'default'"
                :id="chapter == selectionStore.selectedChapter ? 'the-selected-chapter-element' : ''"
                @click="selectionStore.selectChapter(chapter)">
                {{ chapter }}
            </NButton>
        </div>
    </div>
</template>
