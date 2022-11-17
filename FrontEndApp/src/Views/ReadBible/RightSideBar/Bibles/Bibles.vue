<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import { getDownloadedBible } from '../../../../util/Modules/Controller/FeBibleController';
import { NCheckbox, NCheckboxGroup, useMessage } from 'naive-ui';
import RightSideBarContainer from './../../../../components/ReadBible/RightSideBarContainer.vue';
import { useBibleStore } from '../../../../store/BibleStore';

const message = useMessage();
const bibleStore = useBibleStore();
const bibleLists = ref<Array<any>>([]);

async function getBibleLists() {
    bibleLists.value = await getDownloadedBible();
}

function handleCheckBox(bibleVersions: Array<any>) {
    if (!bibleVersions.length) {
        message.warning('Oops.. Default to have 1 selected.');
        bibleStore.selectedBibleVersions = [bibleStore.DefaultSelectedVersion];
    }
}

onBeforeMount(() => {
    getBibleLists();
});
</script>
<template>
    <RightSideBarContainer title="Bible List">
        <NCheckboxGroup v-model:value="bibleStore.selectedBibleVersions" @update:value="handleCheckBox">
            <template v-for="bible in bibleLists">
                <NCheckbox :value="bible.file_name" :label="bible.title" />
            </template>
        </NCheckboxGroup>
    </RightSideBarContainer>
</template>
