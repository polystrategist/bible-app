<script setup lang="ts">
import { NIcon, NButton } from 'naive-ui';
import { Download } from '@vicons/carbon';
import { useBibleDownloadStore } from '../../store/downloadBible';
const bibleDownloadStore = useBibleDownloadStore();
defineProps({
    title: {
        type: String,
    },
});
</script>
<template>
    <div class="w-full h-full">
        <div class="h-30px select-none flex justify-between">
            <h1 class="font-700">{{ $props.title }}</h1>
            <div>
                <NButton quaternary size="tiny" title="Download" @click="bibleDownloadStore.showBibleDownloadModal = true">
                    <template #icon>
                        <NIcon>
                            <Download />
                        </NIcon>
                    </template>
                </NButton>
            </div>
        </div>
        <div class="w-full h-[calc(100%-30px)] overflow-auto overflowing-div">
            <slot />
        </div>
    </div>
</template>
