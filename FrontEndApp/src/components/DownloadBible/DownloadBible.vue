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
    return bible
        .filter((version) => {
            for (const item of moduleStore.bibleLists) {
                if (version.file_name == item.file_name) return false;
            }
            return true;
        })
        .sort((a, b) => (a.title as any) - (b.title as any));
});
</script>
<template>
    <NModal v-model:show="bibleDownloadStore.showBibleDownloadModal">
        <NCard style="width: 600px" :bordered="false" size="small" role="dialog" aria-modal="true">
            <h1 class="font-800 select-none">Modules</h1>
            <div v-if="BibleVersions.length" class="flex flex-col gap-2px select-none h-[80vh] overflow-y-auto overflowing-div">
                <template v-for="version in BibleVersions">
                    <BibleItem :version="version" />
                </template>
            </div>
            <div class="flex items-center justify-center h-[80vh]">It seems you have downloaded all the modules 😊</div>
        </NCard>
    </NModal>
</template>
