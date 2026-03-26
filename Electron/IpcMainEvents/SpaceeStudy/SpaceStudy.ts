import { BrowserWindow, ipcMain } from 'electron';
import { StoreDB } from '../../DataBase/DataBase';
import { DAYJS } from '../../util/dayjs';
import Log from 'electron-log';
import { logSyncChange } from '../../DataBase/SyncDB';

export async function getSelectedSpaceStudy() {
    return await StoreDB.select('*')
        .from('study_spaces')
        .where('is_selected', true)
        .first()
}

export default () => {
    ipcMain.handle('getSpaceStudyList', async (event, args) => {
        const data = await StoreDB.select('*').from('study_spaces');
        return data;
    });

    ipcMain.handle('storeSpaceStudy', async (event, args) => {
        try {
            if (args.id == 0) {
                delete args.id;
                args.created_at = DAYJS().utc().format();
                args.updated_at = DAYJS().utc().format();

                const newData = await StoreDB('study_spaces').insert(args).returning('*');
                // Log sync change for create
                try {
                    await logSyncChange({
                        table_name: 'study_spaces',
                        record_key: String(newData[0].id),
                        action: 'created',
                        payload: newData[0],
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('Failed to log sync change for study space creation:', e);
                }
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
            // Log sync change for update
            try {
                await logSyncChange({
                    table_name: 'study_spaces',
                    record_key: String(updatedData[0].id),
                    action: 'updated',
                    payload: updatedData[0],
                    synced: 0,
                });
            } catch (e) {
                Log.error('Failed to log sync change for study space update:', e);
            }
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
        const countResult = await StoreDB('study_spaces').count('id as rowCount').first();
        const count = countResult?.rowCount ?? 0;

        if (count == 1) {
            return {
                error: {
                    message:
                        'Cannot Delete Last Study Space, there must be at least one study space.',
                },
                data: null,
            };
        }

        // Get the study space before deleting for sync log
        const existing = await StoreDB('study_spaces').where('id', id).first();
        const data = await StoreDB('study_spaces').where('id', id).del();
        // Log sync change for delete
        if (existing) {
            try {
                await logSyncChange({
                    table_name: 'study_spaces',
                    record_key: String(id),
                    action: 'deleted',
                    payload: existing,
                    synced: 0,
                });
            } catch (e) {
                Log.error('Failed to log sync change for study space deletion:', e);
            }
        }
        return {
            data,
            error: null,
        };
    });

    ipcMain.handle('selectStudySpace', async (event, id) => {
        try {
            await StoreDB('study_spaces').whereNot('id', id).update({ is_selected: false });
            const updatedData = await StoreDB('study_spaces')
                .where('id', id)
                .update({ is_selected: true })
                .returning('*');

            return {
                data: updatedData[0],
                error: null,
            };
        } catch (e: any) {
            return {
                error: {
                    message: e.message,
                },
                data: null,
            };
        }
    });

    ipcMain.handle('getSelectedSpaceStudy', async (event) => {
        const data = await getSelectedSpaceStudy();

        return {
            data,
            error: null,
        };
    });
};
