<script setup lang="ts">
import { NModal, NCard, NButton, NAlert, NCheckbox, NCheckboxGroup } from 'naive-ui';
import { computed, ref } from 'vue';
import { useBibleDownloadStore } from '../../store/downloadBible';
import { useModuleStore } from '../../store/moduleStore';
import { bible } from './../../util/modules';

const bibleDownloadStore = useBibleDownloadStore();
const moduleStore = useModuleStore();
const urlsToDownload = ref<null | Array<string>>(null);
const BibleVersions = computed(() => {
    return bible.sort((a, b) => (a.title as any) - (b.title as any));
});

function isAlreadyDownloaded(file_name: string) {
    for (const item of moduleStore.bibleLists) {
        if (file_name == item.file_name) return false;
    }
    return true;
}

function clickDownload() {
    bibleDownloadStore.isDownloading = true;

    window.browserWindow.downloadModule({
        urls: urlsToDownload.value?.map((url) => url),
        progress: (data: any) => {
            // console.log(data);
            // percentage.value = data.percent * 100;
        },
        done: async () => {
            await moduleStore.getBibleLists();
            bibleDownloadStore.isDownloading = false;
        },
    });
}
</script>
<template>
    <NModal v-model:show="bibleDownloadStore.showBibleDownloadModal">
        <NCard style="width: 600px" :bordered="false" size="small" role="dialog" aria-modal="true">
            <div class="flex justify-between items-center mb-2">
                <h1 class="font-800 select-none">Available Versions</h1>
                <NButton
                    size="small"
                    :disabled="bibleDownloadStore.isDownloading"
                    :loading="bibleDownloadStore.isDownloading"
                    @click="clickDownload()"
                >
                    Download Selected
                </NButton>
            </div>
            <NAlert type="warning"> Can Download One Item at a Time. </NAlert>
            <div v-if="BibleVersions.length" class="select-none h-[70vh] overflow-y-auto overflowing-div">
                <NCheckboxGroup
                    :disabled="bibleDownloadStore.isDownloading"
                    v-model:value="urlsToDownload"
                    class="flex flex-col gap-10px py-5"
                >
                    <template v-for="version in BibleVersions">
                        <NCheckbox :disabled="!isAlreadyDownloaded(version.file_name)" :value="version.download_link">
                            <div>
                                "{{ version.title }}" -
                                <span class="italic">
                                    lang: <span class="font-700">{{ version.language_full }}</span>
                                </span>
                            </div>
                        </NCheckbox>
                    </template>
                </NCheckboxGroup>
            </div>
            <div v-else class="flex items-center justify-center h-[80vh]">It seems you have downloaded all the modules 😊</div>
        </NCard>
    </NModal>
</template>
