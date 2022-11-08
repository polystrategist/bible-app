<script setup lang="ts">
import { bibleBooks } from './../books';
import { useSelectionStore } from './../../../store/selections';
const selectionStore = useSelectionStore();
</script>
<template>
    <div class="h-full pr-5px">
        <div class="pl-30px py-20px pr-10px h-full overflow-x-auto overflowing-div">
            <div
                v-for="(book, i) in bibleBooks"
                :key="book"
                class="px-10px py-5px hover:bg-[var(--primary-color)] hover:text-dark-900 cursor-pointer rounded-md"
                @click="selectionStore.selectedBook = i + 1"
            >
                {{ book }}
            </div>
        </div>
    </div>
</template>
