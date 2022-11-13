<script lang="ts" setup>
import { Splitpanes, Pane } from 'splitpanes';
import { onBeforeMount, ref } from 'vue';
import SESSION from '../../util/session';
import LeftSideBar from './LeftSideBar/LeftSideBar.vue';
import RightSideBar from './RightSideBar/RightSideBar.vue';
import ViewVerses from './ViewVerses/ViewVerses.vue';

const storageReadBibleSavedSplitPaneSizes = 'storageReadBibleSavedSplitPaneSizes';
const splitPaneSizes = ref<Array<{ min: number; max: number; size: number }>>([
    { min: 15, max: 30, size: 20 },
    { min: 30, max: 60, size: 60 },
    { min: 15, max: 30, size: 25 },
]);

function changeSize(sizes: Array<any>) {
    SESSION.set(storageReadBibleSavedSplitPaneSizes, sizes);
}

onBeforeMount(() => {
    const saveSizes = SESSION.get(storageReadBibleSavedSplitPaneSizes);
    if (saveSizes) splitPaneSizes.value = saveSizes;
});
</script>

<template>
    <Splitpanes vertical class="h-full w-full" @resized="changeSize">
        <Pane :size="splitPaneSizes[0].size" :min-size="splitPaneSizes[0].min" :max-size="splitPaneSizes[0].max">
            <LeftSideBar />
        </Pane>
        <Pane
            class="bg-gray-100 dark:bg-dark-700 p-3"
            :size="splitPaneSizes[1].size"
            :min-size="splitPaneSizes[1].min"
            :max-size="splitPaneSizes[1].max"
        >
            <ViewVerses />
        </Pane>
        <Pane :size="splitPaneSizes[2].size" :min-size="splitPaneSizes[2].min" :max-size="splitPaneSizes[2].max">
            <RightSideBar />
        </Pane>
    </Splitpanes>
</template>
