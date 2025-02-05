<script lang="ts" setup>
import { NIcon, NTooltip, useMessage } from 'naive-ui';
import { onBeforeMount, ref } from 'vue';
import { rightSideBarBottomMenu, rightSideBarMenus } from './RightSideBar';
import BibleList from './Bibles/Bibles.vue';
import Bookmarks from './Bookmarks/Bookmarks.vue';
import Highlights from './Highlights/Highlights.vue';
import SESSION from '../../../util/session';
import ClipNotes from './ClipNotes/ClipNotes.vue';
import { useThemeStore } from '../../../store/theme';
import { Pane, Splitpanes } from 'splitpanes';
import useRightSideStore from '../../../store/useRightSideStore';
import BottomContents from './BottomContents/BottomContents.vue';

const themeStore = useThemeStore();
const SavedRightSideBar = 'saved-right-side-bar-menu-key';
const selectedButton = ref<string>('bible-search');
const rightSideStore = useRightSideStore();

function selectRightSideBarMenu(key: string) {
    selectedButton.value = key;
    SESSION.set(SavedRightSideBar, key);
}

function selectRightSideBarBottomMenu(key: string) {
    if (rightSideStore.lastSelectedBottomMenu == key) {
        rightSideStore.lastSelectedBottomMenu = null;
        rightSideStore.showBottomPane = false;
        return;
    }

    rightSideStore.lastSelectedBottomMenu = key;
    rightSideStore.showBottomPane = true;
}

onBeforeMount(() => {
    const saveMenuKey = SESSION.get(SavedRightSideBar);
    if (saveMenuKey) selectedButton.value = saveMenuKey;
    else selectRightSideBarMenu('bible-bookmarks');

    window.message = useMessage();
});
</script>
<template>
    <div class="h-full w-full flex">
        <Splitpanes
            @resized="rightSideStore.resizingPaneRightSide"
            horizontal
            class="splitpanes_show_bar w-[calc(100%-40px)] h-full"
            :class="{ 'splitter-hidden': !rightSideStore.showBottomPane }"
        >
            <Pane
                :min-size="rightSideStore.showBottomPane ? 30 : 100"
                :size="
                    rightSideStore.showBottomPane
                        ? rightSideStore.rightSidePaneSplitStartUpValue[0].size
                        : 100
                "
            >
                <div class="h-full p-2">
                    <BibleList v-show="selectedButton == 'bible-lists'" />
                    <Bookmarks v-show="selectedButton == 'bible-bookmarks'" />
                    <Highlights v-show="selectedButton == 'bible-highlights'" />
                    <ClipNotes v-show="selectedButton == 'bible-clip-notes'" />
                </div>
            </Pane>
            <Pane
                :size="
                    rightSideStore.showBottomPane
                        ? rightSideStore.rightSidePaneSplitStartUpValue[1].size
                        : 0
                "
                :min-size="rightSideStore.rightSidePaneSplitStartUpValue[1].min"
                :max-size="rightSideStore.rightSidePaneSplitStartUpValue[1].max"
            >
                <div class="p2 h-full">
                    <BottomContents :selected-menu-key="rightSideStore.lastSelectedBottomMenu" />
                </div>
            </Pane>
        </Splitpanes>
        <div
            class="w-40px min-w-40px bg-gray-100 dark:bg-dark-800 pt-3 text-size-20px flex flex-col justify-between items-center pb-3"
        >
            <div class="flex flex-col items-center gap-1">
                <NTooltip v-for="menu in rightSideBarMenus" :placement="'left'">
                    <template #trigger>
                        <div
                            :key="menu.key"
                            :class="{
                                'bg-[var(--primary-color)] !text-black !hover:bg-[var(--primary-color)] !hover:text-black':
                                    selectedButton == menu.key,
                            }"
                            class="w-27px hover:bg-[var(--primary-color-light)] dark:hover:bg-[var(--primary-color-light)] dark:hover:bg-opacity-25 hover:bg-opacity-20 flex items-center justify-center py-1 rounded-md cursor-pointer"
                            @click="selectRightSideBarMenu(menu.key)"
                        >
                            <NIcon :component="themeStore.isDark ? menu.iconDark : menu.icon" />
                        </div>
                    </template>
                    <span class="capitalize select-none">{{ $t(menu.title) }}</span>
                </NTooltip>
            </div>
            <div>
                <template v-for="menu in rightSideBarBottomMenu">
                    <NTooltip
                        v-if="typeof menu.show === 'undefined' && !menu.show"
                        :placement="'left'"
                    >
                        <template #trigger>
                            <div
                                :key="menu.key"
                                :class="{
                                    'bg-[var(--primary-color)] !text-black !hover:bg-[var(--primary-color)] !hover:text-black':
                                        rightSideStore.lastSelectedBottomMenu == menu.key,
                                }"
                                class="w-27px hover:bg-[var(--primary-color-light)] dark:hover:bg-[var(--primary-color-light)] dark:hover:bg-opacity-25 hover:bg-opacity-20 flex items-center justify-center py-1 rounded-md cursor-pointer"
                                @click="selectRightSideBarBottomMenu(menu.key)"
                            >
                                <NIcon :component="themeStore.isDark ? menu.iconDark : menu.icon" />
                            </div>
                        </template>
                        <span class="capitalize select-none">{{ $t(menu.title) }}</span>
                    </NTooltip>
                </template>
            </div>
        </div>
    </div>
</template>
