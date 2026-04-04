<script lang="ts" setup>
import { NIcon, NLayoutHeader, NButton } from 'naive-ui';
import {
    PanelBottom20Filled,
    PanelBottom20Regular,
    PanelLeft20Filled,
    PanelLeft20Regular,
    PanelRight20Filled,
    PanelRight20Regular,
    Square20Regular,
    SquareMultiple20Regular,
    Subtract20Regular,
} from '@vicons/fluent';
import { Close, Information } from '@vicons/carbon';
import { onBeforeMount, ref } from 'vue';
import { useThemeStore } from '../../store/theme';
import { useMainStore } from '../../store/main';
import SearchBar from '../SearchBar.vue';
import LogoComponent from './../LogoComponent.vue';
// import ProfileDropdown from './Partials/ProfileDropdown.vue';
import ThemeChangerDrawer from '../ThemeChanger/ThemeChangerDrawer.vue';
import { useMenuStore } from '../../store/menu';
import { useSettingStore } from '../../store/settingStore';
import useNoteStore from '../../store/useNoteStore';
import ProfileDropdown from './Partials/ProfileDropdown.vue';

const isMaximized = ref(false);
const themeStore = useThemeStore();
const mainStore = useMainStore();
const menuStore = useMenuStore();
const isElectron = window.isElectron;
const settingStore = useSettingStore();
const noteStore = useNoteStore();

async function minimizeWindow() {
    await window.browserWindow.minimizeWindow();
}

async function maximizeWindow() {
    await window.browserWindow.maximizeWindow();
    isMaximized.value = !isMaximized.value;
}

async function closeWindow() {
    await window.browserWindow.closeWindow();
}

onBeforeMount(async () => {
    if (window.isElectron)
        isMaximized.value = await window.browserWindow.isWindowBrowserMaximized();
});
</script>
<template>
    <NLayoutHeader
        bordered
        class="flex cursor-default select-none items-center pl-13px justify-between"
    >
        <div class="whitespace-nowrap flex items-center gap-2 pl-0px">
            <LogoComponent class="w-32px h-32px" />
            <div class="mr-10px font-semibold">{{ $t('Believers Sword') }}</div>
            <div class="flex items-center gap-1">
            <template v-if="menuStore.menuSelected === 'read-bible'">
                <NButton
                    size="medium"
                    :type="settingStore.showLeftSidebar ? 'primary' : 'default'"
                    :secondary="settingStore.showLeftSidebar"
                    :quaternary="!settingStore.showLeftSidebar"
                    :focusable="false"
                    class="ml-4px"
                    :title="$t('Toggle left sidebar')"
                    @click="settingStore.showLeftSidebar = !settingStore.showLeftSidebar"
                >
                    <NIcon size="20">
                        <PanelLeft20Filled v-if="settingStore.showLeftSidebar" />
                        <PanelLeft20Regular v-else />
                    </NIcon>
                </NButton>
                <NButton
                    size="medium"
                    :type="settingStore.showRightSidebar ? 'primary' : 'default'"
                    :secondary="settingStore.showRightSidebar"
                    :quaternary="!settingStore.showRightSidebar"
                    :focusable="false"
                    class="ml-4px"
                    :title="$t('Toggle right sidebar')"
                    @click="settingStore.showRightSidebar = !settingStore.showRightSidebar"
                >
                    <NIcon size="20">
                        <PanelRight20Filled v-if="settingStore.showRightSidebar" />
                        <PanelRight20Regular v-else />
                    </NIcon>
                </NButton>
                <NButton
                    size="medium"
                    :type="noteStore.showNote ? 'primary' : 'default'"
                    :secondary="noteStore.showNote"
                    :quaternary="!noteStore.showNote"
                    :focusable="false"
                    class="ml-4px"
                    :title="$t('Toggle notes panel')"
                    @click="noteStore.showNote = !noteStore.showNote"
                >
                    <NIcon size="20">
                        <PanelBottom20Filled v-if="noteStore.showNote" />
                        <PanelBottom20Regular v-else />
                    </NIcon>
                </NButton>
            </template>
            </div>
        </div>
        <div class="flex items-center w-full h-full z-50 justify-between">
            <div class="draggable-region flex-grow cursor-move opacity-0">draggable region</div>
            <SearchBar />
            <div class="draggable-region flex-grow cursor-move opacity-0">draggable region</div>
        </div>
        <div class="flex items-center h-full justify-end pr-6px">
            <NButton round size="small" quaternary @click="mainStore.showAbout = true" title="About">
                <NIcon size="20">
                    <Information />
                </NIcon>
            </NButton>
            <ThemeChangerDrawer />
            <ProfileDropdown v-if="false" />
            <NButton
                v-show="isElectron"
                size="small"
                quaternary
                :title="$t('minimize')"
                @click="minimizeWindow()"
                class="ml-5"
            >
                <NIcon size="20">
                    <Subtract20Regular />
                </NIcon>
            </NButton>
            <NButton
                v-show="isElectron"
                size="small"
                quaternary
                :title="$t('maximize')"
                @click="maximizeWindow()"
            >
                <NIcon size="18">
                    <SquareMultiple20Regular v-if="isMaximized" />
                    <Square20Regular v-else />
                </NIcon>
            </NButton>
            <NButton
                size="small"
                quaternary
                v-show="isElectron"
                :title="$t('close')"
                @click="closeWindow()"
                class="!hover:bg-red-5"
            >
                <NIcon size="22">
                    <Close />
                </NIcon>
            </NButton>
        </div>
    </NLayoutHeader>
</template>
<style lang="scss">
.draggable-region {
    -webkit-app-region: drag;
    cursor: move;
}
</style>
