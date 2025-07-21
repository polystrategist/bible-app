<script setup lang="ts">
import { NModal, NCard, NButton, NIcon, useMessage, NInput } from 'naive-ui';
import { computed, ref } from 'vue';
import { useBibleDownloadStore } from '../../store/downloadBible';
import { useModuleStore } from '../../store/moduleStore';
import { bible } from '../../util/modules';
import { Download } from '@vicons/carbon';

const searchBible = ref<string | null>(null);
const message = useMessage();
const bibleDownloadStore = useBibleDownloadStore();
const moduleStore = useModuleStore();
const downloadPercentage = ref<number>(0);
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
function clickDownload(downloadLink: string, version: any) {
    selectedDownloadLink.value = downloadLink;

    bibleDownloadStore.isDownloading = true;
    downloadLoading.value = true;
    window.browserWindow.downloadModule({
        urls: [downloadLink],
        percentage: (percentage: number) => {
            console.log(percentage);
            downloadPercentage.value = percentage;
        },
        done: async () => {
            downloadLoading.value = false;
            await moduleStore.getBibleLists();
            bibleDownloadStore.isDownloading = false;
        },
        cancel: () => {
            downloadLoading.value = false;
            bibleDownloadStore.isDownloading = false;
            message.error('Download Cancelled');
        },
    }, version);
}
</script>
<template>
    <NModal v-model:show="bibleDownloadStore.showBibleDownloadModal">
        <NCard style="width: 600px" :bordered="false" size="small" role="dialog" aria-modal="true">
            <div class="mb-2">
                <h1 class="font-800 select-none m-0 capitalize">{{ $t('bible version') }}</h1>
                <NInput v-model:value="searchBible" placeholder="Search..." size="small" />
            </div>
            <div v-if="BibleVersions.length" class="select-none h-[70vh] overflow-y-auto overflowing-div">
                <template v-for="version in BibleVersions">
                    <div v-if="!version.title.includes('commentaries')" v-show="!searchBible || version.title.toLowerCase().includes(searchBible.toLowerCase())"
                        :disabled="bibleDownloadStore.isDownloading" class="flex gap-10px items-center my-3">
                        <NButton size="tiny" :disabled="!isAlreadyDownloaded(version.file_name) || downloadLoading"
                            :type="!isAlreadyDownloaded(version.file_name) ? 'default' : 'info'"
                            @click="clickDownload(version.download_link, version)" secondary rounded
                            :loading="version.download_link === selectedDownloadLink && downloadLoading">
                            <NIcon>
                                <Download />
                            </NIcon>
                            <span class="capitalize">{{ isAlreadyDownloaded(version.file_name) ? $t('add') :
                                $t('added') }}</span>
                            <span v-if="version.download_link === selectedDownloadLink && downloadLoading" class="px-2">
                                {{
                                    downloadPercentage }}% </span>
                        </NButton>

                        <div :value="version.download_link">
                            <div>
                                "{{ version.title }}"
                            </div>
                        </div>

                    </div>
                </template>
            </div>
            <div v-else class="flex items-center justify-center h-[80vh]">It seems you have downloaded all the modules
                😊</div>
        </NCard>
    </NModal>
</template>
