<script lang="ts" setup>
import { NLayoutFooter, NProgress, NButton, NIcon, NTag } from 'naive-ui';
import { onBeforeMount, onMounted, ref } from 'vue';
import { useMainStore } from '../../store/main';
import { useNetwork } from '@vueuse/core';
import VerseSelectorButton from './../VerseSelector.vue';
import { useMenuStore } from '../../store/menu';
import { useBibleStore } from '../../store/BibleStore';
import { Book24Regular } from '@vicons/fluent';
import useNoteStore from '../../store/useNoteStore';
import { useSettingStore } from '../../store/settingStore';
import { useTTSStore } from '../../store/ttsStore';
import { usePiperTTSStore } from '../../store/piperTTSStore';
import { useThemeStore } from '../../store/theme';
import TTSFooterPlayer from '../TTS/TTSFooterPlayer.vue';

const noteStore = useNoteStore();
const themeStore = useThemeStore();
const bibleStore = useBibleStore();
const ttsStore = useTTSStore();
const piperStore = usePiperTTSStore();
const network = useNetwork();
const mainStore = useMainStore();
const menuStore = useMenuStore();
const settingStore = useSettingStore();
const showBetaTag = !window.isElectron;

type UpdateStatus = 'idle' | 'available' | 'downloading' | 'ready';

const updateStatus = ref<UpdateStatus>('idle');
const updateVersion = ref('');
const downloadPercent = ref(0);
const selectedFaceForToday = ref('😁');
const faceForToday = ['😁', '✊', '😍', '💖', '😇', '😂', '😲', '(❁´◡`❁)', '✋', '📂', '😎'];

onBeforeMount(() => {
    const randomIndex = Math.floor(Math.random() * faceForToday.length);
    selectedFaceForToday.value = faceForToday[randomIndex];
});

onMounted(() => {
    if (window.isElectron) {
        window.browserWindow.onUpdateAvailable((version: string) => {
            updateVersion.value = version;
            updateStatus.value = 'available';
        });

        window.browserWindow.onUpdateProgress((percent: number) => {
            downloadPercent.value = percent;
            updateStatus.value = 'downloading';
        });

        window.browserWindow.onUpdateDownloaded(() => {
            updateStatus.value = 'ready';
            downloadPercent.value = 100;
        });
    }

    if (network.isSupported) {
    } else {
    }

    document.addEventListener('keydown', function (event) {
        // Check if Control, Shift, and N are pressed together
        if (event.ctrlKey && event.shiftKey && event.key === 'N') {
            noteStore.showNote = !noteStore.showNote;
        }

        // Ctrl+Shift+- → decrease scale  (event.code used so it works regardless of keyboard layout)
        // Ctrl+Shift++ → increase scale
        if (event.ctrlKey && event.shiftKey && event.code === 'Minus') {
            event.preventDefault();
            settingStore.appScale = Math.max(0.75, Math.round((settingStore.appScale - 0.05) * 100) / 100);
        }
        if (event.ctrlKey && event.shiftKey && event.code === 'Equal') {
            event.preventDefault();
            settingStore.appScale = Math.min(1.5, Math.round((settingStore.appScale + 0.05) * 100) / 100);
        }
    });
});

function startDownload() {
    updateStatus.value = 'downloading';
    downloadPercent.value = 0;
    window.browserWindow.downloadUpdate();
}

function installUpdate() {
    window.browserWindow.installUpdate();
}
</script>
<template>
    <NLayoutFooter
        bordered
        class="flex cursor-default select-none items-center pl-8px light:bg-white"
    >
        <div class="whitespace-nowrap flex items-center gap-1 w-full max-w-300px">
            <span class="text-size-12px"> {{ $t('version') }} {{ mainStore.version }} </span>
            <NTag v-if="showBetaTag" size="small" type="warning" round :bordered="false">
                Beta Version
            </NTag>
        </div>
        <div
            class="w-full text-center z-50 font-700 flex items-center justify-center flex items-center gap-2"
        >
            <!-- TTS player takes over center when active -->
            <TTSFooterPlayer v-if="(ttsStore.isActive || piperStore.isActive) && menuStore.menuSelected === 'read-bible'" />
            <template v-else>
                <VerseSelectorButton v-if="menuStore.menuSelected === 'read-bible'" size="tiny">
                    <template #icon>
                        <NIcon>
                            <Book24Regular />
                        </NIcon>
                    </template>
                    {{ $t(bibleStore.getSelectedData.book) }}
                    {{ bibleStore.getSelectedData.chapter }}
                </VerseSelectorButton>
            </template>
        </div>
        <div class="flex items-center w-full max-w-300px justify-end pr-2 gap-2">
            <!-- Update available -->
            <template v-if="updateStatus === 'available'">
                <NButton size="tiny" type="primary" @click="startDownload">
                    Update v{{ updateVersion }}
                </NButton>
            </template>

            <!-- Downloading -->
            <template v-else-if="updateStatus === 'downloading'">
                <span class="text-size-10px opacity-70 whitespace-nowrap">Updating {{ downloadPercent }}%</span>
                <div class="w-100px">
                    <NProgress :percentage="downloadPercent" type="line" :show-indicator="false" :height="4" />
                </div>
            </template>

            <!-- Ready to install -->
            <template v-else-if="updateStatus === 'ready'">
                <NButton size="tiny" type="warning" :style="themeStore.isDark ? 'color: #1a1a1a;' : ''" @click="installUpdate">
                    Install &amp; Restart
                </NButton>
            </template>

            <div v-if="updateStatus === 'idle'">{{ selectedFaceForToday }}</div>
        </div>
    </NLayoutFooter>
</template>
