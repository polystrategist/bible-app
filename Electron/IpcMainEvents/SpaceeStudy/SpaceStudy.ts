import { BrowserWindow, ipcMain } from 'electron';
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
                return {
                    data: newData[0],
                    error: null,
                };
            }

            args.updated_at = DAYJS().utc().format();

            const updatedData = await StoreDB('study_spaces')
                .insert(args)
                .onConflict('id')
                .merge()
                .returning('*');

            return {
                data: updatedData[0],
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
        const count = await StoreDB('study_spaces')
            .count('id as rowCount')
            .then((data) => {
                return data[0].rowCount;
            });

        if (count == 1) {
            return {
                error: {
                    message:
                        'Cannot Delete Last Study Space, there must be at least one study space.',
                },
                data: null,
            };
        }

        return {
            data: await StoreDB('study_spaces').where('id', id).del(),
            error: null,
        };
    });
};
