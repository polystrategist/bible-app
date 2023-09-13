<script setup lang="ts">
import { ref } from 'vue';
import RightSideBarContainer from '../../../../components/ReadBible/RightSideBarContainer.vue';
import { useBibleStore } from '../../../../store/BibleStore';
import { useClipNoteStore } from '../../../../store/ClipNotes';

const bibleStore = useBibleStore();
const clipNoteStore = useClipNoteStore();
const selectedClipNote = ref<null | string>(null);

function selectBookVerse(key: string, { book_number, chapter, verse }: { book_number: number; chapter: number; verse: number }) {
    selectedClipNote.value = key;
    bibleStore.selectVerse(book_number, chapter, verse);
    bibleStore.AutoScrollSavedPosition(100);
}

function beforePage() {
    if (clipNoteStore.clipNotesPage > 1) clipNoteStore.clipNotesPage--;
    clipNoteStore.getClipNotes();
}

function nextPage() {
    if (clipNoteStore.clipNotes.length == clipNoteStore.clipNotesLimit) clipNoteStore.clipNotesPage++;
    clipNoteStore.getClipNotes();
}
</script>
<template>
    <RightSideBarContainer :title="$t('Clip Notes')">
        <div class="h-full flex flex-col the-clip-notes-side-bar">
            <div class="h-full overflow-y-auto overflowing-div">
                <div
                    v-for="(clipNote, key) in clipNoteStore.clipNotes"
                    :key="key"
                    class="relative dark:hover:bg-light-50 dark:hover:bg-opacity-20 hover:bg-gray-800 hover:bg-opacity-20 cursor-pointer flex justify-between items-center p-2 text-dark-900 rounded-md"
                    :class="{ 'dark:bg-light-50 dark:bg-opacity-10 bg-gray-800 bg-opacity-10': selectedClipNote == key as any }"
                >
                    <div
                        class="absolute transition-all top-0 left-0 h-0 w-5px bg-[var(--primary-color)] opacity-50"
                        :class="{ '!h-full': selectedClipNote == key as any }"
                    ></div>
                    <div
                        class="w-full p-4px rounded-sm"
                        @click="selectBookVerse(key as any, clipNote)"
                        :style="`background-color:${clipNote.color}`"
                    >
                        <div class="font-700">
                            <span class="mr-1" v-if="clipNote.book_number">
                                {{ $t(bibleStore.getBook(clipNote.book_number).title+'') }}
                            </span>
                            <span>{{ clipNote.chapter }} : {{ clipNote.verse }}</span>
                        </div>
                        <div>{{ clipNote.content.replace(/(<([^>]+)>)/gi, ' ').slice(0, 40) }}...</div>
                    </div>
                </div>
            </div>
            <div class="flex justify-between select-none">
                <div @click="beforePage" class="cursor-pointer hover:text-[var(--primary-color)]">
                    {{ $t('Before') }}
                </div>
                <div>{{ clipNoteStore.clipNotesPage }}</div>
                <div @click="nextPage" class="cursor-pointer hover:text-[var(--primary-color)]">
                    {{ $t('Next') }}
                </div>
            </div>
        </div>
    </RightSideBarContainer>
</template>
<style lang="scss">
.the-clip-notes-side-bar {
    p {
        margin: 0;
    }
}
</style>
