<script lang="ts" setup>
import { ref } from 'vue';
import RightSideBarContainer from '../../../../components/ReadBible/RightSideBarContainer.vue';
import { useBibleStore } from '../../../../store/BibleStore';
import { NButton, NIcon, NPopconfirm } from 'naive-ui';
import { Delete16Filled, Delete16Regular } from '@vicons/fluent';
import { useThemeStore } from '../../../../store/theme';

const themeStore = useThemeStore();
const bibleStore = useBibleStore();
const selectedHighlight = ref<string | null>(null);

function selectBookVerse(
    key: string,
    { book_number, chapter, verse }: { book_number: number; chapter: number; verse: number },
) {
    selectedHighlight.value = key;
    bibleStore.selectVerse(book_number, chapter, verse);
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
    bibleStore.removeHighlightInDb(highlight.study_space_id, highlight.key);
}

function getVersePreview(highlight: any): string {
    // Find the verse in renderVerses and return the first version's raw text
    const verse = bibleStore.renderVerses.find(
        (v: any) =>
            v.book_number === highlight.book_number &&
            v.chapter === highlight.chapter &&
            v.verse === highlight.verse,
    );
    if (!verse || !verse.version[0]) return '';
    // Strip HTML tags to get plain text
    const text = verse.version[0].text.replace(/<[^>]*>/g, '');
    return text.length > 80 ? text.slice(0, 80) + '...' : text;
}
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
                        <div class="text-sm opacity-70 mt-2px">
                            {{ getVersePreview(highlight) }}
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
