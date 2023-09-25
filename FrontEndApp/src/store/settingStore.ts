import { defineStore } from 'pinia';
import { onMounted, ref, watch } from 'vue';
import SESSION from '../util/session';

export const useSettingStore = defineStore('settingStore', () => {
    const showDeuterocanonicalStorageKey = 'show-deuterocanonical';
    const showDeuterocanonical = ref(false);

    onMounted(() => {
        const showDeuterocanonicalStored = SESSION.get(showDeuterocanonicalStorageKey);
        if (showDeuterocanonicalStored) showDeuterocanonical.value = showDeuterocanonicalStored;
        else SESSION.set(showDeuterocanonicalStorageKey, showDeuterocanonical.value);
    });

    watch(
        () => showDeuterocanonical.value,
        (newData, oldData) => {
            if (newData !== oldData) SESSION.set(showDeuterocanonicalStorageKey, newData);
        }
    );

    return {
        showDeuterocanonical,
    };
});
