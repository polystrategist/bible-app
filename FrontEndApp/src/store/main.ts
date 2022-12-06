import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useMainStore = defineStore('useMainStore', () => {
    const version = ref('0.0.1');

    return {
        version,
    };
});
