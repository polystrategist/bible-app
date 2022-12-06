import { defineStore } from 'pinia';
import { onMounted, ref } from 'vue';
export const useBookmarkStore = defineStore('useBookmarkStore', () => {
    const bookmarks = ref<Object | Array<any>>({});

    async function getBookmarks() {
        const savedBookmarks = await window.browserWindow.getBookMarks();
        bookmarks.value = savedBookmarks ? savedBookmarks : {};
    }

    function isBookmarkExists(key: string) {
        const b: any = bookmarks.value;
        const exist = b[key];
        return exist ? true : false;
    }

    onMounted(() => {
        getBookmarks();
    });

    return {
        getBookmarks,
        bookmarks,
        isBookmarkExists,
    };
});
