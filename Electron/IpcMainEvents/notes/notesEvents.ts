import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

export default () => {
    /** Returns all note rows ordered by created_at ASC */
    ipcMain.handle('getNotes', async () => {
        return await StoreDB('notes').orderBy('created_at', 'asc').select();
    });

    /** Upsert a single note row by note_id */
    ipcMain.handle(
        'upsertNote',
        async (event, { note_id, title, content }: { note_id: string; title: string; content: string }) => {
            try {
                const existing = await StoreDB('notes').where('note_id', note_id).first();
                const now = new Date();

                if (existing) {
                    await StoreDB('notes').where('note_id', note_id).update({
                        title,
                        content,
                        updated_at: now,
                    });
                } else {
                    await StoreDB('notes').insert({
                        note_id,
                        title,
                        content,
                        created_at: now,
                        updated_at: now,
                    });
                }

                await logSyncChange({
                    table_name: 'notes',
                    record_key: note_id,
                    action: existing ? 'updated' : 'created',
                    payload: { note_id, title, content },
                    synced: 0,
                });
            } catch (e) {
                Log.error('upsertNote error:', e);
            }
        }
    );

    /** Delete a single note row by note_id */
    ipcMain.handle(
        'deleteNote',
        async (event, { note_id }: { note_id: string }) => {
            try {
                await StoreDB('notes').where('note_id', note_id).delete();
                await logSyncChange({
                    table_name: 'notes',
                    record_key: note_id,
                    action: 'deleted',
                    payload: { note_id },
                    synced: 0,
                });
            } catch (e) {
                Log.error('deleteNote error:', e);
            }
        }
    );
};
