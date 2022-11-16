<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import { getDownloadedBible } from '../../../../util/Modules/Controller/FeBibleController';
import { NCheckbox } from 'naive-ui';
import RightSideBarContainer from './../../../../components/ReadBible/RightSideBarContainer.vue';

const bibleLists = ref<Array<any>>([]);

async function getBibleLists() {
    bibleLists.value = await getDownloadedBible();
}

onBeforeMount(() => {
    getBibleLists();
});
</script>
<template>
    <RightSideBarContainer title="Bible List">
        <div v-for="bible in bibleLists">
            <NCheckbox>
                <span class="truncate">{{ bible.title }}</span>
            </NCheckbox>
        </div>
    </RightSideBarContainer>
</template>
