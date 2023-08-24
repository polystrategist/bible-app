<script lang='ts' setup>
import { NIcon, NTooltip, useMessage } from 'naive-ui';
import { onBeforeMount, ref } from 'vue';
import { rightSideBarMenus } from './RightSideBar';
import BibleList from './Bibles/Bibles.vue';
import Bookmarks from './Bookmarks/Bookmarks.vue';
import Highlights from './Highlights/Highlights.vue';
import SESSION from '../../../util/session';
import ClipNotes from './ClipNotes/ClipNotes.vue';

const SavedRightSideBar = 'saved-right-side-bar-menu-key';
const selectedButton = ref<string>('bible-search');

function selectRightSideBarMenu(key: string) {
    selectedButton.value = key;
    SESSION.set(SavedRightSideBar, key);
}

onBeforeMount(() => {
    const saveMenuKey = SESSION.get(SavedRightSideBar);
    if (saveMenuKey) selectedButton.value = saveMenuKey;
    else selectRightSideBarMenu('bible-bookmarks');

    window.message = useMessage();
});
</script>
<template>
    <div class='h-full w-full flex'>
        <div class='w-[calc(100%-40px)] h-full p-2'>
            <BibleList v-show="selectedButton == 'bible-lists'" />
            <Bookmarks v-show="selectedButton == 'bible-bookmarks'" />
            <Highlights v-show="selectedButton == 'bible-highlights'" />
            <ClipNotes v-show="selectedButton == 'bible-clip-notes'" />
        </div>
        <div
            class='w-40px min-w-40px bg-gray-100 dark:bg-dark-800 flex flex-col items-center gap-1 pt-3 text-size-20px'>
            <NTooltip v-for='menu in rightSideBarMenus' :placement="'left'">
                <template #trigger>
                    <div
                        :key='menu.key'
                        :class="{
                            'bg-[var(--primary-color)] !text-black !hover:bg-[var(--primary-color)] !hover:text-black':
                                selectedButton == menu.key,
                        }"
                        class='w-27px hover:bg-[var(--primary-color-light)] dark:hover:bg-[var(--primary-color-light)] dark:hover:bg-opacity-25 hover:bg-opacity-20 flex items-center justify-center py-1 rounded-md cursor-pointer'
                        @click='selectRightSideBarMenu(menu.key)'
                    >
                        <NIcon :component='menu.icon' />
                    </div>
                </template>
                <span class='capitalize'>{{ $t(menu.title) }}</span>
            </NTooltip>
        </div>
    </div>
</template>
