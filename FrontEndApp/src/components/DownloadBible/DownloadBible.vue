<script setup lang="ts">
import { forEach } from 'lodash';
import { NModal, NCard, NButton } from 'naive-ui';
import { computed } from 'vue';
import { useBibleDownloadStore } from '../../store/downloadBible';
import { useModuleStore } from '../../store/moduleStore';
import { bible } from './../../util/modules';
import BibleItem from './common/BibleItem.vue';

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
</script>
<template>
    <NModal v-model:show="bibleDownloadStore.showBibleDownloadModal">
        <NCard style="width: 600px" :bordered="false" size="small" role="dialog" aria-modal="true">
            <h1 class="font-800 select-none">Available Versions</h1>
            <div v-if="BibleVersions.length" class="flex flex-col gap-2px select-none h-[80vh] overflow-y-auto overflowing-div">
                <template v-for="version in BibleVersions">
                    <BibleItem v-show="isAlreadyDownloaded(version.file_name)" :version="version" />
                </template>
            </div>
            <div v-else class="flex items-center justify-center h-[80vh]">It seems you have downloaded all the modules 😊</div>
        </NCard>
    </NModal>
</template>
