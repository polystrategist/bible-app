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
            const selectedSpaceStudy = await getSelectedSpaceStudy();
            const data = await StoreDB.select()
                .from('highlights')
                .where('book_number', args.book_number)
                .where('chapter', args.chapter)
                .where('study_space_id', selectedSpaceStudy.id);

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
                const selectedSpaceStudy = await getSelectedSpaceStudy();

                if (content.includes('HasHighlightSpan')) {
                    const existingHighlight = await StoreDB('highlights')
                        .where({
                            key,
                            study_space_id: selectedSpaceStudy.id,
                        })
                        .first();

                    await updateOrCreate(
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
                                study_space_id: selectedSpaceStudy.id,
                                study_space_name: selectedSpaceStudy.title,
                            },
                            synced: 0,
                        });
                    } catch (e) {
                        Log.error('Failed to log sync change for highlight:', e);
                    }
                } else {
                    // Highlight being removed — scope lookup and delete to current study space
                    const existingHighlight = await StoreDB('highlights')
                        .where('key', key)
                        .where('study_space_id', selectedSpaceStudy.id)
                        .first();

                    if (existingHighlight) {
                        try {
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
                                    study_space_id: selectedSpaceStudy.id,
                                    study_space_name: selectedSpaceStudy.title,
                                },
                                synced: 0,
                            });
                        } catch (e) {
                            Log.error('Failed to log sync change for highlight deletion:', e);
                        }
                    }

                    await StoreDB('highlights')
                        .where('key', key)
                        .where('study_space_id', selectedSpaceStudy.id)
                        .del();
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
                    .where('study_space_id', args.study_space_id)
                    .first();

                if (existingHighlight) {
                    const studySpace = await StoreDB('study_spaces')
                        .where('id', args.study_space_id)
                        .first();
                    try {
                        await logSyncChange({
                            table_name: 'highlights',
                            record_key: args.key,
                            action: 'deleted',
                            payload: {
                                ...existingHighlight,
                                study_space_name: studySpace?.title ?? 'default',
                            },
                            synced: 0,
                        });
                    } catch (e) {
                        Log.error('Failed to log sync change for highlight deletion:', e);
                    }
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
