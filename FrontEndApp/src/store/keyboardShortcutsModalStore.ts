import { defineStore } from 'pinia';
import { ref } from 'vue';

/**
 * Visibility for the global Keyboard Shortcuts dialog
 * (KeyboardShortcutsModal.vue, mounted once in App.vue). Opened from the Help menu.
 */
export const useKeyboardShortcutsModalStore = defineStore('keyboardShortcutsModal', () => {
    const open = ref(false);
    function show() {
        open.value = true;
    }
    function hide() {
        open.value = false;
    }
    return { open, show, hide };
});
