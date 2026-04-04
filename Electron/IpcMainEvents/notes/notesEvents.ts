import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB, updateOrCreate } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

export default () => {
    ipcMain.handle('getNote', async (event) => {
        return await StoreDB.select().from('notes').first();
    });

    ipcMain.handle(
        'saveNote',
        async (event, { note }: { note: string }) => {
            try {
                const existingNote = await StoreDB('notes').first();

                if (existingNote) {
                    await StoreDB('notes')
                        .where('id', existingNote.id)
                        .update({
                            content: note,
                            updated_at: new Date(),
                        });
                } else {
                    await StoreDB('notes').insert({
                        content: note,
                        updated_at: new Date(),
                        created_at: new Date(),
                    });
                }

                try {
                    await logSyncChange({
                        table_name: 'notes',
                        record_key: 'user_note',
                        action: existingNote ? 'updated' : 'created',
                        payload: {
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
