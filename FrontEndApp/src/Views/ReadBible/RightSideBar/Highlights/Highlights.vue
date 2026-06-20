<script lang="ts" setup>
import { ref, watch, onMounted, computed } from 'vue';
import { useBibleStore } from '../../../../store/BibleStore';
import { NButton, NIcon, NPopconfirm } from 'naive-ui';
import { Delete16Filled, Delete16Regular } from '@vicons/fluent';
import { useThemeStore } from '../../../../store/theme';
import { getBibleService } from '../../../../services/BibleService';
import { useVirtualList } from '@vueuse/core';

const themeStore = useThemeStore();
const bibleStore = useBibleStore();
const selectedHighlight = ref<string | null>(null);
const versePreviews = ref<Record<string, string>>({});

onMounted(() => {
    // Load all highlights at once so virtual scroll has the full dataset
    bibleStore.highlightLimit = 5000;
    bibleStore.highlightPage = 1;
    bibleStore.getHighlights();
});

const { list, containerProps, wrapperProps } = useVirtualList(
    computed(() => bibleStore.allHighlights),
    { itemHeight: 50, overscan: 8 },
);

function selectBookVerse(highlight: any) {
    selectedHighlight.value = highlight.key;
    if (
        bibleStore.selectedBookNumber === highlight.book_number &&
        bibleStore.selectedChapter === highlight.chapter
    ) {
        bibleStore.setActiveVerse(highlight.verse);
    } else {
        bibleStore.selectVerse(highlight.book_number, highlight.chapter, highlight.verse);
    }
    bibleStore.AutoScrollSavedPosition(100);
}

function handleRemoveHighlight(highlight: any) {
    bibleStore.removeHighlightInDb(highlight.key);
}

async function loadVersePreviews() {
    if (!bibleStore.allHighlights.length || !bibleStore.selectedBibleVersions.length) return;

    const firstVersion = bibleStore.selectedBibleVersions[0];
    const bibleService = getBibleService();
    const previews: Record<string, string> = {};

    const chapters = new Map<string, { book_number: number; chapter: number }>();
    for (const hl of bibleStore.allHighlights) {
        const chKey = `${hl.book_number}_${hl.chapter}`;
        if (!chapters.has(chKey)) {
            chapters.set(chKey, { book_number: hl.book_number, chapter: hl.chapter });
        }
    }

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
            // skip on error
        }
    }

    versePreviews.value = previews;
}

watch(
    () => [bibleStore.allHighlights, bibleStore.selectedBibleVersions[0]],
    () => loadVersePreviews(),
    { immediate: true },
);
</script>

<template>
    <div v-bind="containerProps" class="h-full overflowing-div scroll-hover-only">
            <div v-bind="wrapperProps">
                <div
                    v-for="{ data: highlight } in list"
                    :key="highlight.key"
                    class="relative cursor-pointer flex justify-between items-center min-h-[50px]"
                    :class="{
                        'dark:bg-light-50 dark:bg-opacity-10 bg-gray-800 bg-opacity-10':
                            selectedHighlight == highlight.key,
                        'dark:hover:bg-light-50 dark:hover:bg-opacity-10 hover:bg-gray-800 hover:bg-opacity-10':
                            selectedHighlight != highlight.key,
                    }"
                    @click="selectBookVerse(highlight)"
                >
                    <div
                        class="absolute left-0 top-0 bottom-0 w-[2px] bg-[var(--primary-color)] transition-opacity duration-150"
                        :class="selectedHighlight == highlight.key ? 'opacity-100' : 'opacity-0'"
                    ></div>
                    <div class="w-full px-3 py-1 relative">
                        <div class="flex items-center gap-6px font-700">
                            <span
                                class="inline-block w-10px h-10px rounded-full flex-shrink-0"
                                :style="`background: ${highlight.content}`"
                            ></span>
                            <span v-if="highlight.book_number" class="text-sm">
                                {{ $t(bibleStore.getBook(highlight.book_number).title) }}
                                {{ highlight.chapter }}:{{ highlight.verse }}
                            </span>
                        </div>
                        <div
                            v-if="versePreviews[highlight.key]"
                            class="text-xs opacity-50 mt-0.5 ml-4 truncate"
                        >
                            {{ versePreviews[highlight.key] }}
                        </div>
                        <div v-else class="text-xs opacity-20 mt-0.5 ml-4 italic truncate">
                            {{ $t(bibleStore.getBook(highlight.book_number).title) }} {{ highlight.chapter }}:{{ highlight.verse }}
                        </div>
                    </div>
                    <NPopconfirm @positive-click="handleRemoveHighlight(highlight)" @click.stop>
                        <template #trigger>
                            <NButton
                                secondary
                                circle
                                size="tiny"
                                type="error"
                                class="flex-shrink-0 mr-2"
                                @click.stop
                            >
                                <template #icon>
                                    <NIcon v-if="themeStore.isDark"><Delete16Filled /></NIcon>
                                    <NIcon v-else><Delete16Regular /></NIcon>
                                </template>
                            </NButton>
                        </template>
                        Remove This Highlight?
                    </NPopconfirm>
                </div>
            </div>
    </div>
</template>
