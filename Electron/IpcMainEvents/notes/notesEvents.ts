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
                const existingNote = await StoreDB('notes')
                    .where('study_space_id', space_study_id)
                    .first();

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

                const studySpace = await StoreDB('study_spaces').where('id', space_study_id).first();

                try {
                    await logSyncChange({
                        table_name: 'notes',
                        record_key: String(space_study_id),
                        action: existingNote ? 'updated' : 'created',
                        payload: {
                            study_space_id: space_study_id,
                            study_space_name: studySpace?.title ?? 'default',
                            content: note,
                        },
                        synced: 0,
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
