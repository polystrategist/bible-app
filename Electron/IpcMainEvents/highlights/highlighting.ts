import Log from 'electron-log';
import { app, ipcMain } from 'electron';
import { getSelectedSpaceStudy } from '../SpaceeStudy/SpaceStudy';
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
            const selectedSpaceStudy = await getSelectedSpaceStudy();
            const offset = args.page == 1 ? 0 : args.page * args.limit - args.limit;

            const data = await StoreDB.select()
                .from('highlights')
                .whereLike('content', `%${args.search ? args.search : ''}%`)
                .where('study_space_id', selectedSpaceStudy.id)
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
                if (content.includes('HasHighlightSpan')) {
                    const selectedSpaceStudy = await getSelectedSpaceStudy();

                    const existingHighlight = await StoreDB('highlights')
                        .where({
                            key,
                            study_space_id: selectedSpaceStudy.id,
                        })
                        .first();

                    const result = await updateOrCreate(
                        'highlights',
                        {
                            key,
                            study_space_id: selectedSpaceStudy.id,
                        },
                        {
                            book_number,
                            chapter,
                            verse,
                            content,
                        }
                    );

                    // Log sync change
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
                            study_space_id: selectedSpaceStudy.id,
                        },
                        synced: 0,
                    });
                } else {
                    // Highlight being removed
                    const existingHighlight = await StoreDB('highlights')
                        .where('key', key)
                        .first();

                    if (existingHighlight) {
                        // Log sync change before deletion
                        await logSyncChange({
                            table_name: 'highlights',
                            record_key: key,
                            action: 'deleted',
                            payload: {
                                key,
                                book_number,
                                chapter,
                                verse,
                                content: existingHighlight.content,
                            },
                            synced: 0,
                        });
                    }

                    await StoreDB('highlights').where('key', key).del();
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
        async (event, args: { study_space_id: number | string; key: string }) => {
            try {
                const existingHighlight = await StoreDB('highlights')
                    .where('key', args.key)
                    .first();

                if (existingHighlight) {
                    // Log sync change before deletion
                    await logSyncChange({
                        table_name: 'highlights',
                        record_key: args.key,
                        action: 'deleted',
                        payload: existingHighlight,
                        synced: 0,
                    });
                }

                return await StoreDB('highlights')
                    .where('key', args.key)
                    .where('study_space_id', args.study_space_id)
                    .del();
            } catch (e) {
                console.log(e);
            }
        }
    );
};
