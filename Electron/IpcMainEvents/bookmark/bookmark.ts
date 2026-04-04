import { ipcMain, BrowserWindow } from 'electron';
import Log from 'electron-log';
import { StoreDB } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

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

        const existingBookmark = await StoreDB('bookmarks')
            .where({ book_number, chapter, verse })
            .first();

        if (!existingBookmark) {
            await StoreDB('bookmarks').insert({
                key,
                book_number,
                chapter,
                verse,
                updated_at: new Date(),
                created_at: new Date(),
            });

            // Log sync change for new bookmark
            try {
                await logSyncChange({
                    table_name: 'bookmarks',
                    record_key: key,
                    action: 'created',
                    payload: {
                        key,
                        book_number,
                        chapter,
                        verse,
                    },
                    synced: 0,
                });
            } catch (e) {
                Log.error('Failed to log sync change for bookmark creation:', e);
            }
        }

        return await getVersesSavedBookmarks();
    } catch (e) {
        Log.error(e);
        return {};
    }
};

const getVersesSavedBookmarks = async () => {
    try {
        const data = await StoreDB('bookmarks').select();

        const result: any = {};
        data.forEach((item: any) => {
            result[item.key] = item;
        });

        return result;
    } catch (e) {
        Log.error(e);
        return {};
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
        const key = `${book_number}_${chapter}_${verse}`;

        const existingBookmark = await StoreDB('bookmarks')
            .where({ book_number, chapter, verse })
            .first();

        if (!existingBookmark) {
            return true;
        }

        await StoreDB('bookmarks')
            .where('book_number', book_number)
            .andWhere('chapter', chapter)
            .andWhere('verse', verse)
            .delete();

        // Log sync change AFTER successful delete
        try {
            await logSyncChange({
                table_name: 'bookmarks',
                record_key: key,
                action: 'deleted',
                payload: {
                    key,
                    book_number,
                    chapter,
                    verse,
                },
                synced: 0,
            });
        } catch (e) {
            Log.error('Failed to log sync change for bookmark deletion:', e);
        }

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
