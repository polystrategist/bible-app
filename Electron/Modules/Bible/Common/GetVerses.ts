import { isNightly } from '../../../config';
import { app, ipcMain } from 'electron';
import knex from 'knex';

export type GetVerseArgs = {
    bible_versions: Array<string>;
    book_number: number;
    selected_chapter: number;
};

const dataPath = app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = dataPath + `\\modules\\bible\\`;

export default () => {
    ipcMain.handle('getVerses', async (event: any, args: GetVerseArgs) => {
        const finalResult: any = [];

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
                .then((row) => {
                    row.forEach((row: any, index: any) => {
                        let text = {
                            version: version,
                            text: row.text,
                        };
                        if (finalResult[index] && finalResult[index]['version'].length > 0) {
                            finalResult[index]['version'].push(text);
                        } else {
                            finalResult[index] = {
                                book_number: row.book_number,
                                chapter: row.chapter,
                                verse: row.verse,
                            };
                            finalResult[index]['version'] = [text];
                        }
                    });
                });
        }
        return finalResult;
    });
};
