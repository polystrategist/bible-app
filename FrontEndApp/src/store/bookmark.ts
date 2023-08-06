import { defineStore } from 'pinia';
import { onMounted, ref } from 'vue';
import { bookmarksType } from '../GlobalTypes';

export const useBookmarkStore = defineStore('useBookmarkStore', () => {
    const bookmarks = ref<bookmarksType>({});

    async function getBookmarks() {
        const savedBookmarks = await window.browserWindow.getBookMarks();
        bookmarks.value = savedBookmarks ? savedBookmarks : {};
        console.log(bookmarks.value);
    }

    function isBookmarkExists(key: string) {
        const b: any = bookmarks.value;
        const exist = b[key];
        return !!exist;
    }

    onMounted(async () => {
        await getBookmarks();
    });

    return {
        getBookmarks,
        bookmarks,
        isBookmarkExists
    };
});
