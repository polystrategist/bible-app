<script setup lang="ts">
import { NButton } from 'naive-ui';
import { ref } from 'vue';
import { useBibleDownloadStore } from '../../../store/downloadBible';
import { useModuleStore } from '../../../store/moduleStore';

const props = defineProps(['version']);
const percentage = ref(0);
const downloadBibleStore = useBibleDownloadStore();

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
            <NButton size="tiny" :disabled="downloadBibleStore.isDownloading">
                {{
                    downloadBibleStore.isDownloading && downloadBibleStore.downloadingVersion == props.version.file_name
                        ? `${percentage}%`
                        : $t('download')
                }}
            </NButton>
        </div>
    </div>
</template>
