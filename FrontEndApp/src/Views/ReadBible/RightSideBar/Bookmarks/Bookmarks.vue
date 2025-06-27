<script setup lang="ts">
import { useBookmarkStore } from '../../../../store/bookmark';
import { useBibleStore } from '../../../../store/BibleStore';
import RightSideBarContainer from './../../../../components/ReadBible/RightSideBarContainer.vue';
import { TrashCan } from '@vicons/carbon';
import { NIcon, NPopconfirm } from 'naive-ui';
import { ref } from 'vue';
import { bookmarksType } from '../../../../GlobalTypes';

const bookmarkStore = useBookmarkStore();
const bibleStore = useBibleStore();
const selectedBookmarkKey = ref<null | string>(null);

function selectBookVerse(key: string, { book_number, chapter, verse }: { book_number: number; chapter: number; verse: number }) {
    selectedBookmarkKey.value = key;
    bibleStore.selectVerse(book_number, chapter, verse);
    bibleStore.AutoScrollSavedPosition(100);
}

async function deleteBookmark(verse: any) {
    const delItem = await window.browserWindow.deleteBookmark(JSON.stringify(verse));
    await bookmarkStore.getBookmarks();
}
</script>
<template>
    <RightSideBarContainer :title="$t('Bookmarks')">
        <div
            v-for="(bookmark, key) in (bookmarkStore.bookmarks as bookmarksType)"
            :key="key"
            class="relative dark:hover:bg-light-50 dark:hover:bg-opacity-20 hover:bg-gray-800 hover:bg-opacity-20 cursor-pointer flex justify-between items-center"
        >
            <div
                class="absolute transition-all top-0 left-0 h-0 w-5px bg-[var(--primary-color)] opacity-50"
            ></div>
            <div class="w-full p-10px" @click="selectBookVerse(key as string, bookmark)">
                <span class="mr-1">{{ $t(bibleStore.getBook(bookmark.book_number).title) }}</span>
                <span>{{ bookmark.chapter }} : {{ bookmark.verse }}</span>
            </div>
            <div class="dark:hover:text-red-400 hover:text-red-500 opacity-40 hover:opacity-100 pr-10px" @click.stop>
                <NPopconfirm @positive-click="deleteBookmark(bookmark)">
                    <template #trigger>
                        <NIcon size="20">
                            <TrashCan />
                        </NIcon>
                    </template>
                    {{ $t('Are You sure?') }}
                </NPopconfirm>
            </div>
        </div>
    </RightSideBarContainer>
</template>
