<script lang="ts" setup>
import { NButton, NDrawer, NDrawerContent } from 'naive-ui';
import { useBibleStore } from '../../../store/BibleStore';
import { bibleBooks, BookInfo } from '../../../util/books';
import { ref } from 'vue';
import { useSettingStore } from '../../../store/settingStore';

const settings = useSettingStore();
const bibleStore = useBibleStore();
const showOuter = ref(false);
const showSelectChapterDrawer = ref(false);
const showSelectVerseDrawer = ref(false);
const numberOfVerses = ref<number>(0);

const selectedBook = ref<BookInfo | null>(null);
const selectedChapter = ref<number | null>(null);

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
</script>
<template>
    <NButton @click="showOuter = true">
        {{ $t(bibleStore.getSelectedData.book) }} Chapter
        {{ bibleStore.getSelectedData.chapter }}
    </NButton>
    <NDrawer v-model:show="showOuter" :width="502">
        <NDrawerContent title="Select Bible" :native-scrollbar="false">
            <div class="flex flex-wrap gap-2">
                <template v-for="(book, i) in bibleBooks" :key="book.book_number">
                    <NButton
                        v-show="book.deuterocanonical === false || (book.deuterocanonical && settings.showDeuterocanonical)"
                        class="justify-start"
                        @click="selectBook(book)"
                    >
                        {{ $t(book.title) }}
                    </NButton>
                </template>
            </div>
        </NDrawerContent>
        <NDrawer v-model:show="showSelectChapterDrawer" :width="400">
            <NDrawerContent title="Select Chapter" :native-scrollbar="false">
                <div class="flex flex-wrap gap-2">
                    <NButton v-for="chapter in selectedBook?.chapter_count" :key="chapter" @click="selectChapter(chapter)">
                        {{ chapter }}
                    </NButton>
                </div>
            </NDrawerContent>
            <NDrawer v-model:show="showSelectVerseDrawer" :width="300">
                <NDrawerContent title="Select Verse" :native-scrollbar="false">
                    <div class="flex flex-wrap gap-3">
                        <NButton v-for="verse in numberOfVerses" :key="verse" @click="selectVerse(verse)">
                            {{ verse }}
                        </NButton>
                    </div>
                </NDrawerContent>
            </NDrawer>
        </NDrawer>
    </NDrawer>
</template>
