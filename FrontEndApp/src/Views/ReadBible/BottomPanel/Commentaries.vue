<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue';
import {
    NEmpty,
    NSpin,
    NScrollbar,
    NButton,
    NIcon,
    NModal,
    NCard,
    NRadioGroup,
    NRadioButton,
    NCheckbox,
    NCheckboxGroup,
} from 'naive-ui';
import { DocumentImport, ListChecked } from '@vicons/carbon';
import { useCommentaryStore, matchesVerse, formatEntryRange } from '../../../store/commentaryStore';
import { useBibleStore } from '../../../store/BibleStore';
import { bibleBooks } from '../../../util/books';
import CommentaryImport from './CommentaryImport.vue';

const commentaryStore = useCommentaryStore();
const bibleStore = useBibleStore();

const showImportModal = ref(false);
const showSelectorModal = ref(false);
const draftSelected = ref<string[]>([]);
const canImport = window.isElectron;

const selectedCount = computed(() => commentaryStore.selectedFiles.length);
const selectedTitles = computed(() =>
    commentaryStore.modules
        .filter((m) => commentaryStore.selectedFiles.includes(m.file))
        .map((m) => m.title)
        .join(', '),
);
const allSelected = computed(
    () =>
        commentaryStore.modules.length > 0 &&
        draftSelected.value.length === commentaryStore.modules.length,
);

function openSelector() {
    draftSelected.value = [...commentaryStore.selectedFiles];
    showSelectorModal.value = true;
}

function toggleAll() {
    draftSelected.value = allSelected.value ? [] : commentaryStore.modules.map((m) => m.file);
}

function applySelector() {
    onSelectionChange([...draftSelected.value]);
    showSelectorModal.value = false;
}

// Import lives inside the selector dialog: swap the selector out for the
// import modal so they don't stack.
function openImportFromSelector() {
    showSelectorModal.value = false;
    showImportModal.value = true;
}

function getBookShortName(book_number: number): string {
    const book = bibleBooks.find((b) => b.book_number === book_number);
    return book ? book.short_name : String(book_number);
}

const visibleGroups = computed(() =>
    commentaryStore.groups
        .map((group) => ({
            file: group.file,
            title: group.title,
            entries:
                commentaryStore.scope === 'chapter'
                    ? group.entries
                    : group.entries.filter((entry) => matchesVerse(entry, bibleStore.selectedVerse)),
        }))
        .filter((group) => group.entries.length > 0),
);

const hasModules = computed(() => commentaryStore.modules.length > 0);
const hasSelection = computed(() => commentaryStore.selectedFiles.length > 0);

async function load() {
    const { selectedBookNumber, selectedChapter } = bibleStore;
    if (selectedBookNumber && selectedChapter) {
        await commentaryStore.fetchForChapter(selectedBookNumber, selectedChapter);
    }
}

function onSelectionChange(files: string[]) {
    commentaryStore.setSelectedFiles(files);
    load();
}

// Commentary text can embed cross-reference links (rendered as
// `<span class="commentary-ref" data-book/-chapter/-verse>`). Delegate clicks
// on the text container so tapping a reference navigates to that verse.
function onCommentaryClick(event: MouseEvent) {
    const target = event.target as HTMLElement;
    const ref = target.closest?.('.commentary-ref') as HTMLElement | null;
    if (!ref) return;
    const book = Number(ref.dataset.book);
    const chapter = Number(ref.dataset.chapter);
    const verse = Number(ref.dataset.verse);
    if (book && chapter && verse) {
        bibleStore.selectVerse(book, chapter, verse);
    }
}

async function onImported(fileName: string) {
    showImportModal.value = false;
    await commentaryStore.loadModules();
    if (fileName) {
        const next = Array.from(new Set([...commentaryStore.selectedFiles, fileName]));
        commentaryStore.setSelectedFiles(next);
    }
    await commentaryStore.fetchForChapter(bibleStore.selectedBookNumber, bibleStore.selectedChapter);
}

watch(
    () => [bibleStore.selectedBookNumber, bibleStore.selectedChapter],
    () => load(),
);

onMounted(async () => {
    await commentaryStore.loadModules();
    await load();
});
</script>

