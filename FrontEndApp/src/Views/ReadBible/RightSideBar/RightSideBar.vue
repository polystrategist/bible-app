<script setup lang="ts">
import { NIcon } from 'naive-ui';
import { ref } from 'vue';
import { rightSideBarMenus } from './RightSideBar';
import BibleList from './Bibles/Bibles.vue';
import Bookmarks from './Bookmarks/Bookmarks.vue';
import Highlights from './Highlights/Highlights.vue';
import Search from './Search/Search.vue';

const selectedButton = ref<string>('bible-search');
</script>
<template>
    <div class="h-full w-full flex">
        <div class="w-full h-full p-2 overflow-auto overflowing-div">
            <BibleList v-show="selectedButton == 'bible-lists'" />
            <Bookmarks v-show="selectedButton == 'bible-bookmarks'" />
            <Highlights v-show="selectedButton == 'bible-highlights'" />
            <Search v-show="selectedButton == 'bible-search'" />
        </div>
        <div class="w-40px min-w-40px bg-gray-100 dark:bg-dark-800 flex flex-col items-center gap-1 pt-3 text-size-20px">
            <div
                v-for="menu in rightSideBarMenus"
                class="w-27px hover:bg-orange-500 dark:hover:bg-orange-300 dark:hover:bg-opacity-25 dark:hover:text-white hover:dark:text-black hover:bg-opacity-20 flex items-center justify-center py-1 rounded-md cursor-pointer"
                :class="{ 'bg-[var(--primary-color)] !text-black !hover:bg-[var(--primary-color)]': selectedButton == menu.key }"
                @click="selectedButton = menu.key"
                :key="menu.key"
            >
                <NIcon :component="menu.icon" />
            </div>
        </div>
    </div>
</template>
