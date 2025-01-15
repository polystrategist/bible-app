import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import SpaceStudyStore from './SpaceStudyStore';

export default defineStore('useNotesStore', () => {
    const note = ref<string>('');
    const showNote = ref<boolean>(true);
    const spaceStudyStore = SpaceStudyStore();

    function storeNote() {
        // NOTE: save note to database table
        window.browserWindow.saveNote({
            note: note.value,
            space_study_id: spaceStudyStore.selectedSpaceStudy?.id as number | string,
        });
    }

    watch(
        () => note.value,
        () => {
            clearTimeout(window.takingNoteTimeOut);
            window.takingNoteTimeOut = setTimeout(() => {
                storeNote();
            }, 700);
        }
    );

    return {
        note,
        storeNote,
        showNote,
    };
});