<template>
    <div class="h-full flex flex-col p-2 gap-2">
        <!-- Header row 1: reference + selected list + scope -->
        <div class="flex items-center gap-3 shrink-0">
            <div class="text-xs text-gray-500 dark:text-gray-400 font-500 shrink-0">
                Commentaries for
                <span class="font-700 text-[var(--primary-color)]">
                    {{ getBookShortName(bibleStore.selectedBookNumber) }}
                    {{ bibleStore.selectedChapter
                    }}<template v-if="commentaryStore.scope === 'verse'">:{{ bibleStore.selectedVerse }}</template>
                </span>
            </div>

            <!-- Selected commentaries, comma-separated, ellipsized when they overflow -->
            <div
                class="flex-1 min-w-0 text-xs text-gray-400 dark:text-gray-500 truncate"
                :title="selectedTitles"
            >
                {{ selectedTitles }}
            </div>

            <div class="flex items-center gap-2 shrink-0">
                <NButton
                    v-if="hasModules"
                    size="small"
                    title="Choose which commentaries to show"
                    @click="openSelector"
                >
                    <template #icon>
                        <NIcon><ListChecked /></NIcon>
                    </template>
                    {{ selectedCount }} Selected
                </NButton>

                <NRadioGroup v-model:value="commentaryStore.scope" size="small">
                    <NRadioButton value="verse">Verse</NRadioButton>
                    <NRadioButton value="chapter">Chapter</NRadioButton>
                </NRadioGroup>
            </div>
        </div>

        <!-- Body -->
        <div class="flex-1 min-h-0 relative">
            <NScrollbar class="h-full">
                <NEmpty
                    v-if="!commentaryStore.isLoading && !hasModules"
                    description="No commentary installed."
                    size="small"
                    class="py-4"
                >
                    <template #extra>
                        <div class="flex flex-col items-center gap-2">
                            <span class="text-xs text-gray-400">
                                Import a commentary, or download a module that includes commentaries.
                            </span>
                            <NButton
                                v-if="canImport"
                                size="small"
                                type="primary"
                                secondary
                                @click="showImportModal = true"
                            >
                                <template #icon>
                                    <NIcon><DocumentImport /></NIcon>
                                </template>
                                Import Commentary
                            </NButton>
                        </div>
                    </template>
                </NEmpty>

                <NEmpty
                    v-else-if="!commentaryStore.isLoading && !hasSelection"
                    description="Select a commentary to display."
                    size="small"
                    class="py-4"
                />

                <NEmpty
                    v-else-if="!commentaryStore.isLoading && !visibleGroups.length"
                    :description="`No commentary for this ${commentaryStore.scope}.`"
                    size="small"
                    class="py-4"
                />

                <div class="flex flex-col gap-4 pr-1 pb-3" @click="onCommentaryClick">
                    <div v-for="group in visibleGroups" :key="group.file" class="flex flex-col gap-2">
                        <div
                            class="text-[10px] font-600 text-gray-400 dark:text-gray-500 uppercase tracking-wide"
                        >
                            {{ group.title }}
                        </div>

                        <div
                            v-for="(entry, index) in group.entries"
                            :key="`${group.file}-${index}`"
                            class="flex flex-col gap-1 rounded-md border border-gray-200 dark:border-dark-200 bg-gray-100/50 dark:bg-dark-400/40 p-2"
                        >
                            <div class="flex items-center gap-2">
                                <span
                                    v-if="entry.marker"
                                    class="commentary-marker inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-700 whitespace-nowrap"
                                >
                                    {{ entry.marker }}
                                </span>
                                <span class="text-[10px] font-600 text-gray-400 dark:text-gray-500">
                                    {{ formatEntryRange(entry) }}
                                </span>
                            </div>
                            <!-- Commentary text carries inline markup (<em>, <i>, cross-refs) -->
                            <div
                                class="commentary-text text-xs text-gray-700 dark:text-gray-300 leading-relaxed"
                                v-html="entry.text"
                            ></div>
                        </div>
                    </div>
                </div>
            </NScrollbar>

            <div
                v-if="commentaryStore.isLoading"
                class="absolute inset-0 flex items-center justify-center bg-white/60 dark:bg-dark-800/60"
            >
                <NSpin size="small" />
            </div>
        </div>

        <!-- Commentary selector dialog -->
        <NModal v-model:show="showSelectorModal">
            <NCard
                title="Select Commentaries"
                size="small"
                role="dialog"
                aria-modal="true"
                class="max-w-420px"
            >
                <template v-if="canImport" #header-extra>
                    <NButton
                        size="small"
                        type="primary"
                        secondary
                        title="Import a commentary module"
                        @click="openImportFromSelector"
                    >
                        <template #icon>
                            <NIcon><DocumentImport /></NIcon>
                        </template>
                        Import
                    </NButton>
                </template>

                <div class="flex flex-col gap-3">
                    <div class="flex items-center justify-between">
                        <span class="text-xs opacity-60">
                            {{ draftSelected.length }} of {{ commentaryStore.modules.length }} selected
                        </span>
                        <NButton size="tiny" quaternary @click="toggleAll">
                            {{ allSelected ? 'Clear all' : 'Select all' }}
                        </NButton>
                    </div>

                    <NCheckboxGroup v-model:value="draftSelected">
                        <div class="flex flex-col gap-2 max-h-300px overflow-y-auto pr-1">
                            <NCheckbox
                                v-for="m in commentaryStore.modules"
                                :key="m.file"
                                :value="m.file"
                                :label="m.title"
                            />
                        </div>
                    </NCheckboxGroup>

                    <div class="flex justify-end gap-2 mt-1">
                        <NButton size="small" @click="showSelectorModal = false">Cancel</NButton>
                        <NButton size="small" type="primary" @click="applySelector">Apply</NButton>
                    </div>
                </div>
            </NCard>
        </NModal>

        <!-- Import modal -->
        <NModal v-model:show="showImportModal">
            <NCard
                title="Import Commentary"
                size="small"
                role="dialog"
                aria-modal="true"
                class="max-w-460px"
            >
                <CommentaryImport @imported="onImported" @cancel="showImportModal = false" />
            </NCard>
        </NModal>
    </div>
</template>

<style scoped>
/* Outlined chip — avoids opacity-on-CSS-var (which renders solid and hides the
   label). Tinted background via color-mix where supported, transparent otherwise. */
.commentary-marker {
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
    background: color-mix(in srgb, var(--primary-color) 12%, transparent);
}

.commentary-text :deep(em),
.commentary-text :deep(i) {
    font-style: italic;
}

/* Cross-reference links inside commentary text. */
.commentary-text :deep(.commentary-ref) {
    color: var(--primary-color);
    cursor: pointer;
    font-weight: 600;
    text-decoration: none;
}

.commentary-text :deep(.commentary-ref:hover) {
    text-decoration: underline;
}
</style>
