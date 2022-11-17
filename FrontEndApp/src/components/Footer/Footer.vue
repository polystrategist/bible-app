<script setup lang="ts">
import { NLayoutFooter } from 'naive-ui';
import { computed } from 'vue';
import { useBibleStore } from '../../store/BibleStore';

const bibleStore = useBibleStore();
const selectedChapter = computed(() => bibleStore.getSelectedData);
</script>
<template>
    <NLayoutFooter bordered class="flex cursor-default select-none items-center pl-8px light:bg-gray-100">
        <div class="whitespace-nowrap flex items-center gap-1"></div>
        <div class="w-full h-full text-center z-50 font-700">{{ selectedChapter.book }} {{ selectedChapter.chapter }}</div>
        <div class="flex items-center h-full"></div>
    </NLayoutFooter>
</template>
