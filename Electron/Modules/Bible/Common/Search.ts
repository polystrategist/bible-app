import { app, ipcMain } from 'electron';
import { getBibleVersionDb } from './BibleVersionCache';

export type SearchBibleInterface = {
    search: string;
    bible_versions: Array<string>;
    book_number: number | string;
    book_numbers: Array<number | string>;
    page: number;
    limit: number;
};

export default () => {
    ipcMain.handle('searchBible', async (event: any, args: SearchBibleInterface) => {
        const finalResult: any = [];

        for (const version of args.bible_versions) {
            const bibleVersion = getBibleVersionDb(version);

            const rows = await bibleVersion
                .select()
                .from('verses')
                .where((query: any) => {
                    query.where('text', 'LIKE', `%${args.search}%`);

                    if (args.book_numbers) {
                        query.where((bookNumberQuery: any) => {
                            for (const bookNum of args.book_numbers) {
                                bookNumberQuery.orWhere('book_number', bookNum);
                            }
                        });
                    } else if (args.book_number) {
                        query.where('book_number', args.book_number);
                    }
                })
                .limit(args.limit)
                .offset(args.page == 1 ? 0 : args.page * args.limit - args.limit);

            rows.forEach((row: any) => {
                const text = {
                    version: version,
                    text: row.text,
                };
                const key = `${row.book_number}_${row.chapter}_${row.verse}`;
                if (finalResult[key]) {
                    finalResult[key]['version'].push(text);
                } else {
                    finalResult[key] = {
                        book_number: row.book_number,
                        chapter: row.chapter,
                        verse: row.verse,
                    };
                    finalResult[key]['version'] = [text];
                }
            });
        }

        // Convert object to array for frontend
        return Object.values(finalResult);
    });
};
