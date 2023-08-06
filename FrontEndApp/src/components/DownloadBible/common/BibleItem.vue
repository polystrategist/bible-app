<script setup lang="ts">
import { NButton } from 'naive-ui';
import { ref } from 'vue';
import { useBibleDownloadStore } from '../../../store/downloadBible';
import { useModuleStore } from '../../../store/moduleStore';

const props = defineProps(['version']);
const moduleStore = useModuleStore();
const percentage = ref(0);
const downloadBibleStore = useBibleDownloadStore();

function clickDownload() {
    downloadBibleStore.isDownloading = true;
    downloadBibleStore.downloadingVersion = props.version.file_name;
    window.browserWindow.downloadModule({
        url: props.version.download_link as any,
        progress: (data: any) => {
            percentage.value = data.percent * 100;
        },
        done: async () => {
            await moduleStore.getBibleLists();
            downloadBibleStore.isDownloading = false;
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
            <NButton size="tiny" @click="clickDownload" :disabled="downloadBibleStore.isDownloading">
                {{
                    downloadBibleStore.isDownloading && downloadBibleStore.downloadingVersion == props.version.file_name
                        ? `${percentage}%`
                        : 'Download'
                }}
            </NButton>
        </div>
    </div>
</template>
