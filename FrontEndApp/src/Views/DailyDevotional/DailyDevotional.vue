<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { NSpin, NModal, NCard } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { useBibleStore } from '../../store/BibleStore';
import { bibleBooks } from '../../util/books';
import { getBibleService } from '../../services/BibleService';

interface Devotional {
    id: number;
    title: string;
    day_number: number;
    pause: string;
    listen: string;
    think: string;
    pray: string;
    go_action: string;
    verses: string[];
}

const steps = [
    { key: 'pause', label: 'Pause', color: '#7c5cbf', icon: 'mdi:meditation' },
    { key: 'listen', label: 'Listen', color: '#a08090', icon: 'mdi:ear-hearing' },
    { key: 'think', label: 'Think', color: '#d48a9a', icon: 'mdi:head-lightbulb-outline' },
    { key: 'pray', label: 'Pray', color: '#3db8b0', icon: 'mdi:hands-pray' },
    { key: 'go', label: 'Go', color: '#f0c040', icon: 'mdi:run-fast' },
] as const;

const devotional = ref<Devotional | null>(null);
const loading = ref(true);
const activeStep = ref(0);
const bibleStore = useBibleStore();

// Verse preview modal
const showVerseModal = ref(false);
const verseModalTitle = ref('');
const verseModalLoading = ref(false);
const verseModalTexts = ref<Array<{ version: string; text: string }>>([]);

const today = new Date();
const dateLabel = today.toLocaleDateString(undefined, {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
});

const activeColor = computed(() => steps[activeStep.value].color);

const stepContent = computed(() => {
    if (!devotional.value) return '';
    const d = devotional.value;
    const keys: Record<string, string> = {
        pause: d.pause,
        listen: d.listen,
        think: d.think,
        pray: d.pray,
        go: d.go_action,
    };
    return keys[steps[activeStep.value].key] || '';
});

const stepLabel = computed(() => steps[activeStep.value].label.toLowerCase());

function nextStep() {
    if (activeStep.value < steps.length - 1) {
        activeStep.value++;
    }
}

function prevStep() {
    if (activeStep.value > 0) {
        activeStep.value--;
    }
}

async function openVersePreview(verseRef: string) {
    const parts = verseRef.split(':');
    if (parts.length < 2) return;
    const bookName = parts[0].replace(/_/g, ' ');
    const chapter = parseInt(parts[1]);
    const verseNum = parts[2] ? parseInt(parts[2]) : null;

    const book = bibleBooks.find(
        (b) =>
            b.title.toLowerCase() === bookName.toLowerCase() ||
            b.short_name.toLowerCase() === bookName.toLowerCase()
    );
    if (!book) return;

    verseModalTitle.value = verseRef.replace(/:/g, ' ');
    verseModalTexts.value = [];
    verseModalLoading.value = true;
    showVerseModal.value = true;

    try {
        const bibleService = getBibleService();
        const rows = await bibleService.getVerses({
            bible_versions: bibleStore.selectedBibleVersions,
            book_number: book.book_number,
            selected_chapter: chapter,
        });

        if (verseNum && rows.length) {
            const row = rows.find((r: any) => r.verse === verseNum);
            if (row) {
                verseModalTexts.value = (row.version || [])
                    .filter((v: any) => v.text && v.text.trim())
                    .map((v: any) => ({
                        version: v.version.replace('.SQLite3', ''),
                        text: v.text,
                    }));
            }
        } else if (rows.length) {
            verseModalTexts.value = rows.flatMap((r: any) =>
                (r.version || [])
                    .filter((v: any) => v.text && v.text.trim())
                    .map((v: any) => ({
                        version: `${v.version.replace('.SQLite3', '')} — v${r.verse}`,
                        text: v.text,
                    }))
            );
        }
    } finally {
        verseModalLoading.value = false;
    }
}

