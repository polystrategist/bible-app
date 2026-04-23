<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { NEmpty, NSpin, NScrollbar, NPopover, NSkeleton, NButton } from 'naive-ui';
import { useCrossReferencesStore } from '../../../store/crossReferencesStore';
import { useBibleStore } from '../../../store/BibleStore';
import { useModuleStore } from '../../../store/moduleStore';
import { bibleBooks } from '../../../util/books';

const crossRefStore = useCrossReferencesStore();
const bibleStore = useBibleStore();
const moduleStore = useModuleStore();

type VerseTextResult = { version: string; text: string };
const popoverTexts = ref<VerseTextResult[]>([]);
const popoverLoading = ref(false);
const activePopoverIndex = ref<number | null>(null);

function getBookShortName(book_number: number): string {
    const book = bibleBooks.find((b) => b.book_number === book_number);
    return book ? book.short_name : String(book_number);
}

function formatRef(toBook: number, toChapter: number, toVerseStart: number, toVerseEnd: number) {
    const bookName = getBookShortName(toBook);
    const verseRange = toVerseEnd !== toVerseStart ? `${toVerseStart}-${toVerseEnd}` : String(toVerseStart);
    return `${bookName} ${toChapter}:${verseRange}`;
}

function getVersionTitle(fileName: string): string {
    const found = moduleStore.bibleLists.find((b: any) => b.file_name === fileName);
    return found ? found.title : fileName.replace('.SQLite3', '');
}

async function navigateTo(book_number: number, chapter: number, verse: number) {
    activePopoverIndex.value = null;
    await bibleStore.selectVerse(book_number, chapter, verse);
}

async function onPopoverShow(ref: { to_book: number; to_chapter: number; to_verse_start: number }) {
    popoverTexts.value = [];
    popoverLoading.value = true;
    try {
        popoverTexts.value = await window.browserWindow.getVerseText({
            bible_versions: [...bibleStore.selectedBibleVersions],
            book_number: ref.to_book,
            chapter: ref.to_chapter,
            verse: ref.to_verse_start,
        });
    } catch (e) {
        console.error('getVerseText failed:', e);
    } finally {
        popoverLoading.value = false;
    }
}

async function load() {
    const { selectedBookNumber, selectedChapter, selectedVerse } = bibleStore;
    if (selectedBookNumber && selectedChapter && selectedVerse) {
        await crossRefStore.fetchReferences(selectedBookNumber, selectedChapter, selectedVerse);
    }
}

watch(
    () => [bibleStore.selectedBookNumber, bibleStore.selectedChapter, bibleStore.selectedVerse],
    () => load(),
);

onMounted(() => load());
</script>

<template>
    <div class="h-full flex flex-col p-2 gap-2">
        <div class="text-xs text-gray-500 dark:text-gray-400 font-500 shrink-0">
            Cross References for
            <span class="font-700 text-[var(--primary-color)]">
                {{ getBookShortName(bibleStore.selectedBookNumber) }}
                {{ bibleStore.selectedChapter }}:{{ bibleStore.selectedVerse }}
            </span>
        </div>

        <NSpin :show="crossRefStore.isLoading" class="flex-1 min-h-0">
            <NScrollbar class="h-full">
                <NEmpty
                    v-if="!crossRefStore.isLoading && !crossRefStore.references.length"
                    description="No cross references found"
                    size="small"
                    class="py-4"
                />

                <div class="flex flex-wrap gap-1.5 pr-1">
                    <NPopover
                        v-for="(ref, index) in crossRefStore.references"
                        :key="index"
                        :show="activePopoverIndex === index"
                        trigger="manual"
                        placement="top"
                        :width="320"
                        @clickoutside="activePopoverIndex = null"
                    >
                        <template #trigger>
                            <span
                                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-500 cursor-pointer border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:border-[var(--primary-color)] hover:text-[var(--primary-color)] transition-all duration-150 select-none whitespace-nowrap"
                                @click="activePopoverIndex = index; onPopoverShow(ref)"
                            >
                                {{ formatRef(ref.to_book, ref.to_chapter, ref.to_verse_start, ref.to_verse_end) }}
                            </span>
                        </template>

                        <div class="flex flex-col" style="max-height: 260px;">
                            <!-- Header: fixed -->
                            <div class="flex items-center justify-between gap-2 pb-2 shrink-0">
                                <span class="text-xs font-700 text-[var(--primary-color)]">
                                    {{ formatRef(ref.to_book, ref.to_chapter, ref.to_verse_start, ref.to_verse_end) }}
                                </span>
                                <NButton
                                    size="tiny"
                                    type="primary"
                                    secondary
                                    @click="navigateTo(ref.to_book, ref.to_chapter, ref.to_verse_start)"
                                >
                                    Go to verse
                                </NButton>
                            </div>

                            <!-- Scrollable content -->
                            <NScrollbar style="max-height: 200px;">
                                <div class="flex flex-col gap-3 pr-1">
                                    <NSkeleton v-if="popoverLoading" text :repeat="3" />

                                    <div
                                        v-for="item in popoverTexts"
                                        :key="item.version"
                                        class="flex flex-col gap-1"
                                    >
                                        <div class="text-[10px] font-600 text-gray-400 dark:text-gray-500 uppercase tracking-wide">
                                            {{ getVersionTitle(item.version) }}
                                        </div>
                                        <div class="text-xs text-gray-700 dark:text-gray-300 leading-relaxed" v-html="item.text" />
                                    </div>

                                    <div v-if="!popoverLoading && !popoverTexts.length" class="text-xs text-gray-400">
                                        No text available
                                    </div>
                                </div>
                            </NScrollbar>
                        </div>
                    </NPopover>
                </div>
            </NScrollbar>
        </NSpin>
    </div>
</template>
