<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import RightSideBarContainer from '../../../../components/ReadBible/RightSideBarContainer.vue';
import { useBibleStore } from '../../../../store/BibleStore';
import { useClipNoteStore } from '../../../../store/ClipNotes';
import { useVirtualList } from '@vueuse/core';
import { NButton, NIcon, NPopconfirm } from 'naive-ui';
import { TrashCan } from '@vicons/carbon';

const bibleStore = useBibleStore();
const clipNoteStore = useClipNoteStore();
const selectedClipNote = ref<null | string>(null);

onMounted(() => {
    clipNoteStore.clipNotesLimit = 5000;
    clipNoteStore.clipNotesPage = 1;
    clipNoteStore.getClipNotes();
});

const { list, containerProps, wrapperProps } = useVirtualList(
    computed(() => clipNoteStore.clipNotes),
    { itemHeight: 80, overscan: 6 },
);

function noteKey(clipNote: any) {
    return `${clipNote.book_number}_${clipNote.chapter}_${clipNote.verse}`;
}

function selectBookVerse(clipNote: any) {
    selectedClipNote.value = noteKey(clipNote);
    bibleStore.selectVerse(clipNote.book_number, clipNote.chapter, clipNote.verse);
    bibleStore.AutoScrollSavedPosition(100);
}

async function deleteNote(clipNote: any) {
    await clipNoteStore.deleteClipNote({
        book_number: clipNote.book_number,
        chapter: clipNote.chapter,
        verse: clipNote.verse,
    });
}

function stripHtml(html: string) {
    return html.replace(/(<([^>]+)>)/gi, ' ').replace(/\s+/g, ' ').trim();
}
</script>
<template>
    <RightSideBarContainer :title="$t('Clip Notes')">
        <div v-bind="containerProps" class="h-full overflowing-div scroll-hover-only the-clip-notes-side-bar">
            <div v-bind="wrapperProps">
                <div
                    v-for="{ data: clipNote } in list"
                    :key="noteKey(clipNote)"
                    class="relative group cursor-pointer flex items-stretch min-h-[80px] px-2 py-1"
                    @click="selectBookVerse(clipNote)"
                >
                    <!-- Selected accent bar -->
                    <div
                        class="absolute left-0 top-1 bottom-1 w-[2px] rounded-r-full bg-[var(--primary-color)] transition-opacity duration-150"
                        :class="selectedClipNote == noteKey(clipNote) ? 'opacity-100' : 'opacity-0'"
                    ></div>

                    <!-- Card -->
                    <div
                        class="w-full rounded-md p-2 flex flex-col gap-1 ring-1 ring-black ring-opacity-5 shadow-sm transition-shadow group-hover:shadow-md"
                        :style="`background-color: ${clipNote.color}`"
                    >
                        <!-- Header: reference + delete -->
                        <div class="flex items-start justify-between gap-1">
                            <div class="font-700 text-sm text-dark-900 leading-snug">
                                <span v-if="clipNote.book_number" class="mr-1">
                                    {{ $t(bibleStore.getBook(clipNote.book_number).title + '') }}
                                </span>
                                <span>{{ clipNote.chapter }}:{{ clipNote.verse }}</span>
                            </div>

                            <!-- Delete button — visible on hover -->
                            <NPopconfirm @positive-click="deleteNote(clipNote)">
                                <template #trigger>
                                    <NButton
                                        circle
                                        size="tiny"
                                        type="error"
                                        class="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity duration-150"
                                        @click.stop
                                    >
                                        <template #icon>
                                            <NIcon size="12"><TrashCan /></NIcon>
                                        </template>
                                    </NButton>
                                </template>
                                {{ $t('Are You sure?') }}
                            </NPopconfirm>
                        </div>

                        <!-- Content preview -->
                        <div class="text-xs text-dark-800 opacity-75 line-clamp-2 leading-relaxed">
                            {{ stripHtml(clipNote.content) }}
                        </div>
                    </div>
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
