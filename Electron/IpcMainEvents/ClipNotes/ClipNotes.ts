import { app, ipcMain } from 'electron';
import Log from 'electron-log';
import { getSelectedSpaceStudy } from '../SpaceeStudy/SpaceStudy';
import { updateOrCreate } from '../../DataBase/DataBase';
import { StoreDB } from '../../DataBase/DataBase';

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
            const selectedSpaceStudy = await getSelectedSpaceStudy();
            const offset = args.page == 1 ? 0 : args.page * args.limit - args.limit;

            const data = await StoreDB.select()
                .from('clip_notes')
                .whereLike('content', `%${args.search ? args.search : ''}%`)
                .where('study_space_id', selectedSpaceStudy.id)
                .orderBy('id', 'desc')
                .limit(args.limit ? args.limit : 50)
                .offset(offset);

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
            }: {
                book_number: number;
                chapter: number;
                verse: number;
                content: string;
                color: string;
            }
        ) => {
            try {
                const selectedSpaceStudy = await getSelectedSpaceStudy();

                const key = `key_${book_number}_${chapter}_${verse}`;

                const result = await updateOrCreate(
                    'clip_notes',
                    {
                        key,
                        study_space_id: selectedSpaceStudy.id,
                    },
                    {
                        book_number,
                        chapter,
                        verse,
                        content,
                        color,
                        updated_at: new Date(),
                        created_at: new Date(),
                    }
                );

                return StoreDB('clip_notes')
                    .where('key', key)
                    .where('study_space_id', selectedSpaceStudy.id)
                    .first();
            } catch (e) {
                console.log(e);
            }
        }
    );

    ipcMain.handle(
        'getChapterClipNotes',
        async (event, { book_number, chapter }: { book_number: number; chapter: number }) => {
            try {
                const data = await StoreDB('clip_notes')
                    .select()
                    .where('book_number', book_number)
                    .where('chapter', chapter);

                const result: any = {};
                data.forEach((row: any) => {
                    result[row.key] = row;
                });

                return result;
            } catch (e) {
                Log.error(e);
                return {};
            }
        }
    );

    ipcMain.handle(
        'deleteChapterClipNotes',
        async (
            event,
            { book_number, chapter, verse }: { book_number: number; chapter: number; verse: number }
        ) => {
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
