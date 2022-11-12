<script setup lang="ts">
import { bibleBooks } from './../books';
import { useSelectionStore } from './../../../store/selections';
const selectionStore = useSelectionStore();
</script>
<template>
    <div class="h-full pr-5px flex">
        <div class="pl-20px py-10px pr-5px h-full overflow-x-auto overflowing-div w-[80%]">
            <div
                v-for="(book, i) in bibleBooks"
                :key="book"
                class="px-10px py-5px hover:bg-[var(--primary-color)] hover:text-dark-900 cursor-pointer rounded-md"
                @click="selectionStore.selectedBook = i + 1"
            >
                {{ book }}
            </div>
        </div>
        <div class="py-10px pr-10px h-full overflow-x-auto overflowing-div w-[20%]">
            <div
                v-for="(book, i) in bibleBooks"
                :key="book"
                class="px-10px py-5px w-9 hover:bg-[var(--primary-color)] hover:text-dark-900 cursor-pointer rounded-md flex items-center justify-center w-full"
                @click="selectionStore.selectedBook = i + 1"
            >
                {{ i }}
            </div>
        </div>
    </div>
</template>
