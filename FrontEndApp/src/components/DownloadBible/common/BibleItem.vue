<script setup lang="ts">
import { NButton, useMessage } from 'naive-ui';
import { ref } from 'vue';
import { useModuleStore } from '../../../store/moduleStore';

const props = defineProps(['version']);
const moduleStore = useModuleStore();
const downloading = ref(false);
const percentage = ref(0);
const message = useMessage();

async function clickDownload() {
    downloading.value = true;
    await window.browserWindow.downloadModule({
        url: props.version.download_link,
        progress: (data: any) => {
            percentage.value = data.percent * 100;
        },
        done: async () => {
            moduleStore.getBibleLists();
            downloading.value = false;
        },
    });
}
</script>
<template>
    <div class="p-2 hover:bg-light-50 hover:bg-opacity-20 flex justify-between">
        <div>
            "{{ $props.version.title }}" -
            <span class="italic">
                lang: <span class="font-700">{{ $props.version.language_full }}</span>
            </span>
        </div>
        <div>
            <NButton size="tiny" @click="clickDownload" :disabled="downloading">
                {{ downloading ? `${percentage}%` : 'Download' }}
            </NButton>
        </div>
    </div>
</template>
