import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useBibleDownloadStore = defineStore('useBibleDownloadStore', () => {
    const showBibleDownloadModal = ref<boolean>(false);
    const showImportBibleModal = ref<boolean>(false);
    const isDownloading = ref(false);
    const isImporting = ref(false);
    const downloadingVersion = ref<null | string>(null);
    return {
        showBibleDownloadModal,
        showImportBibleModal,
        isDownloading,
        isImporting,
        downloadingVersion,
    };
});
