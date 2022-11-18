import { isNightly } from '../../../config';
import { app, ipcMain } from 'electron';
import knex from 'knex';

export type SearchBibleInterface = {
    search: string;
    bible_versions: Array<string>;
    page: number;
    limit: number;
};

const dataPath = app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = dataPath + `\\modules\\bible\\`;

export default () => {
    ipcMain.handle('searchBible', async (event: any, args: SearchBibleInterface) => {
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
                .where('text', 'LIKE', `%${args.search}%`)
                .limit(args.limit)
                .offset(args.page == 1 ? 0 : args.page * args.limit - args.limit)
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
