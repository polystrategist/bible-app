import ElectronStore from 'electron-store';

export const bookmarkStore = new ElectronStore({
    name: 'bibleBookmark',
    defaults: {
        bookmarks: {},
    },
    schema: {
        bookmarks: {
            type: 'object',
        },
    },
});
