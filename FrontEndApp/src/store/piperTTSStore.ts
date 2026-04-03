import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useBibleStore } from './BibleStore';
import { useSettingStore } from './settingStore';

export const usePiperTTSStore = defineStore('piperTTSStore', () => {
    const isPlaying = ref(false);
    const isPaused = ref(false);
    const currentVerseIndex = ref(-1);
    const activeVerseNumber = ref<number | null>(null);
    const selectedVersionIndex = ref(0);
    const autoAdvancing = ref(false);
    const playbackRate = ref(1);

    // Install state
    const isInstalled = ref(false);
    const isInstalling = ref(false);
    const installStep = ref('');
    const installPercent = ref(0);
    const installError = ref('');

    const isActive = computed(() => isPlaying.value || isPaused.value);

    let audioContext: AudioContext | null = null;
    let currentSource: AudioBufferSourceNode | null = null;
    let stopped = false;
    let playTimeout: ReturnType<typeof setTimeout> | null = null;
    let playGeneration = 0;

    function stripHtml(html: string): string {
        const tmp = document.createElement('div');
        tmp.innerHTML = html;
        // Remove footnote elements before extracting text
        tmp.querySelectorAll('f, s').forEach((el) => el.remove());
        const text = tmp.textContent || tmp.innerText || '';
        return text.replace(/\[†?\d+(?:-\d+)?\]/g, '').replace(/\s+/g, ' ').trim();
    }

    async function checkInstalled() {
        try {
            const status = await window.browserWindow.piperStatus();
            isInstalled.value = status.binaryReady && status.modelReady;
        } catch {
            isInstalled.value = false;
        }
    }

    async function uninstall() {
        stop();
        try {
            const result = await window.browserWindow.piperUninstall();
            if (result.success) {
                isInstalled.value = false;
            }
        } catch {
            // ignore
        }
    }

    async function install() {
        isInstalling.value = true;
        installError.value = '';
        installStep.value = 'binary';
        installPercent.value = 0;

        window.browserWindow.piperOnInstallProgress((data) => {
            installStep.value = data.step;
            installPercent.value = data.percent;
        });

        try {
            const result = await window.browserWindow.piperInstall();
            if (result.success) {
                isInstalled.value = true;
                const settingStore = useSettingStore();
                if (result.modelName) settingStore.piperActiveModel = result.modelName;
            } else {
                installError.value = result.error ?? 'Installation failed';
            }
        } catch (err: any) {
            installError.value = err?.message ?? 'Installation failed';
        } finally {
            isInstalling.value = false;
        }
    }

    function getAudioContext(): AudioContext {
        if (!audioContext || audioContext.state === 'closed') {
            audioContext = new AudioContext();
        }
        return audioContext;
    }

    async function speakVerse(index: number, gen?: number) {
        const myGen = gen ?? playGeneration;
        if (myGen !== playGeneration || stopped) return;

        const bibleStore = useBibleStore();
        const verses = bibleStore.renderVerses;

        if (index >= verses.length) {
            const nextChapter = bibleStore.selectedChapter + 1;
            if (nextChapter <= bibleStore.selectedBook.chapter_count) {
                autoAdvancing.value = true;
                bibleStore.selectChapter(nextChapter).then(() => {
                    if (myGen !== playGeneration) return;
                    autoAdvancing.value = false;
                    speakVerse(0, myGen);
                });
            } else {
                stop();
            }
            return;
        }

        currentVerseIndex.value = index;
        const verse = verses[index];
        activeVerseNumber.value = verse.verse;

        try {
            bibleStore.setActiveVerse(verse.verse);
            bibleStore.AutoScrollSavedPosition(100);
        } catch { /* ignore */ }

        const rawText = verse.version[selectedVersionIndex.value]?.text ?? verse.version[0]?.text ?? '';
        const settingStore = useSettingStore();
        const text = settingStore.readVerseNumber
            ? `Verse ${verse.verse}. ${stripHtml(rawText)}`
            : stripHtml(rawText);

        try {
            const result = await window.browserWindow.piperSpeak(text, settingStore.piperActiveModel);
            if (!result.success || !result.wav || myGen !== playGeneration) return;

            const binary = atob(result.wav);
            const bytes = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);

            const ctx = getAudioContext();
            const audioBuffer = await ctx.decodeAudioData(bytes.buffer);

            if (myGen !== playGeneration) return;

            isPlaying.value = true;
            isPaused.value = false;

            const source = ctx.createBufferSource();
            source.buffer = audioBuffer;
            source.playbackRate.value = playbackRate.value;
            source.connect(ctx.destination);
            currentSource = source;

            source.onended = () => {
                if (myGen !== playGeneration || isPaused.value) return;
                speakVerse(index + 1, myGen);
            };

            source.start();
        } catch (err) {
            console.error('[Piper] audio error:', err);
            stop();
        }
    }

    function playFromVerse(verseIndex: number, versionIndex = 0) {
        const gen = ++playGeneration;
        stopped = false;
        selectedVersionIndex.value = versionIndex;
        stopAudio();
        if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }
        isPlaying.value = false;
        isPaused.value = false;

        playTimeout = setTimeout(() => {
            playTimeout = null;
            speakVerse(verseIndex, gen);
        }, 50);
    }

    function stopAudio() {
        try {
            currentSource?.stop();
        } catch { /* ignore */ }
        currentSource = null;
    }

    function pause() {
        if (!isPlaying.value || isPaused.value) return;
        try { audioContext?.suspend(); } catch { /* ignore */ }
        isPlaying.value = false;
        isPaused.value = true;
    }

    function resume() {
        if (!isPaused.value) return;
        try { audioContext?.resume(); } catch { /* ignore */ }
        isPlaying.value = true;
        isPaused.value = false;
    }

    function togglePlayback() {
        if (isPaused.value) resume();
        else if (isPlaying.value) pause();
    }

    function stop() {
        ++playGeneration;
        stopped = true;
        if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }
        stopAudio();
        isPlaying.value = false;
        isPaused.value = false;
        currentVerseIndex.value = -1;
        activeVerseNumber.value = null;
        selectedVersionIndex.value = 0;
        autoAdvancing.value = false;
    }

    function next() {
        const bibleStore = useBibleStore();
        const nextIndex = currentVerseIndex.value + 1;
        if (nextIndex < bibleStore.renderVerses.length) {
            stopped = false;
            stopAudio();
            setTimeout(() => speakVerse(nextIndex), 50);
        }
    }

    function previous() {
        const prevIndex = Math.max(0, currentVerseIndex.value - 1);
        stopped = false;
        stopAudio();
        setTimeout(() => speakVerse(prevIndex), 50);
    }

    function setRate(rate: number) {
        playbackRate.value = rate;
        if (currentSource) {
            currentSource.playbackRate.value = rate;
        }
    }

    return {
        isPlaying,
        isPaused,
        isActive,
        currentVerseIndex,
        activeVerseNumber,
        selectedVersionIndex,
        autoAdvancing,
        playbackRate,
        isInstalled,
        isInstalling,
        installStep,
        installPercent,
        installError,
        checkInstalled,
        install,
        uninstall,
        playFromVerse,
        pause,
        resume,
        togglePlayback,
        stop,
        next,
        previous,
        setRate,
    };
});
