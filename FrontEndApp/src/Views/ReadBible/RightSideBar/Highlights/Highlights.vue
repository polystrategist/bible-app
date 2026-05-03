<script lang="ts" setup>
import { ref, watch } from 'vue';
import RightSideBarContainer from '../../../../components/ReadBible/RightSideBarContainer.vue';
import { useBibleStore } from '../../../../store/BibleStore';
import { NButton, NIcon, NPopconfirm } from 'naive-ui';
import { Delete16Filled, Delete16Regular } from '@vicons/fluent';
import { useThemeStore } from '../../../../store/theme';
import { getBibleService } from '../../../../services/BibleService';

const themeStore = useThemeStore();
const bibleStore = useBibleStore();
const selectedHighlight = ref<string | null>(null);
const versePreviews = ref<Record<string, string>>({});

function selectBookVerse(
    key: string,
    { book_number, chapter, verse }: { book_number: number; chapter: number; verse: number },
) {
    selectedHighlight.value = key;
    if (
        bibleStore.selectedBookNumber === book_number &&
        bibleStore.selectedChapter === chapter
    ) {
        bibleStore.setActiveVerse(verse);
    } else {
        bibleStore.selectVerse(book_number, chapter, verse);
    }
    bibleStore.AutoScrollSavedPosition(100);
}

function beforePage() {
    if (bibleStore.highlightPage > 1) bibleStore.highlightPage--;
    bibleStore.getHighlights();
}

function nextPage() {
    if (bibleStore.allHighlights.length == bibleStore.highlightLimit) bibleStore.highlightPage++;
    bibleStore.getHighlights();
}

function handleRemoveHighlight(highlight: any) {
    bibleStore.removeHighlightInDb(highlight.key);
}

async function loadVersePreviews() {
    if (!bibleStore.allHighlights.length || !bibleStore.selectedBibleVersions.length) return;

    const firstVersion = bibleStore.selectedBibleVersions[0];
    const bibleService = getBibleService();
    const previews: Record<string, string> = {};

    // Group highlights by book+chapter to batch fetches
    const chapters = new Map<string, { book_number: number; chapter: number }>();
    for (const hl of bibleStore.allHighlights) {
        const chKey = `${hl.book_number}_${hl.chapter}`;
        if (!chapters.has(chKey)) {
            chapters.set(chKey, { book_number: hl.book_number, chapter: hl.chapter });
        }
    }

    // Fetch each chapter once
    for (const [, { book_number, chapter }] of chapters) {
        try {
            const verses = await bibleService.getVerses({
                bible_versions: [firstVersion],
                book_number,
                selected_chapter: chapter,
            });
            for (const v of verses) {
                const key = `${book_number}_${chapter}_${v.verse}`;
                if (v.version?.[0]?.text) {
                    const raw = v.version[0].text.replace(/<[^>]*>/g, '');
                    previews[key] = raw.length > 60 ? raw.slice(0, 60) + '...' : raw;
                }
            }
        } catch {
            // Skip on error
        }
    }

    versePreviews.value = previews;
}

// Reload previews when highlights or selected version changes
watch(
    () => [bibleStore.allHighlights, bibleStore.selectedBibleVersions[0]],
    () => {
        loadVersePreviews();
    },
    { immediate: true },
);
</script>

<template>
    <RightSideBarContainer :title="$t('Highlights')">
        <div class="h-full flex flex-col">
            <div class="h-full overflow-y-auto overflowing-div">
                <div
                    v-for="(highlight, key) in bibleStore.allHighlights"
                    :key="key"
                    class="relative dark:hover:bg-light-50 dark:hover:bg-opacity-20 hover:bg-gray-800 hover:bg-opacity-20 cursor-pointer flex justify-between items-center"
                    :class="{
                        'dark:bg-light-50 dark:bg-opacity-10 bg-gray-800 bg-opacity-10':
                            selectedHighlight == (key as any),
                    }"
                >
                    <div
                        class="absolute transition-all top-0 left-0 h-0 w-5px bg-[var(--primary-color)] opacity-50"
                        :class="{ '!h-full': selectedHighlight == (key as any) }"
                    ></div>
                    <div
                        class="w-full p-10px relative"
                        @click="selectBookVerse(key as any, highlight)"
                    >
                        <div class="flex items-center gap-6px font-700">
                            <span
                                class="inline-block w-12px h-12px rounded-full flex-shrink-0"
                                :style="`background: ${highlight.content}`"
                            ></span>
                            <span v-if="highlight.book_number">
                                {{ $t(bibleStore.getBook(highlight.book_number).title) }}
                                {{ highlight.chapter }}:{{ highlight.verse }}
                            </span>
                            <NPopconfirm @positive-click="handleRemoveHighlight(highlight)">
                                <template #trigger>
                                    <NButton
                                        secondary
                                        circle
                                        size="tiny"
                                        type="error"
                                        class="absolute top-5px right-5px"
                                    >
                                        <template #icon>
                                            <NIcon v-if="themeStore.isDark"
                                                ><Delete16Filled
                                            /></NIcon>
                                            <NIcon v-else><Delete16Regular /></NIcon>
                                        </template>
                                    </NButton>
                                </template>
                                Remove This Highlight?
                            </NPopconfirm>
                        </div>
                        <div
                            v-if="versePreviews[highlight.key]"
                            class="text-xs opacity-60 mt-2px ml-18px"
                        >
                            {{ versePreviews[highlight.key] }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="flex justify-between select-none">
                <div @click="beforePage" class="cursor-pointer hover:text-[var(--primary-color)]">
                    {{ $t('Before') }}
                </div>
                <div>{{ bibleStore.highlightPage }}</div>
                <div @click="nextPage" class="cursor-pointer hover:text-[var(--primary-color)]">
                    {{ $t('Next') }}
                </div>
            </div>
        </div>
    </RightSideBarContainer>
</template>
