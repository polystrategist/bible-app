import { defineStore } from 'pinia';
import { computed, ref, watch } from 'vue';

export const useUserStore = defineStore('useUserStore', () => {
    const user = ref<any>(null);
    const user_id = computed(() => {
        return user.value?.user?.id ?? null;
    });
    const syncData = ref<boolean>(false);

    function syncDataOnline() {
        window.syncDataOnline = setTimeout(() => {
            console.info('sync');
        }, 1000);
    }

    watch(
        () => syncData.value,
        (isSyncData) => {}
    );

    return {
        user,
        user_id,
        syncData,
    };
});
