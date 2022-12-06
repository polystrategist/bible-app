<script setup lang="ts">
import { NPopover, NButton, NIcon } from 'naive-ui';
import { onClickOutside } from '@vueuse/core';
import { ref } from 'vue';
import { BookmarkAdd } from '@vicons/carbon';
import { ContextMenuOptions } from './ContextMenuOptions';
import { useBookmarkStore } from './../../../../store/bookmark';

const contextMenuRef = ref(null);
const emits = defineEmits(['close']);
const bookmarkStore = useBookmarkStore();
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
});
async function clickContextMenu(key: string) {
    if (key == 'add-to-bookmark') {
        const saveToBookmark = await window.browserWindow.saveBookMark(JSON.stringify(props.data));
        bookmarkStore.bookmarks = saveToBookmark;
    }
    emits('close');
}
onClickOutside(contextMenuRef, (event) => emits('close'));
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
        <div ref="contextMenuRef" class="w-200px max-h-200px overflow-y-auto overflowing-div flex flex-col select-none">
            <div
                v-for="option in ContextMenuOptions"
                class="flex items-center p-7px cursor-pointer hover:bg-[var(--primary-color)] hover:text-dark-500"
                @click="clickContextMenu(option.key)"
            >
                <div class="w-30px">
                    <NIcon size="20" :component="option.icon" />
                </div>
                <span class="text-size-17px">{{ option.label }}</span>
            </div>
        </div>
    </NPopover>
</template>
