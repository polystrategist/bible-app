import Log from 'electron-log';
import { app, ipcMain } from 'electron';
import { updateOrCreate } from '../../DataBase/DataBase';
import { StoreDB } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

export type GetVerseArgs = {
    bible_versions: Array<string>;
    book_number: number;
    selected_chapter: number;
};

export default () => {
    ipcMain.handle(
        'getHighLights',
        async (
            event,
            args: {
                page: number;
                search: string | null;
                limit: number;
            }
        ) => {
            const offset = args.page == 1 ? 0 : args.page * args.limit - args.limit;

            const data = await StoreDB.select()
                .from('highlights')
                .whereLike('content', `%${args.search ? args.search : ''}%`)
                .orderBy('id', 'desc')
                .limit(args.limit ? args.limit : 50)
                .offset(offset);

            return data;
        }
    );

    ipcMain.handle(
        'getChapterHighlights',
        async (
            event: any,
            args: {
                book_number: number;
                chapter: number;
            }
        ) => {
            const data = await StoreDB.select()
                .from('highlights')
                .where('book_number', args.book_number)
                .where('chapter', args.chapter);

            const result: any = {};
            data.forEach((row: any) => {
                result[row.key] = row;
            });

            return result;
        }
    );

    ipcMain.handle(
        'saveHighlight',
        async (
            event,
            {
                key,
                book_number,
                chapter,
                verse,
                content,
            }: {
                key: string;
                book_number: number;
                chapter: number;
                verse: number;
                content: string;
            }
        ) => {
            try {
                const existingHighlight = await StoreDB('highlights')
                    .where({ key })
                    .first();

                await updateOrCreate(
                    'highlights',
                    { key },
                    {
                        book_number,
                        chapter,
                        verse,
                        content,
                    }
                );

                try {
                    await logSyncChange({
                        table_name: 'highlights',
                        record_key: key,
                        action: existingHighlight ? 'updated' : 'created',
                        payload: {
                            key,
                            book_number,
                            chapter,
                            verse,
                            content,
                        },
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('Failed to log sync change for highlight:', e);
                }

                return 1;
            } catch (e) {
                Log.error(e);
                return 0;
            }
        }
    );

    ipcMain.handle(
        'deleteHighlight',
        async (event, args: { key: string }) => {
            try {
                const existingHighlight = await StoreDB('highlights')
                    .where('key', args.key)
                    .first();

                if (existingHighlight) {
                    try {
                        await logSyncChange({
                            table_name: 'highlights',
                            record_key: args.key,
                            action: 'deleted',
                            payload: existingHighlight,
                            synced: 0,
                        });
                    } catch (e) {
                        Log.error('Failed to log sync change for highlight deletion:', e);
                    }
                }

                return await StoreDB('highlights')
                    .where('key', args.key)
                    .del();
            } catch (e) {
                console.log(e);
            }
        }
    );
};
