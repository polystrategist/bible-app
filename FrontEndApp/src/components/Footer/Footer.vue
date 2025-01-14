<script lang="ts" setup>
import { NLayoutFooter, NProgress, NButton, NIcon } from 'naive-ui';
import { onBeforeMount, onMounted, ref } from 'vue';
import { useMainStore } from '../../store/main';
import { useNetwork } from '@vueuse/core';
import VerseSelectorButton from './../VerseSelector.vue';
import { useMenuStore } from '../../store/menu';
import { useBibleStore } from '../../store/BibleStore';
import { Note24Regular, Note28Filled, PointScan24Filled } from '@vicons/fluent';
import useNoteStore from '../../store/useNoteStore';
import { useThemeStore } from '../../store/theme';

const themeStore = useThemeStore();
const noteStore = useNoteStore();
const bibleStore = useBibleStore();
const network = useNetwork();
const mainStore = useMainStore();
const menuStore = useMenuStore();
const downloadPercentage = ref<number>(0);
const selectedFaceForToday = ref('😁');
const faceForToday = ['😁', '✊', '😍', '💖', '😇', '😂', '😲', '(❁´◡`❁)', '✋', '📂', '😎'];

onBeforeMount(() => {
    const randomIndex = Math.floor(Math.random() * faceForToday.length);
    selectedFaceForToday.value = faceForToday[randomIndex];
});

onMounted(() => {
    window.browserWindow.updateDownloadProgress({
        percentage: (percentage: number) => {
            downloadPercentage.value = percentage;
        },
        done: () => {
            downloadPercentage.value = 0;
        },
    });

    if (network.isSupported) {
    } else {
    }

    document.addEventListener('keydown', function (event) {
        // Check if Control, Shift, and N are pressed together
        if (event.ctrlKey && event.shiftKey && event.key === 'N') {
            noteStore.showNote = !noteStore.showNote;
        }
    });
});
</script>
<template>
    <NLayoutFooter
        bordered
        class="flex cursor-default select-none items-center pl-8px light:bg-white"
    >
        <div class="whitespace-nowrap flex items-center gap-1 w-full max-w-300px">
            <span class="text-size-12px"> {{ $t('version') }} {{ mainStore.version }} </span>
        </div>
        <div class="w-full text-center z-50 font-700 flex items-center justify-center">
            <VerseSelectorButton v-if="menuStore.menuSelected === 'read-bible'" size="tiny">
                <template #icon>
                    <NIcon>
                        <PointScan24Filled />
                    </NIcon>
                </template>
                {{ $t(bibleStore.getSelectedData.book) }}
                {{ bibleStore.getSelectedData.chapter }}
            </VerseSelectorButton>
            <NButton
                secondary
                size="tiny"
                @click="noteStore.showNote = !noteStore.showNote"
                :type="noteStore.showNote ? 'primary' : 'default'"
                title="Ctr + Shift + N"
            >
                <template #icon>
                    <NIcon>
                        <Note24Regular v-if="!themeStore.isDark" />
                        <Note28Filled v-else />
                    </NIcon>
                </template>
                Note
            </NButton>
        </div>
        <div class="flex items-center w-full max-w-300px justify-end pr-2">
            <div v-if="downloadPercentage > 0" class="w-150px flex items-center gap-1">
                <span class="text-size-10px">Updating</span>
                <NProgress :percentage="downloadPercentage" type="line" />
            </div>
            <div>{{ selectedFaceForToday }}</div>
        </div>
    </NLayoutFooter>
</template>
