import { defineStore } from 'pinia';
import { ref, computed, watch } from 'vue';
import { useBibleStore } from './BibleStore';
import { useSettingStore } from './settingStore';

export const useTTSStore = defineStore('ttsStore', () => {
    const isPlaying = ref(false);
    const isPaused = ref(false);
    const currentVerseIndex = ref(-1);
    const activeVerseNumber = ref<number | null>(null);
    const playbackRate = ref(1);
    const selectedVersionIndex = ref(0);
    const autoAdvancing = ref(false);
    const voices = ref<SpeechSynthesisVoice[]>([]);
    const selectedVoiceURI = ref('');

    let keepAliveInterval: ReturnType<typeof setInterval> | null = null;
    let initialized = false;

    const isActive = computed(() => isPlaying.value || isPaused.value);

    const voiceOptions = computed(() =>
        voices.value.map((v) => ({ label: v.name, value: v.voiceURI }))
    );

    function stripHtml(html: string): string {
        const tmp = document.createElement('div');
        tmp.innerHTML = html;
        const text = tmp.textContent || tmp.innerText || '';
        // Remove footnote/cross-reference markers like [5], [16], etc.
        return text.replace(/\[\d+\]/g, '');
    }

    function loadVoices() {
        try {
            const all = window.speechSynthesis.getVoices();
            if (all.length > 0) {
                voices.value = all;
                if (!selectedVoiceURI.value) {
                    const english = all.find((v) => v.lang.startsWith('en'));
                    selectedVoiceURI.value = (english ?? all[0]).voiceURI;
                }
            }
        } catch {
            // speechSynthesis not available
        }
    }

    function ensureInitialized() {
        if (initialized) return;
        initialized = true;
        try {
            loadVoices();
            window.speechSynthesis.onvoiceschanged = loadVoices;
        } catch {
            // not available
        }

        // Watch for chapter load after auto-advance
        const bibleStore = useBibleStore();
        watch(
            () => bibleStore.renderVerses,
            (verses) => {
                if (autoAdvancing.value && verses.length > 0) {
                    autoAdvancing.value = false;
                    setTimeout(() => {
                        startKeepAlive();
                        speakVerse(0);
                    }, 100);
                }
            }
        );
    }

    function getSelectedVoice(): SpeechSynthesisVoice | null {
        return voices.value.find((v) => v.voiceURI === selectedVoiceURI.value) ?? null;
    }

    // Chrome/Electron silently pauses speechSynthesis when the window loses focus.
    // Resume every 10s to keep it alive.
    function startKeepAlive() {
        if (keepAliveInterval) return;
        keepAliveInterval = setInterval(() => {
            try {
                if (window.speechSynthesis.speaking && window.speechSynthesis.paused) {
                    window.speechSynthesis.resume();
                }
            } catch { /* ignore */ }
        }, 10_000);
    }

    function stopKeepAlive() {
        if (keepAliveInterval) {
            clearInterval(keepAliveInterval);
            keepAliveInterval = null;
        }
    }

    function speakVerse(index: number) {
        const bibleStore = useBibleStore();
        const verses = bibleStore.renderVerses;

        if (index >= verses.length) {
            // Try to advance to the next chapter
            const nextChapter = bibleStore.selectedChapter + 1;
            if (nextChapter <= bibleStore.selectedBook.chapter_count) {
                autoAdvancing.value = true;
                bibleStore.selectChapter(nextChapter);
            } else {
                // End of book
                isPlaying.value = false;
                isPaused.value = false;
                activeVerseNumber.value = null;
                currentVerseIndex.value = -1;
                stopKeepAlive();
            }
            return;
        }

        currentVerseIndex.value = index;
        const verse = verses[index];
        activeVerseNumber.value = verse.verse;

        // Select and scroll to the verse being read
        try {
            bibleStore.selectVerse(verse.book_number, verse.chapter, verse.verse);
            bibleStore.AutoScrollSavedPosition(100);
        } catch { /* ignore */ }

        const rawText = verse.version[selectedVersionIndex.value]?.text ?? verse.version[0]?.text ?? '';
        const settingStore = useSettingStore();
        const text = settingStore.readVerseNumber
            ? `Verse ${verse.verse}. ${stripHtml(rawText)}`
            : stripHtml(rawText);

        try {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = playbackRate.value;

            const voice = getSelectedVoice();
            if (voice) utterance.voice = voice;

            utterance.onstart = () => {
                isPlaying.value = true;
                isPaused.value = false;
            };

            utterance.onend = () => {
                speakVerse(index + 1);
            };

            utterance.onerror = (e) => {
                if (e.error === 'interrupted' || e.error === 'canceled') return;
                console.error('[TTS] Error:', e.error);
                isPlaying.value = false;
                isPaused.value = false;
                activeVerseNumber.value = null;
                stopKeepAlive();
            };

            window.speechSynthesis.speak(utterance);
        } catch (err) {
            console.error('[TTS] Failed to speak:', err);
            isPlaying.value = false;
            stopKeepAlive();
        }
    }

    function playFromVerse(verseIndex: number, versionIndex = 0) {
        ensureInitialized();
        selectedVersionIndex.value = versionIndex;
        try { window.speechSynthesis.cancel(); } catch { /* ignore */ }
        stopKeepAlive();
        isPlaying.value = false;
        isPaused.value = false;

        setTimeout(() => {
            startKeepAlive();
            speakVerse(verseIndex);
        }, 50);
    }

    function pause() {
        if (!isPlaying.value || isPaused.value) return;
        try { window.speechSynthesis.pause(); } catch { /* ignore */ }
        isPlaying.value = false;
        isPaused.value = true;
    }

    function resume() {
        if (!isPaused.value) return;
        try { window.speechSynthesis.resume(); } catch { /* ignore */ }
        isPlaying.value = true;
        isPaused.value = false;
    }

    function togglePlayback() {
        if (isPaused.value) resume();
        else if (isPlaying.value) pause();
    }

    function stop() {
        try { window.speechSynthesis.cancel(); } catch { /* ignore */ }
        isPlaying.value = false;
        isPaused.value = false;
        currentVerseIndex.value = -1;
        activeVerseNumber.value = null;
        selectedVersionIndex.value = 0;
        autoAdvancing.value = false;
        stopKeepAlive();
    }

    function next() {
        const bibleStore = useBibleStore();
        const nextIndex = currentVerseIndex.value + 1;
        if (nextIndex < bibleStore.renderVerses.length) {
            try { window.speechSynthesis.cancel(); } catch { /* ignore */ }
            setTimeout(() => speakVerse(nextIndex), 50);
        }
    }

    function previous() {
        const prevIndex = Math.max(0, currentVerseIndex.value - 1);
        try { window.speechSynthesis.cancel(); } catch { /* ignore */ }
        setTimeout(() => speakVerse(prevIndex), 50);
    }

    function setRate(rate: number) {
        playbackRate.value = rate;
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
        voices,
        voiceOptions,
        selectedVoiceURI,
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
