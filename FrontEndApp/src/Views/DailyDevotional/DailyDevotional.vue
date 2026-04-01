<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { NSpin, NModal, NSteps, NStep } from 'naive-ui';
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
    { key: 'pause', label: 'Pause', icon: 'mdi:pause-circle-outline' },
    { key: 'listen', label: 'Listen', icon: 'mdi:ear-hearing' },
    { key: 'think', label: 'Think', icon: 'mdi:head-lightbulb-outline' },
    { key: 'pray', label: 'Pray', icon: 'mdi:hands-pray' },
    { key: 'go', label: 'Go', icon: 'mdi:arrow-right-circle-outline' },
] as const;

const devotional = ref<Devotional | null>(null);
const loading = ref(true);
const activeStep = ref(0);
const bibleStore = useBibleStore();

function hasVisibleText(html: string): boolean {
    return html.replace(/<[^>]*>/g, '').trim().length > 0;
}

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
                    .filter((v: any) => v.text && hasVisibleText(v.text))
                    .map((v: any) => ({
                        version: v.version.replace('.SQLite3', ''),
                        text: v.text,
                    }));
            }
        } else if (rows.length) {
            verseModalTexts.value = rows.flatMap((r: any) =>
                (r.version || [])
                    .filter((v: any) => v.text && hasVisibleText(v.text))
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
        <div class="devo-container">
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
                <!-- Header -->
                <div class="devo-header">
                    <p class="devo-date">{{ dateLabel }}</p>
                    <span class="devo-day-badge">Day {{ devotional.day_number }}</span>
                    <h1 class="devo-title">{{ devotional.title }}</h1>

                    <!-- Verse chips -->
                    <div v-if="devotional.verses?.length" class="devo-verses">
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
                </div>

                <!-- Step progress bar -->
                <NSteps :current="activeStep + 1" class="devo-steps" size="small">
                    <NStep
                        v-for="(step, i) in steps"
                        :key="step.key"
                        :title="step.label"
                        @click="activeStep = i"
                        style="cursor: pointer"
                    />
                </NSteps>

                <!-- Content area -->
                <div class="devo-content-area">
                    <div class="devo-content-accent" />
                    <div class="devo-content-inner">
                        <h3 class="devo-step-label">{{ steps[activeStep].label }}</h3>
                        <div class="devo-step-body" v-html="stepContent"></div>
                    </div>
                </div>

                <!-- Navigation -->
                <div class="devo-nav">
                    <button
                        v-if="activeStep > 0"
                        class="devo-nav-btn"
                        @click="prevStep"
                    >
                        <Icon icon="mdi:arrow-left" class="text-sm" />
                        Back
                    </button>
                    <span v-else />
                    <button
                        v-if="activeStep < steps.length - 1"
                        class="devo-nav-btn devo-nav-btn-primary"
                        @click="nextStep"
                    >
                        Next
                        <Icon icon="mdi:arrow-right" class="text-sm" />
                    </button>
                    <span v-else class="devo-finished">
                        <Icon icon="mdi:check-circle" class="text-[var(--primary-color)]" />
                        Completed
                    </span>
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

.devo-container {
    max-width: 640px;
    margin: 0 auto;
    padding: 32px 24px;
}

/* ---- Header ---- */
.devo-header {
    text-align: center;
    margin-bottom: 32px;
}

.devo-date {
    font-size: 12px;
    opacity: 0.4;
    margin-bottom: 8px;
}

.devo-day-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--primary-color);
    border: 1px solid color-mix(in srgb, var(--primary-color) 40%, transparent);
    margin-bottom: 10px;
}

.devo-title {
    font-size: 22px;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 14px;
}

.devo-verses {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    justify-content: center;
}

.verse-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 500;
    background: color-mix(in srgb, var(--primary-color) 10%, transparent);
    color: var(--primary-color);
    border: none;
    cursor: pointer;
    transition: all 0.15s;
}

.verse-chip:hover {
    background: color-mix(in srgb, var(--primary-color) 20%, transparent);
}

/* ---- Step Progress Track ---- */
.devo-steps {
    margin-bottom: 28px;
}

/* ---- Content Area ---- */
.devo-content-area {
    display: flex;
    gap: 0;
    margin-bottom: 20px;
}

.devo-content-accent {
    width: 3px;
    flex-shrink: 0;
    border-radius: 3px;
    background: var(--primary-color);
    opacity: 0.6;
}

.devo-content-inner {
    flex: 1;
    padding: 4px 0 4px 20px;
}

.devo-step-label {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--primary-color);
    margin-bottom: 14px;
    opacity: 0.8;
}

.devo-step-body {
    font-size: 15px;
    line-height: 1.8;
    opacity: 0.82;
}

.devo-step-body :deep(p) {
    margin-bottom: 14px;
}

.devo-step-body :deep(p:last-child) {
    margin-bottom: 0;
}

.devo-step-body :deep(em) {
    color: var(--primary-color);
    font-style: italic;
}

.devo-step-body :deep(.verse-ref) {
    display: block;
    text-align: right;
    font-size: 12px;
    opacity: 0.5;
    margin-top: 6px;
    font-style: italic;
}

/* ---- Navigation ---- */
.devo-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 8px;
    border-top: 1px solid rgba(128, 128, 128, 0.1);
}

.devo-nav-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: 8px;
    border: 1px solid rgba(128, 128, 128, 0.2);
    background: none;
    color: inherit;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    opacity: 0.6;
    transition: all 0.15s;
}

.devo-nav-btn:hover {
    opacity: 1;
    border-color: rgba(128, 128, 128, 0.4);
}

.devo-nav-btn-primary {
    background: var(--primary-color);
    border-color: var(--primary-color);
    color: white;
    opacity: 1;
}

.devo-nav-btn-primary:hover {
    opacity: 0.85;
    border-color: var(--primary-color);
}

.devo-finished {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 500;
    opacity: 0.6;
}

/* ---- Verse Preview Modal ---- */
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
    display: block;
}
</style>
