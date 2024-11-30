import { app, ipcMain } from 'electron';
import knex from 'knex';
import { isNightly } from '../../config';
import UPath from 'upath';

const dataPath = UPath.join(app.getPath('appData'), !isNightly ? 'believers-sword' : 'believers-sword-nightly');
const filePath = UPath.join(dataPath, `StoreDB`, `Store.db`);
const StoreDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: filePath,
    },
});

export default () => {
    ipcMain.handle(
        'getClipNotes',
        async (
            event,
            args: {
                page: number;
                search: string | null;
                limit: number;
            }
        ) => {
            let data: Array<any> = [];
            let offset = args.page == 1 ? 0 : args.page * args.limit - args.limit;

            await StoreDB.select()
                .from('clip_notes')
                .whereLike('content', `%${args.search ? args.search : ''}%`)
                .orderBy('id', 'desc')
                .limit(args.limit ? args.limit : 50)
                .offset(offset)
                .then((row) => {
                    row.forEach((row: any, index: any) => data.push(row));
                });

            return data;
        }
    );

    ipcMain.handle(
        'storeClipNote',
        async (
            event,
            {
                book_number,
                chapter,
                verse,
                content,
                color,
            }: { book_number: number; chapter: number; verse: number; content: string; color: string }
        ) => {
            try {
                const key = `key_${book_number}_${chapter}_${verse}`;
                await StoreDB('clip_notes')
                    .insert({
                        key,
                        book_number,
                        chapter,
                        verse,
                        content,
                        color,
                        updated_at: new Date(),
                        created_at: new Date(),
                    })
                    .onConflict('key')
                    .merge();

                return StoreDB('clip_notes').where('key', key).first();
            } catch (e) {
                console.log(e);
            }
        }
    );

    ipcMain.handle('getChapterClipNotes', async (event, { book_number, chapter }: { book_number: number; chapter: number }) => {
        try {
            let data: any = {};

            await StoreDB('clip_notes')
                .select()
                .where('book_number', book_number)
                .where('chapter', chapter)
                .then((row) => {
                    row.forEach((row: any, index: any) => {
                        data[row.key] = row;
                    });
                });

            return data;
        } catch (e) {
            console.log(e);
        }
    });

    ipcMain.handle(
        'deleteChapterClipNotes',
        async (event, { book_number, chapter, verse }: { book_number: number; chapter: number; verse: number }) => {
            try {
                return await StoreDB('clip_notes')
                    .select()
                    .where('book_number', book_number)
                    .where('chapter', chapter)
                    .where('verse', verse)
                    .del();
            } catch (e) {
                console.log(e);
            }
        }
    );
};
