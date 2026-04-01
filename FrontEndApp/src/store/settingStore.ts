import { defineStore } from 'pinia';
import { onMounted, ref, watch } from 'vue';
import SESSION from '../util/session';

export const useSettingStore = defineStore('settingStore', () => {
    const showDeuterocanonicalStorageKey = 'show-deuterocanonical';
    const appScaleStorageKey = 'app-scale';
    const verseReaderModeKey = 'verse-reader-mode';
    const piperActiveModelKey = 'piper-active-model';
    const readVerseNumberKey = 'read-verse-number';
    const showLeftSidebarKey = 'show-left-sidebar';
    const showRightSidebarKey = 'show-right-sidebar';
    const showDeuterocanonical = ref(false);
    const appScale = ref(1);
    const isLoadingScale = ref(false);
    const verseReaderMode = ref<string>('browser-tts');
    const piperActiveModel = ref<string>('en_US-ryan-high');
    const readVerseNumber = ref<boolean>(true);
    const showLeftSidebar = ref(true);
    const showRightSidebar = ref(true);

    onMounted(() => {
        const showDeuterocanonicalStored = SESSION.get(showDeuterocanonicalStorageKey);
        if (showDeuterocanonicalStored) showDeuterocanonical.value = showDeuterocanonicalStored;
        else SESSION.set(showDeuterocanonicalStorageKey, showDeuterocanonical.value);

        const savedVerseReaderMode = SESSION.get(verseReaderModeKey);
        if (savedVerseReaderMode) verseReaderMode.value = savedVerseReaderMode;

        const savedPiperModel = SESSION.get(piperActiveModelKey);
        if (savedPiperModel) piperActiveModel.value = savedPiperModel;

        const savedReadVerseNumber = SESSION.get(readVerseNumberKey);
        if (savedReadVerseNumber !== null && savedReadVerseNumber !== undefined)
            readVerseNumber.value = savedReadVerseNumber === true || savedReadVerseNumber === 'true';

        const savedShowLeft = SESSION.get(showLeftSidebarKey);
        if (savedShowLeft !== null && savedShowLeft !== undefined)
            showLeftSidebar.value = savedShowLeft !== false && savedShowLeft !== 'false';

        const savedShowRight = SESSION.get(showRightSidebarKey);
        if (savedShowRight !== null && savedShowRight !== undefined)
            showRightSidebar.value = savedShowRight !== false && savedShowRight !== 'false';

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

    watch(
        () => verseReaderMode.value,
        (val) => SESSION.set(verseReaderModeKey, val)
    );

    watch(
        () => piperActiveModel.value,
        (val) => SESSION.set(piperActiveModelKey, val)
    );

    watch(
        () => readVerseNumber.value,
        (val) => SESSION.set(readVerseNumberKey, val)
    );

    watch(
        () => showLeftSidebar.value,
        (val) => SESSION.set(showLeftSidebarKey, val)
    );

    watch(
        () => showRightSidebar.value,
        (val) => SESSION.set(showRightSidebarKey, val)
    );

    return {
        showDeuterocanonical,
        appScale,
        verseReaderMode,
        piperActiveModel,
        readVerseNumber,
        showLeftSidebar,
        showRightSidebar,
    };
});
