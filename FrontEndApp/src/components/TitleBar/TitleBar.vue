<script lang='ts' setup>
import { NIcon, NLayoutHeader } from 'naive-ui';
import {
    Heart24Filled,
    Square20Regular,
    SquareMultiple20Regular,
    Subtract20Regular,
    WeatherMoon20Regular,
    WeatherSunny20Regular
} from '@vicons/fluent';
import { Close, Information } from '@vicons/carbon';
import { onBeforeMount, ref } from 'vue';
import Logo from './../../assets/logo.svg';
import { useThemeStore } from '../../store/theme';
import { useMainStore } from '../../store/main';
import { useMenuStore } from '../../store/menu';

const isMaximized = ref(false);
const themeStore = useThemeStore();
const mainStore = useMainStore();
const menuStore = useMenuStore();
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


onBeforeMount(async () => {
    isMaximized.value = await window.browserWindow.isWindowBrowserMaximized();
});
</script>
<template>
    <NLayoutHeader bordered class='flex cursor-default select-none items-center pl-8px light:bg-gray-100'>
        <div class='whitespace-nowrap flex items-center gap-1'>
            <div class='w-18px'>
                <img :src='Logo' alt='believers sword logo' />
            </div>
            <span class='capitalize'>
                {{ $t('title') }} {{ mainStore.appName.includes('nightly') ? 'Nightly' : '' }}
                <span class='text-size-10px'> {{ mainStore.version }} </span>
            </span>
        </div>
        <div id='draggable-region' class='w-full h-full text-center cursor-move z-50'></div>
        <div class='flex items-center h-full'>
            <div
                class='px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer'
                @click='mainStore.showAbout = true'
            >
                <NIcon size='17'>
                    <Information />
                </NIcon>
                <span class='text-size-12px ml-1'>About</span>
            </div>
            <div
                class='px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer'
                @click="menuStore.setMenu('/donate-page')"
            >
                <NIcon size='17'>
                    <Heart24Filled />
                </NIcon>
                <span class='text-size-12px ml-1'>Donate</span>
            </div>
            <div
                :class='{"mr-50px": isElectron}'
                class='px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer mr-10px'
                @click='changeTheme()'
            >
                <NIcon size='17'>
                    <WeatherMoon20Regular v-if='themeStore.isDark' />
                    <WeatherSunny20Regular v-else />
                </NIcon>
                <span class='text-size-12px ml-1' v-if='themeStore.isDark'>Dark</span>
                <span class='text-size-12px ml-1' v-else>Light</span>
            </div>
            <div
                v-show='isElectron'
                class='px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer'
                title='Minimize'
                @click='minimizeWindow()'
            >
                <NIcon size='17'>
                    <Subtract20Regular />
                </NIcon>
            </div>
            <div
                v-show='isElectron'
                class='px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer'
                title='Maximize'
                @click='maximizeWindow()'
            >
                <NIcon size='17'>
                    <SquareMultiple20Regular v-if='isMaximized' />
                    <Square20Regular v-else />
                </NIcon>
            </div>
            <div
                v-show='isElectron'
                class='px-1 flex h-full items-center hover:bg-opacity-80 hover:bg-red-600 cursor-pointer'
                title='Close'
                @click='closeWindow()'
            >
                <NIcon size='20'>
                    <Close />
                </NIcon>
            </div>
        </div>
    </NLayoutHeader>
</template>
<style lang='scss'>
#draggable-region {
  -webkit-app-region: drag;
  cursor: move;
}
</style>
