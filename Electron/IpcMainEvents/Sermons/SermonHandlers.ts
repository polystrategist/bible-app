import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

/**
 * IPC handlers for the sermons offline cache and sermon favorites.
 *
 * - `cached_sermons` is overwritten on each successful first-page fetch from
 *   the backend, so the Sermons view can fall back to local data when offline.
 *
 * - `sermon_favorites` stores user-starred sermons (with their full payload so
 *   they remain readable offline). Every mutation logs a sync_logs entry with
 *   table_name = 'sermon_favorites' so the backend `user_sermon_favorites`
 *   table can mirror it across devices.
 */
export const SermonHandlers = () => {
    ipcMain.handle('replaceCachedSermons', async (_event, sermons: any[]) => {
        try {
            const now = new Date().toISOString();
            await StoreDB.transaction(async (trx) => {
                await trx('cached_sermons').delete();
                if (!Array.isArray(sermons) || sermons.length === 0) return;
                const rows = sermons.slice(0, 10).map((s, i) => ({
                    sermon_id: s?.id,
                    position: i,
                    payload: JSON.stringify(s),
                    cached_at: now,
                })).filter((r) => typeof r.sermon_id === 'number');
                if (rows.length) await trx('cached_sermons').insert(rows);
            });
            return { success: true };
        } catch (error) {
            Log.error('replaceCachedSermons failed:', error);
            return { success: false, error: String(error) };
        }
    });

    ipcMain.handle('getCachedSermons', async () => {
        try {
            const rows = await StoreDB('cached_sermons').orderBy('position', 'asc');
            return rows.map((r: any) => JSON.parse(r.payload));
        } catch (error) {
            Log.error('getCachedSermons failed:', error);
            return [];
        }
    });

    ipcMain.handle('getSermonFavorites', async () => {
        try {
            const rows = await StoreDB('sermon_favorites').orderBy('created_at', 'desc');
            return rows.map((r: any) => JSON.parse(r.payload));
        } catch (error) {
            Log.error('getSermonFavorites failed:', error);
            return [];
        }
    });

    ipcMain.handle('getSermonFavoriteIds', async () => {
        try {
            const rows = await StoreDB('sermon_favorites').select('sermon_id');
            return rows.map((r: any) => r.sermon_id as number);
        } catch (error) {
            Log.error('getSermonFavoriteIds failed:', error);
            return [];
        }
    });

    ipcMain.handle('addSermonFavorite', async (_event, sermon: any) => {
        try {
            const id = sermon?.id;
            if (typeof id !== 'number') return { success: false };
            const now = new Date().toISOString();
            const payload = JSON.stringify(sermon);
            const existing = await StoreDB('sermon_favorites').where({ sermon_id: id }).first();
            if (existing) {
                await StoreDB('sermon_favorites').where({ sermon_id: id }).update({
                    payload,
                    updated_at: now,
                });
                await logSyncChange({
                    table_name: 'sermon_favorites',
                    record_key: String(id),
                    action: 'updated',
                    payload: { sermon_id: id },
                    synced: 0,
                });
            } else {
                await StoreDB('sermon_favorites').insert({
                    sermon_id: id,
                    payload,
                    created_at: now,
                    updated_at: now,
                });
                await logSyncChange({
                    table_name: 'sermon_favorites',
                    record_key: String(id),
                    action: 'created',
                    payload: { sermon_id: id },
                    synced: 0,
                });
            }
            return { success: true };
        } catch (error) {
            Log.error('addSermonFavorite failed:', error);
            return { success: false, error: String(error) };
        }
    });

    ipcMain.handle('removeSermonFavorite', async (_event, sermonId: number) => {
        try {
            await StoreDB('sermon_favorites').where({ sermon_id: sermonId }).delete();
            await logSyncChange({
                table_name: 'sermon_favorites',
                record_key: String(sermonId),
                action: 'deleted',
                payload: { sermon_id: sermonId },
                synced: 0,
            });
            return { success: true };
        } catch (error) {
            Log.error('removeSermonFavorite failed:', error);
            return { success: false, error: String(error) };
        }
    });
};
