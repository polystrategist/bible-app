import { ipcMain, BrowserWindow } from 'electron';
import { bookmarkStore } from '../../ElectronStore/bookmarkStore';

const saveVersesInBookmark = async ({
    book_number,
    chapter,
    verse,
    version,
}: {
    book_number: number;
    chapter: number;
    verse: number;
    version: Array<any> | null | undefined;
}) => {
    try {
        const key = `${book_number}_${chapter}_${verse}`;
        bookmarkStore.set(`bookmarks.${key}`, { book_number, chapter, verse, version: version ? version : [] });
        return bookmarkStore.get('bookmarks');
    } catch (e) {
        if (e instanceof Error) console.log(e.message);
    }
};

const getVersesSavedBookmarks = async () => {
    try {
        return await bookmarkStore.get('bookmarks');
    } catch (e) {
        if (e instanceof Error) console.log(e.message);
    }
};

const deleteVerseInSavedBookmarks = async ({
    book_number,
    chapter,
    verse,
}: {
    book_number: number;
    chapter: number;
    verse: number;
}) => {
    try {
        await bookmarkStore.delete(`bookmarks.${book_number}_${chapter}_${verse}` as any);
        return true;
    } catch (e) {
        return false;
    }
};

export const BookmarkEvents = (win: BrowserWindow) => {
    ipcMain.handle('save-bookmark', (event, payload) => saveVersesInBookmark(payload));
    ipcMain.handle('get-bookmarks', (event) => getVersesSavedBookmarks());
    ipcMain.handle('delete-bookmark', (event, payload) => deleteVerseInSavedBookmarks(payload));
};
