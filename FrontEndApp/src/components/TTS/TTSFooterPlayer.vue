<script lang="ts" setup>
import { computed } from 'vue';
import { NButton, NIcon, NSelect } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { useTTSStore } from '../../store/ttsStore';
import { useBibleStore } from '../../store/BibleStore';

const ttsStore = useTTSStore();
const bibleStore = useBibleStore();

const rateOptions = [
    { label: '0.5×', value: 0.5 },
    { label: '0.75×', value: 0.75 },
    { label: '1×', value: 1 },
    { label: '1.25×', value: 1.25 },
    { label: '1.5×', value: 1.5 },
    { label: '2×', value: 2 },
];

const currentVerse = computed(() => {
    const idx = ttsStore.currentVerseIndex;
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
    const raw = v.version[ttsStore.selectedVersionIndex]?.text ?? v.version[0]?.text ?? '';
    const tmp = document.createElement('div');
    tmp.innerHTML = raw;
    const text = tmp.textContent || tmp.innerText || '';
    return text.length > 60 ? text.slice(0, 60) + '…' : text;
});
</script>

<template>
    <div class="flex items-center gap-2 px-2 py-0.5 rounded-lg bg-[var(--primary-color)] bg-opacity-10 border border-[var(--primary-color)] border-opacity-30 max-w-600px w-full">
        <!-- Speaking icon -->
        <Icon icon="mdi:text-to-speech" class="text-[var(--primary-color)] flex-shrink-0" style="font-size: 16px;" />

        <!-- Verse label -->
        <span class="text-xs font-700 text-[var(--primary-color)] whitespace-nowrap flex-shrink-0">
            {{ verseLabel }}
        </span>

        <!-- Verse snippet -->
        <span class="text-xs opacity-60 truncate flex-1 min-w-0">{{ verseSnippet }}</span>

        <!-- Controls -->
        <div class="flex items-center gap-0.5 flex-shrink-0">
            <NButton size="tiny" quaternary circle title="Previous verse" @click="ttsStore.previous()">
                <Icon icon="mdi:skip-previous" style="font-size: 14px;" />
            </NButton>

            <NButton size="tiny" quaternary circle :title="ttsStore.isPlaying ? 'Pause' : 'Resume'" @click="ttsStore.togglePlayback()">
                <Icon :icon="ttsStore.isPlaying ? 'mdi:pause' : 'mdi:play'" style="font-size: 14px;" />
            </NButton>

            <NButton size="tiny" quaternary circle title="Next verse" @click="ttsStore.next()">
                <Icon icon="mdi:skip-next" style="font-size: 14px;" />
            </NButton>

            <NButton size="tiny" quaternary circle title="Stop" @click="ttsStore.stop()">
                <Icon icon="mdi:stop" style="font-size: 14px;" />
            </NButton>
        </div>

        <!-- Speed -->
        <NSelect
            :value="ttsStore.playbackRate"
            :options="rateOptions"
            size="tiny"
            style="width: 62px; flex-shrink: 0;"
            :consistent-menu-width="false"
            @update:value="ttsStore.setRate"
        />
    </div>
</template>
