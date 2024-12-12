import { ipcMain } from 'electron';
import { StoreDB } from '../../DataBase/DataBase';
import { DAYJS } from '../../util/dayjs';

export default () => {
    ipcMain.handle('getSpaceStudyList', async (event, args) => {
        return await StoreDB.select('*')
            .from('study_spaces')
            .then((data) => {
                return data;
            });
    });

    ipcMain.handle('storeSpaceStudy', async (event, args) => {
        try {
            if (args.id == 0) {
                delete args.id;
                args.created_at = DAYJS().utc().format();
                args.updated_at = DAYJS().utc().format();

                const newData = await StoreDB('study_spaces').insert(args).returning('*');
                return newData;
            }

            args.updated_at = DAYJS().utc().format();
            return {
                data: await StoreDB('study_spaces')
                    .insert(args)
                    .onConflict('id')
                    .merge()
                    .returning('*'),
                error: null,
            };
        } catch (e: any) {
            if (e?.errno == 19) {
                return {
                    error: {
                        code: 19,
                        errno: 19,
                        message: 'Title Already Exist',
                    },
                    data: null,
                };
            }
        }
    });

    ipcMain.handle('deleteSpaceStudy', async (event, id) => {
        return await StoreDB('study_spaces').where('id', id).del();
    });
};
