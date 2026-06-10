import { defineStore } from 'pinia';
import { ref } from 'vue';

/**
 * Visibility for the global Feedback dialog (FeedbackModal.vue, mounted once in
 * App.vue). Opened from the Help menu.
 */
export const useFeedbackModalStore = defineStore('feedbackModal', () => {
    const open = ref(false);
    function show() {
        open.value = true;
    }
    function hide() {
        open.value = false;
    }
    return { open, show, hide };
});
