<script setup lang="ts">
import { onMounted, ref, warn, watch } from 'vue';
import Editor from '../../../components/Editor/Editor.vue';
import useNoteStore from '../../../store/useNoteStore';
import SpaceStudyStore from '../../../store/SpaceStudyStore';

const spaceStudyStore = SpaceStudyStore();
const EditorRef = ref<{
    setContent: Function;
}>();
const noteStore = useNoteStore();

async function setNoteWhenSelectingADifferentSpace() {
    try {
        // get note
        const note = await window.browserWindow.getNote(
            spaceStudyStore.selectedSpaceStudy?.id as number
        );

        EditorRef.value?.setContent(note.content ?? '');
    } catch (error) {
        EditorRef.value?.setContent('');
    }
}

watch(
    () => spaceStudyStore.selectedSpaceStudy,
    async () => {
        await setNoteWhenSelectingADifferentSpace();
    }
);
</script>
<template>
    <div class="p-10px h-[calc(100%-20px)] relative dark:bg-dark-400 bg-white">
        <Editor ref="EditorRef" v-model="noteStore.note" overflow />
    </div>
</template>
