import { app, ipcMain } from 'electron';
import { getBibleVersionDb } from './BibleVersionCache';

export type GetVerseArgs = {
    bible_versions: Array<string>;
    book_number: number;
    selected_chapter: number;
};

export default () => {
    ipcMain.handle('getVersesCount', async (event: any, args: GetVerseArgs) => {
        let versesCount = 0;

        for (const version of args.bible_versions) {
            const bibleVersion = getBibleVersionDb(version);

            const rows = await bibleVersion
                .select()
                .from('verses')
                .where('book_number', args.book_number)
                .where('chapter', args.selected_chapter);

            versesCount = rows.length;
        }
        return versesCount;
    });
};
