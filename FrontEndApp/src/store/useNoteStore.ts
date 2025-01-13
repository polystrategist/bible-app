import { defineStore } from "pinia";
import { ref } from "vue";

export default defineStore('useNotesStore', () => {
    const note = ref<string>('');

    function storeNote() {
        // NOTE: save note to database table
    }

    return {
        note,
        storeNote
    }
})