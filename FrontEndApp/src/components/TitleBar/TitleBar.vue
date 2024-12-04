<script lang="ts" setup>
import { NIcon, NLayoutHeader, NButton } from 'naive-ui';
import {
    CaretDown24Filled,
    CaretDown24Regular,
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
import ProfileDropdown from './Partials/ProfileDropdown.vue';
import ThemeChangerDrawer from '../ThemeChanger/ThemeChangerDrawer.vue';
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

onBeforeMount(async () => {
    if (window.isElectron) isMaximized.value = await window.browserWindow.isWindowBrowserMaximized();
});
</script>
<template>
    <NLayoutHeader bordered class="flex cursor-default select-none items-center pl-8px justify-between">
        <div class="whitespace-nowrap flex items-center gap-1 pl-0px">
            <LogoComponent class="w-20px h-20px" />
            <div class="mr-20px">{{ $t('Believers Sword') }}</div>
            <div>
                <NButton v-if="menuStore.menuSelected === 'read-bible'" quaternary size="tiny" round icon-placement="right">
                    Study Space
                    <template #icon>
                        <NIcon>
                            <CaretDown24Filled v-if="themeStore.isDark" />
                            <CaretDown24Regular v-else />
                        </NIcon>
                    </template>
                </NButton>
            </div>
        </div>
        <div class="flex items-center w-full h-full z-50 justify-between">
            <div class="draggable-region flex-grow cursor-move opacity-0">draggable region</div>
            <SearchBar />
            <div class="draggable-region flex-grow cursor-move opacity-0">draggable region</div>
        </div>
        <div class="flex items-center h-full justify-end pr-6px h-30px">
            <div class="mr-1">
                <NButton round size="tiny" quaternary  @click="mainStore.showAbout = true" title="About">
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
            <NButton v-show="isElectron" size="tiny" quaternary :title="$t('minimize')" @click="minimizeWindow()">
                <NIcon size="17">
                    <Subtract20Regular />
                </NIcon>
            </NButton>
            <NButton v-show="isElectron" size="tiny" quaternary :title="$t('maximize')" @click="maximizeWindow()">
                <NIcon size="15">
                    <SquareMultiple20Regular v-if="isMaximized" />
                    <Square20Regular v-else />
                </NIcon>
            </NButton>
            <NButton
                size="tiny"
                quaternary
                v-show="isElectron"
                :title="$t('close')"
                @click="closeWindow()"
                class="!hover:bg-red-5"
            >
                <NIcon size="20">
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
