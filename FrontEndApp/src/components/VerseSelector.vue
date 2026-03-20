<script lang="ts" setup>
import { NButton, NModal, NCard, NInput } from 'naive-ui';
import { useBibleStore } from './../store/BibleStore';
import { bibleBooks, BookInfo } from '../util/books';
import { ref, computed } from 'vue';
import { useSettingStore } from '../store/settingStore';

const settings = useSettingStore();
const bibleStore = useBibleStore();
const showOuter = ref(false);
const showSelectChapterDrawer = ref(false);
const showSelectVerseDrawer = ref(false);
const numberOfVerses = ref<number>(0);
const searchQuery = ref('');
const props = defineProps({
    size: {
        type: String,
        default: 'medium',
    },
    quaternary: {
        type: Boolean,
        default: true,
    },
    circle: {
        type: Boolean,
        default: false,
    },
    title: {
        type: String,
        default: 'Find Verse',
    },
});

const selectedBook = ref<BookInfo | null>(null);
const selectedChapter = ref<number | null>(null);

const filteredBooks = computed(() => {
    if (!searchQuery.value.trim()) {
        return bibleBooks;
    }
    const query = searchQuery.value.toLowerCase();
    return bibleBooks.filter(book => 
        book.title.toLowerCase().includes(query) || 
        book.short_name.toLowerCase().includes(query)
    );
});

function selectBook(book: BookInfo) {
    selectedBook.value = book;
    showSelectChapterDrawer.value = true;
}

async function selectChapter(chapter: number) {
    selectedChapter.value = chapter;
    const verseCount: number = await window.browserWindow.getVersesCount(
        JSON.stringify({
            book_number: selectedBook.value?.book_number,
            selected_chapter: chapter,
            bible_versions: bibleStore.selectedBibleVersions,
        })
    );

    numberOfVerses.value = verseCount;
    showSelectVerseDrawer.value = true;
}

function selectVerse(verse: number) {
    bibleStore.selectVerse(selectedBook.value?.book_number as number, selectedChapter.value as number, verse);
    bibleStore.AutoScrollSavedPosition(300);
    showSelectVerseDrawer.value = false;
    showSelectChapterDrawer.value = false;
    showOuter.value = false;
}

function resetSearch() {
    searchQuery.value = '';
}
</script>
<template>
    <NButton @click="showOuter = true" :quaternary="props.quaternary" :size="props.size as any" :circle="props.circle" :title="title">
        <template #icon>
            <slot name="icon" />
        </template>
        <slot />
    </NButton>
    <NModal v-model:show="showOuter" @update:show="(val) => !val && resetSearch()">
        <NCard style="width: 600px; max-height: 80vh;" title="Select Bible" class="my-30px" content-style="max-height: calc(80vh - 110px); overflow-y: auto; padding: 16px;">
            <template #header-extra>
                <NInput 
                    v-model:value="searchQuery" 
                    type="text" 
                    placeholder="Search books..." 
                    style="width: 200px"
                    clearable
                />
            </template>
            <div>
                <div class="mb-4">
                    <div class="text-sm font-600 text-gray-600 dark:text-gray-400 mb-3 uppercase tracking-wide">Old Testament</div>
                    <div class="flex flex-wrap gap-2">
                        <template v-for="(book, i) in filteredBooks" :key="book.book_number">
                            <NButton
                                v-show="(book.deuterocanonical === false || (book.deuterocanonical && settings.showDeuterocanonical)) && book.book_number < 470"
                                class="justify-start"
                                @click="selectBook(book)"
                                secondary
                                round
                            >
                                {{ $t(book.title) }}
                            </NButton>
                        </template>
                    </div>
                </div>
                <div>
                    <div class="text-sm font-600 text-gray-600 dark:text-gray-400 mb-3 uppercase tracking-wide">New Testament</div>
                    <div class="flex flex-wrap gap-2">
                        <template v-for="(book, i) in filteredBooks" :key="book.book_number">
                            <NButton
                                v-show="book.book_number >= 470"
                                class="justify-start"
                                @click="selectBook(book)"
                                secondary
                                round
                            >
                                {{ $t(book.title) }}
                            </NButton>
                        </template>
                    </div>
                </div>
            </div>
        </NCard>
    </NModal>
    <NModal v-model:show="showSelectChapterDrawer">
        <NCard style="width: 500px" title="Select Chapter" class="my-30px">
            <div class="flex flex-wrap gap-2">
                <NButton v-for="chapter in selectedBook?.chapter_count" secondary :key="chapter" @click="selectChapter(chapter)">
                    {{ chapter }}
                </NButton>
            </div>
        </NCard>
    </NModal>
    <NModal v-model:show="showSelectVerseDrawer">
        <NCard style="width: 700px" title="Select Verse" class="my-30px">
            <div class="flex flex-wrap gap-3">
                <NButton v-for="verse in numberOfVerses" secondary :key="verse" @click="selectVerse(verse)">
                    {{ verse }}
                </NButton>
            </div>
        </NCard>
    </NModal>
</template>
