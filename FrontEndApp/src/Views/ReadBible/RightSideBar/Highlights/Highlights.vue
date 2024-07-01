<script lang="ts" setup>
import { ref } from 'vue';
import RightSideBarContainer from '../../../../components/ReadBible/RightSideBarContainer.vue';
import { useBibleStore } from '../../../../store/BibleStore';

const bibleStore = useBibleStore();
const selectedHighlight = ref<string | null>(null);

function selectBookVerse(key: string, { book_number, chapter, verse }: { book_number: number; chapter: number; verse: number }) {
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
</script>

<template>
    <RightSideBarContainer :title="$t('Highlights')">
        <div class="h-full flex flex-col">
            <div class="h-full overflow-y-auto overflowing-div">
                <div
                    v-for="(highlight, key) in bibleStore.allHighlights"
                    :key="key"
                    class="relative dark:hover:bg-light-50 dark:hover:bg-opacity-20 hover:bg-gray-800 hover:bg-opacity-20 cursor-pointer flex justify-between items-center"
                    :class="{ 'dark:bg-light-50 dark:bg-opacity-10 bg-gray-800 bg-opacity-10': selectedHighlight == key as any }"
                >
                    <div
                        class="absolute transition-all top-0 left-0 h-0 w-5px bg-[var(--primary-color)] opacity-50"
                        :class="{ '!h-full': selectedHighlight == key as any }"
                    ></div>
                    <div class="w-full p-10px" @click="selectBookVerse(key as any, highlight)">
                        <div class="font-700">
                            <span class="mr-1" v-if="highlight.book_number">
                                {{ $t(bibleStore.getBook(highlight.book_number).title) }}
                            </span>
                            <span class="mr-2">{{ highlight.chapter }} : {{ highlight.verse }}</span>
                            <span class="text-sm opacity-70">{{ highlight.key.split('_')[0] }}</span>
                        </div>
                        <div>
                            <span v-html="highlight.content"></span>
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
