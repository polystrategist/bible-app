import { defineStore } from 'pinia';
import { onMounted, ref, watch } from 'vue';
import SESSION from '../util/session';

export const useSettingStore = defineStore('settingStore', () => {
    const showDeuterocanonicalStorageKey = 'show-deuterocanonical';
    const appScaleStorageKey = 'app-scale';
    const showDeuterocanonical = ref(false);
    const appScale = ref(1);
    const isLoadingScale = ref(false);

    onMounted(() => {
        const showDeuterocanonicalStored = SESSION.get(showDeuterocanonicalStorageKey);
        if (showDeuterocanonicalStored) showDeuterocanonical.value = showDeuterocanonicalStored;
        else SESSION.set(showDeuterocanonicalStorageKey, showDeuterocanonical.value);

        const savedScale = Number(SESSION.get(appScaleStorageKey));
        const fallbackScale = Number.isFinite(savedScale) ? savedScale : 1;
        appScale.value = Math.min(1.5, Math.max(0.75, fallbackScale));

        if (window.browserWindow?.getAppScale) {
            isLoadingScale.value = true;
            window.browserWindow
                .getAppScale()
                .then((scale) => {
                    appScale.value = Math.min(1.5, Math.max(0.75, Number(scale) || 1));
                    SESSION.set(appScaleStorageKey, appScale.value);
                })
                .finally(() => {
                    isLoadingScale.value = false;
                });
        }
    });

    watch(
        () => showDeuterocanonical.value,
        (newData, oldData) => {
            if (newData !== oldData) SESSION.set(showDeuterocanonicalStorageKey, newData);
        }
    );

    watch(
        () => appScale.value,
        async (newScale, oldScale) => {
            if (newScale === oldScale) return;

            const normalizedScale = Math.min(1.5, Math.max(0.75, Number(newScale) || 1));
            if (normalizedScale !== newScale) {
                appScale.value = normalizedScale;
                return;
            }

            SESSION.set(appScaleStorageKey, normalizedScale);
            if (isLoadingScale.value) return;

            if (window.browserWindow?.setAppScale) {
                const finalScale = await window.browserWindow.setAppScale(normalizedScale);
                if (finalScale !== normalizedScale) {
                    appScale.value = finalScale;
                    SESSION.set(appScaleStorageKey, finalScale);
                }
            }
        }
    );

    return {
        showDeuterocanonical,
        appScale,
    };
});
