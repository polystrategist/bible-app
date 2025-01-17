<script setup lang="ts">
import { NIcon, NPopover } from 'naive-ui';
import { onClickOutside } from '@vueuse/core';
import { ref } from 'vue';
import { ContextMenuOptions } from './ContextMenuOptions';
import { useBookmarkStore } from '../../../../store/bookmark';

const contextMenuRef = ref(null);
const emits = defineEmits(['close', 'create-clip-note']);
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
        bookmarkStore.bookmarks = await window.browserWindow.saveBookMark(JSON.stringify(props.data));
    } else if (key == 'create-clip-note') {
        emits('create-clip-note', props.data);
    } else if (key == 'clear-highlight') {
        console.log(props.data)
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
        <div ref="contextMenuRef" class="w-200px max-h-200px overflow-y-auto overflowing-div flex flex-col select-none p-5px">
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
        </div>
    </NPopover>
</template>
