<script setup lang="ts">
import { useBookmarkStore } from '../../../../store/bookmark';
import { useBibleStore } from '../../../../store/BibleStore';
import { debouncedRunSync } from '../../../../util/Sync/sync';
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
    debouncedRunSync();
}
</script>
<template>
    <div class="h-full overflow-auto overflowing-div scroll-hover-only">
        <div
            v-for="(bookmark, key) in (bookmarkStore.bookmarks as bookmarksType)"
            :key="key"
            class="relative cursor-pointer flex justify-between items-center transition-colors duration-100"
            :class="{
                'dark:bg-light-50 dark:bg-opacity-10 bg-gray-800 bg-opacity-10': selectedBookmarkKey == key,
                'dark:hover:bg-light-50 dark:hover:bg-opacity-10 hover:bg-gray-800 hover:bg-opacity-10': selectedBookmarkKey != key,
            }"
        >
            <div
                class="absolute left-0 top-0 bottom-0 w-[2px] bg-[var(--primary-color)] transition-opacity duration-150"
                :class="selectedBookmarkKey == key ? 'opacity-100' : 'opacity-0'"
            ></div>
            <div class="w-full px-3 py-1.5" @click="selectBookVerse(key as string, bookmark)">
                <span class="font-600 text-sm mr-1">{{ $t(bibleStore.getBook(bookmark.book_number).title) }}</span>
                <span class="opacity-60 text-sm">{{ bookmark.chapter }}:{{ bookmark.verse }}</span>
            </div>
            <div
                class="pr-3 text-gray-400 hover:text-red-500 dark:hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                @click.stop
            >
                <NPopconfirm @positive-click="deleteBookmark(bookmark)">
                    <template #trigger>
                        <NIcon size="16" class="cursor-pointer opacity-40 hover:opacity-100">
                            <TrashCan />
                        </NIcon>
                    </template>
                    {{ $t('Are You sure?') }}
                </NPopconfirm>
            </div>
        </div>
    </div>
</template>
