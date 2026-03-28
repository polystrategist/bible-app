<script lang="ts" setup>
import { computed } from 'vue';
import { NButton, NSelect } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { useTTSStore } from '../../store/ttsStore';
import { usePiperTTSStore } from '../../store/piperTTSStore';
import { useSettingStore } from '../../store/settingStore';
import { useBibleStore } from '../../store/BibleStore';

const ttsStore = useTTSStore();
const piperStore = usePiperTTSStore();
const settingStore = useSettingStore();
const bibleStore = useBibleStore();

const rateOptions = [
    { label: '0.5×', value: 0.5 },
    { label: '0.75×', value: 0.75 },
    { label: '1×', value: 1 },
    { label: '1.25×', value: 1.25 },
    { label: '1.5×', value: 1.5 },
    { label: '2×', value: 2 },
];

// Use whichever store is active
const store = computed(() =>
    settingStore.verseReaderMode === 'piper-tts' ? piperStore : ttsStore
);

const currentVerse = computed(() => {
    const idx = store.value.currentVerseIndex;
    if (idx < 0) return null;
    return bibleStore.renderVerses[idx] ?? null;
});

const verseLabel = computed(() => {
    const v = currentVerse.value;
    if (!v) return '';
    return `${bibleStore.selectedBook.short_name} ${v.chapter}:${v.verse}`;
});

const verseSnippet = computed(() => {
    const v = currentVerse.value;
    if (!v) return '';
    const raw = v.version[store.value.selectedVersionIndex]?.text ?? v.version[0]?.text ?? '';
    const tmp = document.createElement('div');
    tmp.innerHTML = raw;
    const text = tmp.textContent || tmp.innerText || '';
    return text.length > 55 ? text.slice(0, 55) + '…' : text;
});
</script>

<template>
    <div
        class="flex items-center gap-3 px-3 py-1 rounded-full w-full max-w-580px"
        style="
            background: color-mix(in srgb, var(--primary-color) 18%, transparent);
            border: 1.5px solid color-mix(in srgb, var(--primary-color) 55%, transparent);
            box-shadow: 0 2px 12px color-mix(in srgb, var(--primary-color) 25%, transparent);
        "
    >
        <!-- Animated voice icon -->
        <Icon
            icon="mdi:account-voice"
            class="flex-shrink-0 text-[var(--primary-color)]"
            :class="store.isPlaying ? 'animate-pulse' : 'opacity-60'"
            style="font-size: 18px;"
        />

        <!-- Verse ref + snippet -->
        <div class="flex items-baseline gap-2 flex-1 min-w-0 overflow-hidden">
            <span class="text-xs font-700 text-[var(--primary-color)] whitespace-nowrap flex-shrink-0">
                {{ verseLabel }}
            </span>
            <span class="text-xs opacity-55 truncate">{{ verseSnippet }}</span>
        </div>

        <!-- Playback controls -->
        <div class="flex items-center gap-0 flex-shrink-0">
            <NButton size="tiny" quaternary circle title="Previous verse" @click="store.previous()">
                <Icon icon="mdi:skip-previous" style="font-size: 15px;" />
            </NButton>
            <NButton
                size="tiny"
                quaternary
                circle
                :title="store.isPlaying ? 'Pause' : 'Resume'"
                @click="store.togglePlayback()"
            >
                <Icon :icon="store.isPlaying ? 'mdi:pause' : 'mdi:play'" style="font-size: 15px;" />
            </NButton>
            <NButton size="tiny" quaternary circle title="Next verse" @click="store.next()">
                <Icon icon="mdi:skip-next" style="font-size: 15px;" />
            </NButton>
            <NButton size="tiny" quaternary circle title="Stop" @click="store.stop()">
                <Icon icon="mdi:stop" style="font-size: 15px;" />
            </NButton>
        </div>

        <!-- Speed -->
        <div class="flex items-center gap-1 flex-shrink-0">
            <span class="text-xs opacity-40">Speed</span>
            <NSelect
                :value="store.playbackRate"
                :options="rateOptions"
                size="tiny"
                style="width: 62px;"
                :consistent-menu-width="false"
                @update:value="store.setRate"
            />
        </div>
    </div>
</template>
