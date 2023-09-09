<script setup lang="ts">
import { NCheckbox, NCheckboxGroup, useMessage, NIcon, NButton } from 'naive-ui';
import RightSideBarContainer from './../../../../components/ReadBible/RightSideBarContainer.vue';
import { useBibleStore } from '../../../../store/BibleStore';
import { useModuleStore } from '../../../../store/moduleStore';
import { useBibleDownloadStore } from '../../../../store/downloadBible';
import { Download } from '@vicons/carbon';

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
        <template #rightSide>
            <NButton quaternary size="tiny" title="Download" @click="bibleDownloadStore.showBibleDownloadModal = true">
                <template #icon>
                    <NIcon>
                        <Download />
                    </NIcon>
                </template>
                Download
            </NButton>
        </template>
        <NCheckboxGroup v-model:value="bibleStore.selectedBibleVersions" @update:value="handleCheckBox">
            <template v-for="bible in moduleStore.bibleLists">
                <NCheckbox :value="bible.file_name" :label="`${bible.title}`" /><br />
            </template>
        </NCheckboxGroup>
    </RightSideBarContainer>
</template>
