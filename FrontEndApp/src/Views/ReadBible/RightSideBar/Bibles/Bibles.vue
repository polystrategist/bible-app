<script setup lang="ts">
import { NCheckbox, NCheckboxGroup, useMessage, NIcon, NButton } from 'naive-ui';
import RightSideBarContainer from './../../../../components/ReadBible/RightSideBarContainer.vue';
import { useBibleStore } from '../../../../store/BibleStore';
import { useModuleStore } from '../../../../store/moduleStore';
import { useBibleDownloadStore } from '../../../../store/downloadBible';
import { Download, DocumentImport } from '@vicons/carbon';

const message = useMessage();
const bibleStore = useBibleStore();
const moduleStore = useModuleStore();
const bibleDownloadStore = useBibleDownloadStore();

function handleCheckBox(bibleVersions: Array<any>) {
    if (!bibleVersions.length) {
        message.warning('Oops.. Default to have 1 selected.');
        bibleStore.selectedBibleVersions = [bibleStore.DefaultSelectedVersion];
    }
    bibleStore.getVerses();
}
</script>
<template>
    <RightSideBarContainer :title="$t('Bible List')">
        <div class="flex gap-4px mb-6px">
            <NButton quaternary size="tiny" title="Download" @click="bibleDownloadStore.showBibleDownloadModal = true">
                <template #icon>
                    <NIcon>
                        <Download />
                    </NIcon>
                </template>
                <span class="capitalize">{{ $t('download') }}</span>
            </NButton>
            <NButton quaternary size="tiny" title="Import" @click="bibleDownloadStore.showImportBibleModal = true">
                <template #icon>
                    <NIcon>
                        <DocumentImport />
                    </NIcon>
                </template>
                <span class="capitalize">{{ $t('import') }}</span>
            </NButton>
        </div>
        <NCheckboxGroup v-model:value="bibleStore.selectedBibleVersions" @update:value="handleCheckBox" class="flex flex-col">
            <template v-for="bible in moduleStore.bibleLists">
                <NCheckbox v-if="!bible.title.includes('commentaries')" :value="bible.file_name"
                    :label="`${bible.title}`" />
            </template>
        </NCheckboxGroup>
    </RightSideBarContainer>
</template>
