<script setup lang="ts">
import { onMounted, ref, warn, watch } from 'vue';
import Editor from '../../../components/Editor/Editor.vue';
import useNoteStore from '../../../store/useNoteStore';

const noteStore = useNoteStore();

onMounted(() => {
    document.addEventListener('keydown', function (event) {
        // Check if 'Ctrl+S' or 'Cmd+S' is pressed
        if ((event.ctrlKey || event.metaKey) && event.key === 's') {
            console.log('asdfasdf');
        }
    });
});
</script>
<template>
    <div class="p-10px h-[calc(100%-20px)] relative">
        <div class="absolute bottom-2 right-1 bg-white bg-opacity-5 px-6px py-2px rounded-md">
            <span
                class="flex flex-wrap items-center gap-x-1 text-sm text-gray-600 dark:text-neutral-400"
            >
                <kbd
                    class="min-h-[18px] inline-flex justify-center items-center px-1 bg-gray-200 border border-transparent font-mono text-xs text-gray-800 rounded-md dark:bg-neutral-700 dark:text-neutral-200"
                >
                    ctrl
                </kbd>
                +
                <kbd
                    class="min-h-[18px] inline-flex justify-center items-center px-1 bg-gray-200 border border-transparent font-mono text-xs text-gray-800 rounded-md dark:bg-neutral-700 dark:text-neutral-200"
                >
                    S
                </kbd>
                To Save
            </span>
        </div>
        <Editor v-model="noteStore.note" overflow />
    </div>
</template>
