import { app, ipcMain } from 'electron';
import { getBibleVersionDb } from './BibleVersionCache';

export type GetVerseArgs = {
    bible_versions: Array<string>;
    book_number: number;
    selected_chapter: number;
};

const DEFAULT_BIBLE_MODULE = 'King James Version - 1769.SQLite3';

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

            if (rows.length > versesCount) {
                versesCount = rows.length;
            }
        }

        // Fall back to the default KJV module if selected versions have no verses for this book/chapter
        if (versesCount === 0) {
            try {
                const kjv = getBibleVersionDb(DEFAULT_BIBLE_MODULE);
                const rows = await kjv
                    .select()
                    .from('verses')
                    .where('book_number', args.book_number)
                    .where('chapter', args.selected_chapter);
                versesCount = rows.length;
            } catch {
                // KJV module not available, keep versesCount as 0
            }
        }

        return versesCount;
    });
};
