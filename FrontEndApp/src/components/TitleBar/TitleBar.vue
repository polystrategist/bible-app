<script lang="ts" setup>
import { NIcon, NLayoutHeader, NTooltip, NButton } from 'naive-ui';
import {
    Heart24Filled,
    Square20Regular,
    SquareMultiple20Regular,
    Subtract20Regular,
    WeatherMoon20Regular,
    WeatherSunny20Regular,
} from '@vicons/fluent';
import { Close, Information } from '@vicons/carbon';
import { onBeforeMount, ref } from 'vue';
import { useThemeStore } from '../../store/theme';
import { useMainStore } from '../../store/main';
import SearchBar from '../SearchBar.vue';
import LogoComponent from './../LogoComponent.vue';
import ProfileDropdown from './Partials/ProfileDropdown.vue';
import { PaintBucket24Filled } from '@vicons/fluent';
import ThemeChangerDrawer from '../ThemeChanger/ThemeChangerDrawer.vue';

const isMaximized = ref(false);
const themeStore = useThemeStore();
const mainStore = useMainStore();
const isElectron = window.isElectron;

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

function changeTheme() {
    themeStore.isDark = !themeStore.isDark;
}

function openDonationInBrowser() {
    window.open('https://buymeacoffee.com/jenuel.dev', '_blank');
}

onBeforeMount(async () => {
    if (window.isElectron) isMaximized.value = await window.browserWindow.isWindowBrowserMaximized();
});
</script>
<template>
    <NLayoutHeader bordered class="flex cursor-default select-none items-center pl-8px justify-between">
        <div class="whitespace-nowrap flex items-center gap-1 pl-0px">
            <div class="w-20px h-20px">
                <LogoComponent />
            </div>
            {{ $t('Believers Sword') }}
        </div>
        <div class="flex items-center w-full h-full z-50 justify-between">
            <div class="draggable-region flex-grow cursor-move opacity-0">draggable region</div>
            <SearchBar />
            <div class="draggable-region flex-grow cursor-move opacity-0">draggable region</div>
        </div>
        <div class="flex items-center h-full justify-end pr-6px h-30px">
            <div class="mr-1">
                <NButton round size="tiny" tertiary @click="mainStore.showAbout = true" title="About">
                    <NIcon size="17">
                        <Information />
                    </NIcon>
                </NButton>
            </div>
            <div class="mr-1">
                <ThemeChangerDrawer />
            </div>
            <div class="mr-3">
                <ProfileDropdown />
            </div>
            <div
                v-show="isElectron"
                class="px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer rounded-md"
                :title="$t('minimize')"
                @click="minimizeWindow()"
            >
                <NIcon size="17">
                    <Subtract20Regular />
                </NIcon>
            </div>
            <div
                v-show="isElectron"
                class="px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer rounded-md"
                :title="$t('maximize')"
                @click="maximizeWindow()"
            >
                <NIcon size="17">
                    <SquareMultiple20Regular v-if="isMaximized" />
                    <Square20Regular v-else />
                </NIcon>
            </div>
            <div
                v-show="isElectron"
                class="px-1 flex h-full items-center hover:bg-opacity-80 hover:bg-red-600 cursor-pointer rounded-md"
                :title="$t('close')"
                @click="closeWindow()"
            >
                <NIcon size="20">
                    <Close />
                </NIcon>
            </div>
        </div>
    </NLayoutHeader>
</template>
<style lang="scss">
.draggable-region {
    -webkit-app-region: drag;
    cursor: move;
}
</style>
