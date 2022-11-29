import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useBibleDownloadStore = defineStore('useBibleDownloadStore', () => {
    const showBibleDownloadModal = ref<boolean>(false);
    return {
        showBibleDownloadModal,
    };
});
