import { isNightly } from '../../../config';
import { app, ipcMain } from 'electron';
import knex from 'knex';

export type GetVerseArgs = {
    bible_versions: Array<string>;
    book_number: number;
    selected_chapter: number;
};

const dataPath = app.getPath('userData');
const filePath = dataPath + `\\modules\\bible\\`;

export default () => {
    ipcMain.handle('getVersesCount', async (event: any, args: GetVerseArgs) => {
        let versesCount = 0;

        for (const version of args.bible_versions) {
            const bibleVersion = knex({
                client: 'sqlite3',
                useNullAsDefault: false,
                connection: {
                    filename: filePath + version,
                },
            });

            await bibleVersion
                .select()
                .from('verses')
                .where('book_number', args.book_number)
                .where('chapter', args.selected_chapter)
                .then((rows) => {
                    versesCount = rows.length;
                });
        }
        return versesCount;
    });
};