onMounted(async () => {
    try {
        devotional.value = await (window as any).browserWindow.getTodayDevotional();
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="daily-devotional h-full overflow-auto">
        <div class="max-w-2xl mx-auto px-6 py-8">
            <!-- Header -->
            <div class="mb-6 text-center">
                <h2 class="text-lg font-semibold opacity-80 mb-1">Daily Devotional &amp; Reflection</h2>
                <p class="text-xs opacity-40">{{ dateLabel }}</p>
            </div>

            <!-- Loading -->
            <div v-if="loading" class="flex justify-center py-20">
                <NSpin size="medium" />
            </div>

            <!-- No content -->
            <div v-else-if="!devotional" class="text-center opacity-50 py-20">
                <Icon icon="mdi:book-off-outline" class="text-5xl mb-3" />
                <p>No devotional found for today.</p>
            </div>

            <template v-else>
                <!-- Title + Day -->
                <div class="text-center mb-6">
                    <span class="devotional-day-badge">Day {{ devotional.day_number }}</span>
                    <h1 class="text-xl font-bold mt-3 leading-snug">{{ devotional.title }}</h1>
                </div>

                <!-- Verse chips -->
                <div
                    v-if="devotional.verses?.length"
                    class="flex flex-wrap gap-2 justify-center mb-6"
                >
                    <button
                        v-for="verse in devotional.verses"
                        :key="verse"
                        class="verse-chip"
                        :title="`Read ${verse.replace(/:/g, ' ')}`"
                        @click="openVersePreview(verse)"
                    >
                        <Icon icon="mdi:book-open-variant" class="text-xs" />
                        {{ verse.replace(/:/g, ' ') }}
                    </button>
                </div>

                <!-- Step circles -->
                <div class="step-circles">
                    <button
                        v-for="(step, i) in steps"
                        :key="step.key"
                        class="step-circle"
                        :class="{ active: activeStep === i, visited: i < activeStep }"
                        :style="{
                            background: step.color,
                            borderColor: activeStep === i ? step.color : 'transparent',
                        }"
                        @click="activeStep = i"
                    >
                        {{ step.label }}
                    </button>
                </div>

                <!-- Step content card -->
                <div class="step-card" :style="{ background: activeColor }">
                    <h3 class="step-card-label">{{ stepLabel }}</h3>
                    <div class="step-card-body" v-html="stepContent"></div>

                    <!-- Navigation -->
                    <div class="step-card-nav">
                        <button
                            v-if="activeStep > 0"
                            class="step-nav-btn"
                            @click="prevStep"
                        >
                            Back
                        </button>
                        <span v-else></span>
                        <button
                            v-if="activeStep < steps.length - 1"
                            class="step-nav-btn"
                            @click="nextStep"
                        >
                            Next
                        </button>
                    </div>
                </div>
            </template>
        </div>

        <!-- Verse Preview Modal -->
        <NModal v-model:show="showVerseModal" preset="card" class="verse-preview-modal" :style="{ maxWidth: '520px' }">
            <template #header>
                <div class="flex items-center gap-2">
                    <Icon icon="mdi:book-open-page-variant" class="text-[var(--primary-color)]" />
                    <span>{{ verseModalTitle }}</span>
                </div>
            </template>
            <div v-if="verseModalLoading" class="flex justify-center py-8">
                <NSpin size="small" />
            </div>
            <div v-else-if="verseModalTexts.length === 0" class="text-center opacity-50 py-6">
                Verse not found in your current Bible version.
            </div>
            <div v-else class="verse-preview-list">
                <div
                    v-for="(item, i) in verseModalTexts"
                    :key="i"
                    class="verse-preview-item"
                >
                    <div class="verse-preview-version">{{ item.version }}</div>
                    <div class="verse-preview-text" v-html="item.text"></div>
                </div>
            </div>
        </NModal>
    </div>
</template>

<style scoped>
.daily-devotional {
    font-family: var(--bible-font-family, 'Poppins'), sans-serif;
}

.devotional-day-badge {
    display: inline-flex;
    padding: 3px 12px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
    opacity: 0.8;
}

.verse-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    background: color-mix(in srgb, var(--primary-color) 12%, transparent);
    color: var(--primary-color);
    border: none;
    cursor: pointer;
    transition: opacity 0.15s;
}

.verse-chip:hover {
    opacity: 0.75;
}

/* Step circles row */
.step-circles {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-bottom: 20px;
}

.step-circle {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    border: 3px solid transparent;
    color: white;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    outline: none;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.6;
}

.step-circle.active {
    opacity: 1;
    transform: scale(1.12);
    border-color: currentColor !important;
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.15);
}

.step-circle.visited {
    opacity: 0.85;
}

/* Step content card */
.step-card {
    border-radius: 16px;
    padding: 28px 28px 20px;
    min-height: 280px;
    color: white;
    display: flex;
    flex-direction: column;
    transition: background 0.3s ease;
}

.step-card-label {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 16px;
    opacity: 0.95;
}

.step-card-body {
    flex: 1;
    font-size: 15px;
    line-height: 1.75;
    opacity: 0.92;
}

.step-card-body :deep(p) {
    margin-bottom: 14px;
}

.step-card-body :deep(em) {
    font-style: italic;
}

.step-card-body :deep(blockquote) {
    border-left: 3px solid rgba(255, 255, 255, 0.4);
    padding-left: 14px;
    margin: 12px 0;
    font-style: italic;
    opacity: 0.9;
}

.step-card-body :deep(.verse-ref) {
    display: block;
    text-align: right;
    font-size: 13px;
    opacity: 0.7;
    margin-top: 8px;
}

/* Navigation buttons */
.step-card-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
}

.step-nav-btn {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    border-radius: 20px;
    padding: 8px 22px;
    color: white;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
}

.step-nav-btn:hover {
    background: rgba(255, 255, 255, 0.3);
}

/* Verse preview modal */
.verse-preview-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.verse-preview-item {
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(128, 128, 128, 0.15);
}

.verse-preview-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.verse-preview-version {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--primary-color);
    margin-bottom: 6px;
    opacity: 0.85;
}

.verse-preview-text {
    font-size: 15px;
    line-height: 1.75;
    opacity: 0.9;
}

.verse-preview-text :deep(f) {
    display: none;
}

.verse-preview-text :deep(pb) {
    display: none;
}
</style>
