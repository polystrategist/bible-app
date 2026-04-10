import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useBibleDownloadStore = defineStore('useBibleDownloadStore', () => {
    const isDownloading = ref(false);
    const downloadingVersion = ref<null | string>(null);
    return {
        isDownloading,
        downloadingVersion,
    };
});
