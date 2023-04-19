import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore('useUserStore', () => {
    const user = ref<any>(null)

    return {
        user
    }
});