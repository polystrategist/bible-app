<script lang="ts" setup>
import { NIcon, NLayoutHeader, NTooltip } from 'naive-ui';
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
import Logo from './../../assets/logo.svg';
import { useThemeStore } from '../../store/theme';
import { useMainStore } from '../../store/main';
import SearchBar from '../SearchBar.vue';
import LogoComponent from './../LogoComponent.vue';
import ProfileDropdown from './Partials/ProfileDropdown.vue';

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
    <NLayoutHeader bordered class="flex cursor-default select-none items-center pl-8px light:bg-gray-100 justify-between">
        <div class="whitespace-nowrap flex items-center gap-1 w-200px pl-0px">
            <NTooltip placement="right">
                <template #trigger>
                    <div class="w-28px">
                        <LogoComponent />
                    </div>
                </template>
                {{ $t('Believers Sword') }}
            </NTooltip>
        </div>
        <div class="flex items-center w-full h-full z-50 justify-between">
            <div class="draggable-region flex-grow cursor-move opacity-0">draggable region</div>
            <SearchBar />
            <div class="draggable-region flex-grow cursor-move opacity-0">draggable region</div>
        </div>
        <div class="flex items-center h-full justify-end pr-6px h-30px">
            <div
                class="px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer rounded-md"
                @click="mainStore.showAbout = true"
            >
                <NIcon size="17">
                    <Information />
                </NIcon>
                <span class="text-size-12px ml-1 capitalize whitespace-nowrap">{{ $t('about') }}</span>
            </div>
            <div
                class="px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer rounded-md"
                @click="openDonationInBrowser"
            >
                <NIcon size="17">
                    <Heart24Filled />
                </NIcon>
                <span class="text-size-12px ml-1 capitalize whitespace-nowrap">{{ $t('donate') }}</span>
            </div>
            <div
                :class="{ 'mr-50px': isElectron }"
                class="px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer mr-5px rounded-md"
                @click="changeTheme()"
            >
                <NIcon size="17">
                    <WeatherMoon20Regular v-if="themeStore.isDark" />
                    <WeatherSunny20Regular v-else />
                </NIcon>
                <span class="text-size-12px ml-1 capitalize whitespace-nowrap">
                    {{ themeStore.isDark ? $t('dark') : $t('light') }}
                </span>
            </div>
            <div class='mr-3'>
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
                    <SquareMultiple20Regular v-if="!isMaximized" />
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
