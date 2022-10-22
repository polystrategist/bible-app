<script setup lang="ts">
import { NLayoutHeader, NIcon } from "naive-ui";
import {
    Subtract20Regular,
    SquareMultiple20Regular,
    Square20Regular,
    WeatherSunny20Regular,
    WeatherMoon20Regular,
} from "@vicons/fluent";
import { Close } from "@vicons/carbon";
import { onBeforeMount, ref } from "vue";
import Logo from "./../../assets/logo.svg";
import { useThemeStore } from "../../store/theme";

const isMaximized = ref(false);
const themeStore = useThemeStore();

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
    const isWindowBrowserMaximized: boolean = await window.browserWindow.isWindowBrowserMaximized();
    isMaximized.value = isWindowBrowserMaximized;
});
</script>
<template>
    <NLayoutHeader class="flex cursor-default select-none items-center pl-8px">
        <div class="whitespace-nowrap flex items-center gap-1">
            <div class="w-18px">
                <img :src="Logo" />
            </div>
            <span> Believers Sword </span>
        </div>
        <div id="draggable-region" class="w-full h-full text-center cursor-move z-50"></div>
        <div class="flex items-center h-full">
            <div
                @click="changeTheme()"
                class="px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer mr-50px"
            >
                <NIcon size="17">
                    <WeatherMoon20Regular v-if="themeStore.isDark" />
                    <WeatherSunny20Regular v-else />
                </NIcon>
            </div>
            <div
                @click="minimizeWindow()"
                class="px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer"
            >
                <NIcon size="17">
                    <Subtract20Regular />
                </NIcon>
            </div>
            <div
                @click="maximizeWindow()"
                class="px-1 flex h-full items-center hover:bg-opacity-20 hover:bg-gray-200 cursor-pointer"
            >
                <NIcon size="17">
                    <SquareMultiple20Regular v-if="isMaximized" />
                    <Square20Regular v-else />
                </NIcon>
            </div>
            <div @click="closeWindow()" class="px-1 flex h-full items-center hover:bg-opacity-80 hover:bg-red-600 cursor-pointer">
                <NIcon size="20">
                    <Close />
                </NIcon>
            </div>
        </div>
    </NLayoutHeader>
</template>
<style lang="scss">
#draggable-region {
    -webkit-app-region: drag;
    cursor: move;
}
</style>
