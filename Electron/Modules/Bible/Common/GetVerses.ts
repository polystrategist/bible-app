import { isNightly } from '../../../config';
import { app, ipcMain } from 'electron';
import { getBibleVersionDb } from './BibleVersionCache';

export type GetVerseArgs = {
    bible_versions: Array<string>;
    book_number: number;
    selected_chapter: number;
};

export default () => {
    ipcMain.handle('getVerses', async (event: any, args: GetVerseArgs) => {
        const finalResult: any = [];

        for (const version of args.bible_versions) {
            const bibleVersion = getBibleVersionDb(version);

            const rows = await bibleVersion
                .select()
                .from('verses')
                .where('book_number', args.book_number)
                .where('chapter', args.selected_chapter);

            rows.forEach((row: any) => {
                const text = {
                    version: version,
                    text: row.text,
                };
                if (finalResult[row.verse - 1]) {
                    finalResult[row.verse - 1]['version'].push(text);
                } else {
                    finalResult[row.verse - 1] = {
                        book_number: row.book_number,
                        chapter: row.chapter,
                        verse: row.verse,
                    };
                    finalResult[row.verse - 1]['version'] = [text];
                }
            });
        }
        return finalResult;
    });
};
