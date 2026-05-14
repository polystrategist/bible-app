<script setup lang="ts">
import { NIcon, NPopover } from 'naive-ui';
import { onClickOutside } from '@vueuse/core';
import { ref, type PropType } from 'vue';
import { ContextMenuOptions } from './ContextMenuOptions';
import { useBookmarkStore } from '../../../../store/bookmark';
import { useBibleStore } from '../../../../store/BibleStore';
import { debouncedRunSync } from '../../../../util/Sync/sync';
import { colors } from '../../../../util/highlighter';

const bibleStore = useBibleStore();
const contextMenuRef = ref(null);
const emits = defineEmits(['close', 'create-clip-note']);
const bookmarkStore = useBookmarkStore();
const showColorPicker = ref(false);

const props = defineProps({
    showContextMenu: {
        type: Boolean,
        default: false,
    },
    x: {
        type: Number,
        default: 0,
    },
    y: {
        type: Number,
        default: 0,
    },
    data: {
        type: Object,
        default: {},
    },
    selectedVersesData: {
        type: Array as PropType<any[]>,
        default: () => [],
    },
});

async function highlightVerse(color: string) {
    const verses = props.selectedVersesData.length > 0 ? props.selectedVersesData : [props.data];
    for (const verseData of verses) {
        const { book_number, chapter, verse } = verseData;
        const key = `${book_number}_${chapter}_${verse}`;
        await window.browserWindow.saveHighlight(
            JSON.stringify({ key, book_number, chapter, verse, content: color }),
        );
    }
    await bibleStore.getChapterHighlights();
    debouncedRunSync();
    showColorPicker.value = false;
    emits('close');
}

async function clickContextMenu(key: string) {
    if (key == 'add-to-bookmark') {
        const verses = props.selectedVersesData.length > 0 ? props.selectedVersesData : [props.data];
        for (const verseData of verses) {
            bookmarkStore.bookmarks = await window.browserWindow.saveBookMark(
                JSON.stringify(verseData),
            );
        }
        debouncedRunSync();
    } else if (key == 'create-clip-note') {
        emits('create-clip-note', props.data);
    } else if (key == 'highlight-verse') {
        showColorPicker.value = !showColorPicker.value;
        return; // Don't close menu
    } else if (key == 'compare-verse') {
        (window as any).browserWindow.openCompareVerseWindow({
            book_number: props.data.book_number,
            chapter: props.data.chapter,
            verse: props.data.verse,
            book_name: bibleStore.selectedBook.title,
        });
    } else if (key == 'clear-highlight') {
        const verses = props.selectedVersesData.length > 0 ? props.selectedVersesData : [props.data];
        for (const verseData of verses) {
            const verseKey = `${verseData.book_number}_${verseData.chapter}_${verseData.verse}`;
            await bibleStore.removeHighlightInDb(verseKey);
            await bibleStore.removeHighlightInDb(verseData.key);
        }
    }
    showColorPicker.value = false;
    emits('close');
}
onClickOutside(contextMenuRef, (event) => {
    showColorPicker.value = false;
    emits('close');
});
</script>
<template>
    <NPopover
        :show="showContextMenu"
        :x="x"
        :y="y"
        trigger="manual"
        content-style="padding: 0 !important;"
        class="!p-0 !rounded-md"
    >
        <div
            ref="contextMenuRef"
            class="w-200px max-h-250px overflow-y-auto overflowing-div flex flex-col select-none p-5px"
        >
            <div
                v-for="option in ContextMenuOptions"
                class="flex items-center pt-4px pb-2px pl-7px pr-1 cursor-pointer hover:bg-[var(--primary-color)] hover:text-dark-500 rounded-sm"
                @click="clickContextMenu(option.key)"
            >
                <div class="w-25px">
                    <NIcon size="15" :component="option.icon" />
                </div>
                <span class="text-size-15px whitespace-nowrap">{{ $t(option.label) }}</span>
            </div>
            <!-- Color picker for highlight -->
            <div v-if="showColorPicker" class="flex flex-wrap gap-5px px-7px py-6px border-t border-gray-500 border-opacity-30 mt-4px">
                <button
                    v-for="c in colors"
                    :key="c.color"
                    :style="`background: ${c.color}`"
                    class="h-24px w-24px rounded-full cursor-pointer border-2 border-transparent hover:border-white transition-all hover:scale-110"
                    :title="c.name"
                    @click="highlightVerse(c.color)"
                ></button>
            </div>
        </div>
    </NPopover>
</template>
