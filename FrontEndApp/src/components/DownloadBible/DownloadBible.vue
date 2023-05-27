<script setup lang="ts">
import { NModal, NCard, NButton, NIcon } from 'naive-ui';
import { computed, ref } from 'vue';
import { useBibleDownloadStore } from '../../store/downloadBible';
import { useModuleStore } from '../../store/moduleStore';
import { bible } from '../../util/modules';
import { Download } from '@vicons/carbon';

const bibleDownloadStore = useBibleDownloadStore();
const moduleStore = useModuleStore();
const BibleVersions = computed(() => {
    return bible.sort((a, b) => (a.title as any) - (b.title as any));
});

function isAlreadyDownloaded(file_name: string) {
    for (const item of moduleStore.bibleLists) {
        if (file_name == item.file_name) return false;
    }
    return true;
}

const downloadLoading = ref(false);
const selectedDownloadLink = ref<string | null>(null);
function clickDownload(downloadLink: string) {
    selectedDownloadLink.value = downloadLink;

    bibleDownloadStore.isDownloading = true;
    downloadLoading.value = true;
    window.browserWindow.downloadModule({
        urls: [downloadLink],
        done: async () => {
            downloadLoading.value = false;
            await moduleStore.getBibleLists();
            bibleDownloadStore.isDownloading = false;
        },
    });
}
</script>
<template>
    <NModal v-model:show="bibleDownloadStore.showBibleDownloadModal">
        <NCard style="width: 600px" :bordered="false" size="small" role="dialog" aria-modal="true">
            <div class="flex justify-between items-center">
                <h1 class="font-800 select-none">Available Versions</h1>
            </div>
            <div v-if="BibleVersions.length" class="select-none h-[70vh] overflow-y-auto overflowing-div">
                <div
                    v-for="version in BibleVersions"
                    :disabled="bibleDownloadStore.isDownloading"
                    class="flex gap-10px items-center my-3"
                >
                    <div :value="version.download_link">
                        <div>
                            "{{ version.title }}" -
                            <span class="italic">
                                lang: <span class="font-700">{{ version.language_full }}</span>
                            </span>
                        </div>
                    </div>
                    <NButton
                        size="tiny"
                        :disabled="!isAlreadyDownloaded(version.file_name) || downloadLoading"
                        :type="!isAlreadyDownloaded(version.file_name) ? 'default' : 'info'"
                        @click="clickDownload(version.download_link)"
                        secondary
                        rounded
                        :loading="version.download_link === selectedDownloadLink && downloadLoading"
                    >
                        <NIcon>
                            <Download />
                        </NIcon>
                        Download
                    </NButton>
                </div>
            </div>
            <div v-else class="flex items-center justify-center h-[80vh]">It seems you have downloaded all the modules 😊</div>
        </NCard>
    </NModal>
</template>
