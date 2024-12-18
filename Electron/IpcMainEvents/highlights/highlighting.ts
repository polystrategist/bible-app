import Log from 'electron-log';
import { isNightly } from './../../config';
import { app, ipcMain } from 'electron';
import knex from 'knex';
import { getSelectedSpaceStudy } from '../SpaceeStudy/SpaceStudy';

export type GetVerseArgs = {
    bible_versions: Array<string>;
    book_number: number;
    selected_chapter: number;
};

const dataPath =
    app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
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
                    await StoreDB('highlights')
                        .insert({
                            key,
                            book_number,
                            chapter,
                            verse,
                            content,
                            study_space_id: selectedSpaceStudy.id,
                        })
                        .onConflict(['key', 'study_space_id'])
                        .merge();
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
};
