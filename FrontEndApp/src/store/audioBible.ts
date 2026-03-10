import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import SESSION from '../util/session';

const storageAudioBibleSettings = 'audio-bible-settings';
const storageAudioBiblePositions = 'audio-bible-positions';

type SourceMode = 'template' | 'direct';

type ChapterSelection = {
    bookNumber: number;
    chapter: number;
    bookShort: string;
    bookName: string;
    bookId: number;
};

export const useAudioBibleStore = defineStore('audioBibleStore', () => {
    const isEnabled = ref(false);
    const sourceMode = ref<SourceMode>('template');
    const sourceTemplate = ref('');
    const directSourceUrl = ref('');
    const autoPlayOnChapterChange = ref(false);
    const playbackRate = ref(1);

    const currentSource = ref('');
    const currentChapterKey = ref('');
    const isPlaying = ref(false);
    const currentTime = ref(0);
    const duration = ref(0);
    const errorMessage = ref('');

    const chapterPositions = ref<Record<string, number>>({});

    let audioEl: HTMLAudioElement | null = null;
    let isInitialized = false;

    function getChapterKey(selection: ChapterSelection) {
        return `${selection.bookNumber}_${selection.chapter}`;
    }

    function formatTemplateValue(value: string) {
        return encodeURIComponent(value.trim());
    }

    function resolveSourceFromSelection(selection: ChapterSelection) {
        if (sourceMode.value === 'direct') {
            return directSourceUrl.value.trim();
        }

        const template = sourceTemplate.value.trim();
        if (!template) {
            return '';
        }

        return template
            .replaceAll('{bookNumber}', String(selection.bookNumber))
            .replaceAll('{bookId}', String(selection.bookId))
            .replaceAll('{chapter}', String(selection.chapter))
            .replaceAll('{chapterPadded}', String(selection.chapter).padStart(2, '0'))
            .replaceAll('{bookShort}', formatTemplateValue(selection.bookShort))
            .replaceAll('{bookName}', formatTemplateValue(selection.bookName));
    }

    function persistSettings() {
        SESSION.set(storageAudioBibleSettings, {
            isEnabled: isEnabled.value,
            sourceMode: sourceMode.value,
            sourceTemplate: sourceTemplate.value,
            directSourceUrl: directSourceUrl.value,
            autoPlayOnChapterChange: autoPlayOnChapterChange.value,
            playbackRate: playbackRate.value,
        });
    }

    function persistPositions() {
        SESSION.set(storageAudioBiblePositions, chapterPositions.value);
    }

    function ensureAudioElement() {
        if (audioEl) {
            return audioEl;
        }

        audioEl = new Audio();
        audioEl.preload = 'metadata';

        audioEl.addEventListener('timeupdate', () => {
            if (!audioEl) {
                return;
            }
            currentTime.value = audioEl.currentTime || 0;
            duration.value = Number.isFinite(audioEl.duration) ? audioEl.duration : 0;
            if (currentChapterKey.value) {
                chapterPositions.value[currentChapterKey.value] = currentTime.value;
            }
        });

        audioEl.addEventListener('loadedmetadata', () => {
            if (!audioEl) {
                return;
            }
            duration.value = Number.isFinite(audioEl.duration) ? audioEl.duration : 0;
            if (currentChapterKey.value && chapterPositions.value[currentChapterKey.value]) {
                audioEl.currentTime = chapterPositions.value[currentChapterKey.value];
            }
        });

        audioEl.addEventListener('play', () => {
            isPlaying.value = true;
            errorMessage.value = '';
        });

        audioEl.addEventListener('pause', () => {
            isPlaying.value = false;
            persistPositions();
        });

        audioEl.addEventListener('ended', () => {
            isPlaying.value = false;
            persistPositions();
        });

        audioEl.addEventListener('error', () => {
            errorMessage.value = 'Unable to play this audio source.';
            isPlaying.value = false;
        });

        return audioEl;
    }

    function initialize() {
        if (isInitialized) {
            return;
        }

        const storedSettings = SESSION.get(storageAudioBibleSettings);
        if (storedSettings) {
            isEnabled.value = !!storedSettings.isEnabled;
            sourceMode.value = storedSettings.sourceMode || 'template';
            sourceTemplate.value = storedSettings.sourceTemplate || '';
            directSourceUrl.value = storedSettings.directSourceUrl || '';
            autoPlayOnChapterChange.value = !!storedSettings.autoPlayOnChapterChange;
            playbackRate.value = Number(storedSettings.playbackRate) || 1;
        }

        const storedPositions = SESSION.get(storageAudioBiblePositions);
        if (storedPositions && typeof storedPositions === 'object') {
            chapterPositions.value = storedPositions;
        }

        ensureAudioElement().playbackRate = playbackRate.value;

        watch(
            [isEnabled, sourceMode, sourceTemplate, directSourceUrl, autoPlayOnChapterChange, playbackRate],
            () => {
                persistSettings();
                if (audioEl) {
                    audioEl.playbackRate = playbackRate.value;
                }
            },
            { deep: false }
        );

        isInitialized = true;
    }

    async function play() {
        const el = ensureAudioElement();
        if (!el.src) {
            errorMessage.value = 'No audio source loaded for this chapter.';
            return false;
        }

        try {
            await el.play();
            return true;
        } catch (error) {
            errorMessage.value = 'Playback was blocked. Click play again after interacting with the page.';
            return false;
        }
    }

    function pause() {
        const el = ensureAudioElement();
        el.pause();
    }

    async function togglePlayback() {
        if (isPlaying.value) {
            pause();
            return false;
        }

        return play();
    }

    function seekTo(seconds: number) {
        const el = ensureAudioElement();
        const safeTarget = Math.min(Math.max(seconds, 0), duration.value || 0);
        el.currentTime = safeTarget;
        currentTime.value = safeTarget;
        if (currentChapterKey.value) {
            chapterPositions.value[currentChapterKey.value] = safeTarget;
            persistPositions();
        }
    }

    function seekBy(offsetSeconds: number) {
        seekTo(currentTime.value + offsetSeconds);
    }

    async function loadChapterAudio(selection: ChapterSelection) {
        const el = ensureAudioElement();
        currentChapterKey.value = getChapterKey(selection);

        if (!isEnabled.value) {
            return false;
        }

        const resolvedSource = resolveSourceFromSelection(selection);
        if (!resolvedSource) {
            errorMessage.value = 'Set an audio URL or URL template to start playback.';
            return false;
        }

        const hasSourceChanged = currentSource.value !== resolvedSource;
        currentSource.value = resolvedSource;

        if (hasSourceChanged) {
            const shouldAutoPlay = autoPlayOnChapterChange.value;
            el.src = resolvedSource;
            el.load();
            currentTime.value = chapterPositions.value[currentChapterKey.value] || 0;

            if (shouldAutoPlay) {
                await play();
            } else {
                pause();
            }
        }

        return true;
    }

    return {
        initialize,
        isEnabled,
        sourceMode,
        sourceTemplate,
        directSourceUrl,
        autoPlayOnChapterChange,
        playbackRate,
        currentSource,
        currentTime,
        duration,
        isPlaying,
        errorMessage,
        chapterPositions,
        play,
        pause,
        togglePlayback,
        seekTo,
        seekBy,
        loadChapterAudio,
    };
});
