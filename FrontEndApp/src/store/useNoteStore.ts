import { defineStore } from "pinia";
import { ref } from "vue";

export default defineStore('useNotesStore', () => {
    const note = ref<string>('');
    const showNote = ref<boolean>(true);

    function storeNote() {
        // NOTE: save note to database table
    }

    return {
        note,
        storeNote,
        showNote
    }
})