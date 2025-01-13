<script lang="ts" setup>
import { Splitpanes, Pane } from 'splitpanes';
import { onBeforeMount, ref } from 'vue';
import SESSION from '../../util/session';
import LeftSideBar from './LeftSideBar/LeftSideBar.vue';
import RightSideBar from './RightSideBar/RightSideBar.vue';
import ViewVerses from './ViewVerses/ViewVerses.vue';
import Editor from '../../components/Editor/Editor.vue';
import TakeNote from './TakeNote/TakeNote.vue';

const storageReadBibleSavedSplitPaneSizes = 'storageReadBibleSavedSplitPaneSizes';
const storageViewVerseSplitPaneSizes = 'storageViewVerseSplitPaneSizes';

const splitPaneSizes = ref<Array<{ min: number; max: number; size: number }>>([
    { min: 15, max: 30, size: 20 },
    { min: 30, max: 60, size: 60 },
    { min: 15, max: 30, size: 25 },
]);

const verseViewPaneSizes = ref<Array<{ min: number; max: number; size: number }>>([
    { min: 30, max: 100, size: 70 },
    { min: 20, max: 70, size: 30 },
]);

function changeSize(sizes: Array<any>) {
    SESSION.set(storageReadBibleSavedSplitPaneSizes, sizes);
}

function changeViewVerseSize(sizes: Array<any>) {
    SESSION.set(storageViewVerseSplitPaneSizes, sizes);
}

onBeforeMount(() => {
    const saveSizes = SESSION.get(storageReadBibleSavedSplitPaneSizes);
    if (saveSizes) splitPaneSizes.value = saveSizes;

    const saveViewVerseSizes = SESSION.get(storageViewVerseSplitPaneSizes);
    if (saveViewVerseSizes) verseViewPaneSizes.value = saveViewVerseSizes;
});
</script>

<template>
    <Splitpanes vertical class="h-full w-full" @resized="changeSize">
        <Pane
            class="bg-gray-100 dark:bg-dark-600"
            :size="splitPaneSizes[0].size"
            :min-size="splitPaneSizes[0].min"
            :max-size="splitPaneSizes[0].max"
        >
            <LeftSideBar />
        </Pane>
        <Pane class="dark:bg-dark-800 h-full">
            <Splitpanes
                horizontal
                class="h-full w-full splitpanes_show_bar"
                @resized="changeViewVerseSize"
            >
                <Pane :min-size="30">
                    <ViewVerses />
                </Pane>
                <Pane
                    class="bg-gray-100 dark:bg-dark-600 relative !overflow-auto"
                    :size="verseViewPaneSizes[1].size"
                    :min-size="verseViewPaneSizes[1].min"
                    :max-size="verseViewPaneSizes[1].max"
                >
                    <TakeNote />
                </Pane>
            </Splitpanes>
        </Pane>
        <Pane
            class="bg-gray-100 dark:bg-dark-600"
            :size="splitPaneSizes[2].size"
            :min-size="splitPaneSizes[2].min"
            :max-size="splitPaneSizes[2].max"
        >
            <RightSideBar />
        </Pane>
    </Splitpanes>
</template>
