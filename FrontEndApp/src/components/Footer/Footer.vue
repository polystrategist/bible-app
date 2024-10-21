<script lang="ts" setup>
import { NLayoutFooter, NProgress, NButton } from 'naive-ui';
import { onBeforeMount, onMounted, ref } from 'vue';
import { useMainStore } from '../../store/main';
import { useNetwork } from '@vueuse/core';
import VerseSelector from './VerseSelector/VerseSelector.vue';
import { useMenuStore } from '../../store/menu';

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
});
</script>
<template>
    <NLayoutFooter bordered class="flex cursor-default select-none items-center pl-8px light:bg-gray-100">
        <div class="whitespace-nowrap flex items-center gap-1 w-full max-w-300px">
            <span class="text-size-12px"> {{ $t('version') }} {{ mainStore.version }} </span>
        </div>
        <div class="w-full text-center z-50 font-700">
            <VerseSelector v-if="menuStore.menuSelected === 'read-bible'" />
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
