import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

/**
 * IPC handlers for devotion-streak days (`devotion_days`). One row per local
 * calendar date the user completed the Daily Devotion. Created-only and
 * idempotent; the streak is computed on the client from the full day set.
 * Synced (table_name 'devotion_days', record_key = day). Mirrors PrayerDays.
 */

/** Local calendar date as YYYY-MM-DD. */
function todayKey(): string {
    const d = new Date();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${d.getFullYear()}-${mm}-${dd}`;
}

export default () => {
    // All recorded devotion days, newest first.
    ipcMain.handle('getDevotionDays', async () => {
        try {
            return await StoreDB('devotion_days').select().orderBy('day', 'desc');
        } catch (e) {
            Log.error('getDevotionDays failed:', e);
            return [];
        }
    });

    // Mark today as a completed devotion (idempotent). Returns the day recorded.
    ipcMain.handle('markDevotionToday', async () => {
        try {
            const day = todayKey();
            const existing = await StoreDB('devotion_days').where({ day }).first();
            if (existing) return day;

            const now = new Date().toISOString();
            await StoreDB('devotion_days').insert({
                day,
                created_at: now,
                updated_at: now,
            });

            try {
                await logSyncChange({
                    table_name: 'devotion_days',
                    record_key: day,
                    action: 'created',
                    payload: { day, created_at: now, updated_at: now },
                    synced: 0,
                });
            } catch (e) {
                Log.error('Failed to log sync change for devotion day:', e);
            }
            return day;
        } catch (e) {
            Log.error('markDevotionToday failed:', e);
            return null;
        }
    });
};
