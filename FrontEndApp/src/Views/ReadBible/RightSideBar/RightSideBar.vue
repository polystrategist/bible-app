<script lang="ts" setup>
import { NIcon, NTooltip, useMessage } from 'naive-ui';
import { onBeforeMount, ref } from 'vue';
import { rightSideBarBottomMenu, rightSideBarMenus } from './RightSideBar';
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
const selectedButton = ref<string>('bible-bookmarks');
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
    if (saveMenuKey && saveMenuKey !== 'bible-lists') selectedButton.value = saveMenuKey;
    else selectRightSideBarMenu('bible-bookmarks');
    window.message = useMessage();
});
</script>
<template>
    <div class="h-full w-full flex">
        <Splitpanes
            @resized="rightSideStore.resizingPaneRightSide"
            horizontal
            :dbl-click-splitter="false"
            class="splitpanes_show_bar w-[calc(100%-48px)] h-full"
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
                <div class="h-full p-2 read-bible-right-content">
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
                <div class="p-2 h-full">
                    <BottomContents :selected-menu-key="rightSideStore.lastSelectedBottomMenu" />
                </div>
            </Pane>
        </Splitpanes>

        <!-- VS Code-style activity bar -->
        <div
            class="w-48px min-w-48px bg-gray-100 dark:bg-dark-800 flex flex-col items-center justify-between py-2 read-bible-right-toolbar border-l border-gray-200 dark:border-dark-600"
        >
            <!-- Primary tabs: Bookmarks, Highlights, Clip Notes -->
            <div class="flex flex-col items-center w-full gap-1">
                <NTooltip v-for="menu in rightSideBarMenus" :key="menu.key" :placement="'left'">
                    <template #trigger>
                        <div
                            class="relative w-full h-44px flex items-center justify-center cursor-pointer transition-all duration-150 rounded-sm"
                            :class="
                                selectedButton == menu.key
                                    ? 'text-[var(--primary-color)]'
                                    : 'text-gray-400 dark:text-gray-500 hover:text-gray-700 dark:hover:text-gray-200'
                            "
                            @click="selectRightSideBarMenu(menu.key)"
                        >
                            <!-- Active accent bar on the left edge (facing the content panel) -->
                            <div
                                class="absolute left-0 top-3 bottom-3 w-[2px] rounded-r-full transition-all duration-150"
                                :class="
                                    selectedButton == menu.key
                                        ? 'bg-[var(--primary-color)]'
                                        : 'bg-transparent'
                                "
                            ></div>
                            <NIcon
                                :component="themeStore.isDark ? menu.iconDark : menu.icon"
                                size="20"
                            />
                        </div>
                    </template>
                    <span class="capitalize select-none">{{ $t(menu.title) }}</span>
                </NTooltip>
            </div>

            <!-- Separator -->
            <div class="w-6 border-t border-gray-300 dark:border-dark-500 my-1"></div>

            <!-- Utility tabs: Dictionary, References -->
            <div class="flex flex-col items-center w-full gap-1">
                <template v-for="menu in rightSideBarBottomMenu" :key="menu.key">
                    <NTooltip
                        v-if="typeof menu.show === 'undefined' || menu.show !== false"
                        :placement="'left'"
                    >
                        <template #trigger>
                            <div
                                class="relative w-full h-44px flex items-center justify-center cursor-pointer transition-all duration-150 rounded-sm"
                                :class="
                                    rightSideStore.lastSelectedBottomMenu == menu.key
                                        ? 'text-[var(--primary-color)]'
                                        : 'text-gray-400 dark:text-gray-500 hover:text-gray-700 dark:hover:text-gray-200'
                                "
                                @click="selectRightSideBarBottomMenu(menu.key)"
                            >
                                <!-- Active accent bar -->
                                <div
                                    class="absolute left-0 top-3 bottom-3 w-[2px] rounded-r-full transition-all duration-150"
                                    :class="
                                        rightSideStore.lastSelectedBottomMenu == menu.key
                                            ? 'bg-[var(--primary-color)]'
                                            : 'bg-transparent'
                                    "
                                ></div>
                                <NIcon
                                    :component="themeStore.isDark ? menu.iconDark : menu.icon"
                                    size="20"
                                />
                            </div>
                        </template>
                        <span class="capitalize select-none">{{ $t(menu.title) }}</span>
                    </NTooltip>
                </template>
            </div>
        </div>
    </div>
</template>
