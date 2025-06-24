import { ipcMain, BrowserWindow, app } from 'electron';
import UPath from 'upath';
import knex from 'knex';
import { getSelectedSpaceStudy } from '../SpaceeStudy/SpaceStudy';
import { setupPortableMode } from '../../util/portable';

setupPortableMode();
const dataPath = app.getPath('userData');
const filePath = UPath.join(dataPath, `StoreDB`, `Store.db`);
const StoreDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: filePath,
    },
});

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
        const selectedSpaceStudy = await getSelectedSpaceStudy();

        const existingBookmark = await StoreDB('bookmarks')
            .where({ book_number, chapter, verse, study_space_id: selectedSpaceStudy.id })
            .first();

        if (!existingBookmark) {
            await StoreDB('bookmarks').insert({
                key: `${book_number}_${chapter}_${verse}`,
                book_number,
                chapter,
                verse,
                study_space_id: selectedSpaceStudy.id,
                updated_at: new Date(),
                created_at: new Date(),
            });
        }

        return await getVersesSavedBookmarks();
    } catch (e) {
        if (e instanceof Error) console.log(e.message);
    }
};

const getVersesSavedBookmarks = async () => {
    try {
        const selectedSpaceStudy = await getSelectedSpaceStudy();

        const data = await StoreDB('bookmarks')
            .select()
            .where('study_space_id', selectedSpaceStudy.id);

        const result: any = {};
        for (const item of data) {
            result[item.key] = item;
        }

        return result;
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
        await StoreDB('bookmarks')
            .where('book_number', book_number)
            .andWhere('chapter', chapter)
            .andWhere('verse', verse)
            .delete();

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
