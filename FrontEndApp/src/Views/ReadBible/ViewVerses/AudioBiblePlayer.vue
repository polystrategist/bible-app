<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import {
    NAlert,
    NButton,
    NInput,
    NInputGroup,
    NSelect,
    NSlider,
    NSwitch,
    NTag,
} from 'naive-ui';
import { useBibleStore } from '../../../store/BibleStore';
import { useAudioBibleStore } from '../../../store/audioBible';
import { bibleBooks } from '../../../util/books';

const bibleStore = useBibleStore();
const audioStore = useAudioBibleStore();
const showOptions = ref(false);
const showSourceConfig = ref(false);

watch(
    () => showOptions.value,
    (visible) => {
        if (!visible) {
            showSourceConfig.value = false;
        }
    }
);

const playbackRateOptions = [
    { label: '0.75x', value: 0.75 },
    { label: '1x', value: 1 },
    { label: '1.25x', value: 1.25 },
    { label: '1.5x', value: 1.5 },
];

const sourceModeOptions = [
    { label: 'Template', value: 'template' },
    { label: 'Direct URL', value: 'direct' },
];

function formatTime(seconds: number) {
    if (!Number.isFinite(seconds)) {
        return '00:00';
    }
    const total = Math.max(0, Math.floor(seconds));
    const mins = Math.floor(total / 60)
        .toString()
        .padStart(2, '0');
    const secs = (total % 60).toString().padStart(2, '0');
    return `${mins}:${secs}`;
}

const currentChapterLabel = computed(() => {
    return `${bibleStore.selectedBook.title} ${bibleStore.selectedChapter}`;
});

const chapterSelection = computed(() => {
    const bookId =
        bibleBooks.findIndex((book) => book.book_number === bibleStore.selectedBookNumber) + 1;

    return {
        bookNumber: bibleStore.selectedBookNumber,
        chapter: bibleStore.selectedChapter,
        bookShort: bibleStore.selectedBook.short_name,
        bookName: bibleStore.selectedBook.title,
        bookId: bookId > 0 ? bookId : 1,
    };
});

async function refreshForCurrentChapter() {
    await audioStore.loadChapterAudio(chapterSelection.value);
}

onMounted(async () => {
    audioStore.initialize();
    await refreshForCurrentChapter();
});

watch(
    () => [
        bibleStore.selectedBookNumber,
        bibleStore.selectedChapter,
        audioStore.isEnabled,
        audioStore.sourceMode,
        audioStore.sourceTemplate,
        audioStore.directSourceUrl,
    ],
    async () => {
        await refreshForCurrentChapter();
    }
);
</script>

<template>
    <div class="border-y border-gray-200 dark:border-dark-300 p-2 flex flex-col gap-2">
        <div class="flex items-center gap-2 flex-wrap">
            <NTag size="small" type="default">Audio Bible</NTag>
            <NSwitch v-model:value="audioStore.isEnabled">
                <template #checked>On</template>
                <template #unchecked>Off</template>
            </NSwitch>
            <NButton size="small" quaternary @click="showOptions = !showOptions">
                {{ showOptions ? 'Hide Options' : 'Show Options' }}
            </NButton>
            <NButton :disabled="!audioStore.isEnabled" size="small" @click="audioStore.seekBy(-15)">
                -15s
            </NButton>
            <NButton
                :disabled="!audioStore.isEnabled"
                size="small"
                type="primary"
                @click="audioStore.togglePlayback"
            >
                {{ audioStore.isPlaying ? 'Pause' : 'Play' }}
            </NButton>
            <NButton :disabled="!audioStore.isEnabled" size="small" @click="audioStore.seekBy(15)">
                +15s
            </NButton>
            <div class="text-xs opacity-80">{{ currentChapterLabel }}</div>
            <div class="text-xs opacity-70">
                {{ formatTime(audioStore.currentTime) }} / {{ formatTime(audioStore.duration) }}
            </div>
        </div>

        <template v-if="showOptions">
            <NInputGroup>
                <NSlider
                    :value="audioStore.currentTime"
                    :min="0"
                    :max="Math.max(audioStore.duration, 1)"
                    :disabled="!audioStore.isEnabled"
                    @update:value="(value: number) => audioStore.seekTo(value)"
                />
                <NSelect
                    v-model:value="audioStore.playbackRate"
                    class="max-w-100px"
                    :options="playbackRateOptions"
                    size="small"
                />
                <NButton size="small" tertiary @click="showSourceConfig = !showSourceConfig">
                    {{ showSourceConfig ? 'Hide Source' : 'Source' }}
                </NButton>
            </NInputGroup>

            <div
                v-if="showSourceConfig"
                class="grid grid-cols-1 md:grid-cols-[140px,1fr] gap-2 items-center"
            >
                <NSelect
                    v-model:value="audioStore.sourceMode"
                    :options="sourceModeOptions"
                    size="small"
                />
                <NInput
                    v-if="audioStore.sourceMode === 'template'"
                    v-model:value="audioStore.sourceTemplate"
                    size="small"
                    placeholder="https://host/audio/{bookId}/{chapterPadded}.mp3"
                />
                <NInput
                    v-else
                    v-model:value="audioStore.directSourceUrl"
                    size="small"
                    placeholder="https://host/audio/chapter.mp3"
                />
                <div class="md:col-span-2 text-xs opacity-70">
                    Template tokens: {bookId}, {bookNumber}, {chapter}, {chapterPadded}, {bookShort},
                    {bookName}
                </div>
                <div class="md:col-span-2">
                    <NSwitch v-model:value="audioStore.autoPlayOnChapterChange" size="small">
                        <template #checked>Auto play chapter change</template>
                        <template #unchecked>Auto play chapter change</template>
                    </NSwitch>
                </div>
            </div>
        </template>

        <NAlert
            v-if="showOptions && audioStore.errorMessage"
            type="warning"
            :show-icon="false"
            class="text-xs"
        >
            {{ audioStore.errorMessage }}
        </NAlert>
    </div>
</template>
