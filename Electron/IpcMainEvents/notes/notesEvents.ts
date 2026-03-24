import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB, updateOrCreate } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

export default () => {
    ipcMain.handle('getNote', async (event, space_study_id: number) => {
        return await StoreDB.select().from('notes').where('study_space_id', space_study_id).first();
    });

    ipcMain.handle(
        'saveNote',
        async (event, { space_study_id, note }: { space_study_id: number; note: string }) => {
            try {
                await updateOrCreate(
                    'notes',
                    {
                        study_space_id: space_study_id,
                    },
                    {
                        content: note,
                        updated_at: new Date(),
                    }
                );

                // Log sync change for notes
                try {
                    await logSyncChange({
                        table_name: 'notes',
                        record_key: String(space_study_id),
                        action: 'updated',
                        payload: {
                            study_space_id: space_study_id,
                            content: note
                        },
                        synced: 0
                    });
                } catch (syncErr) {
                    Log.error('Failed to log sync change for note update:', syncErr);
                }
            } catch (e) {
                Log.error(e);
            }
        }
    );
};
