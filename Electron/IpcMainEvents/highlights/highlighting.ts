import Log from 'electron-log';
import { app, ipcMain } from 'electron';
import knex from 'knex';
import { getSelectedSpaceStudy } from '../SpaceeStudy/SpaceStudy';
import { updateOrCreate } from '../../DataBase/DataBase';
import { setupPortableMode } from '../../util/portable';

export type GetVerseArgs = {
    bible_versions: Array<string>;
    book_number: number;
    selected_chapter: number;
};

setupPortableMode();
const dataPath = app.getPath('userData');
const filePath = dataPath + `\\StoreDB\\Store.db`;
const StoreDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: filePath,
    },
});

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

            let data: Array<any> = [];
            let offset = args.page == 1 ? 0 : args.page * args.limit - args.limit;

            await StoreDB.select()
                .from('highlights')
                .whereLike('content', `%${args.search ? args.search : ''}%`)
                .where('study_space_id', selectedSpaceStudy.id)
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
        'getChapterHighlights',
        async (
            event: any,
            args: {
                book_number: number;
                chapter: number;
            }
        ) => {
            let data: any = {};
            await StoreDB.select()
                .from('highlights')
                .where('book_number', args.book_number)
                .where('chapter', args.chapter)
                .then((row) => {
                    row.forEach((row: any, index: any) => {
                        data[row.key] = row;
                    });
                });

            return data;
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
                } else {
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
