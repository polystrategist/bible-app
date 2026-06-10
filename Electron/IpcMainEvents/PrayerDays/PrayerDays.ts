import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

/**
 * IPC handlers for prayer-streak days (`prayer_days`). One row per local
 * calendar date the user finished a prayer session. Created-only and
 * idempotent; the streak is computed on the client from the full day set.
 * Synced (table_name 'prayer_days', record_key = day).
 */

/** Local calendar date as YYYY-MM-DD. */
function todayKey(): string {
    const d = new Date();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${d.getFullYear()}-${mm}-${dd}`;
}

export default () => {
    // All recorded prayer days, newest first.
    ipcMain.handle('getPrayerDays', async () => {
        try {
            return await StoreDB('prayer_days').select().orderBy('day', 'desc');
        } catch (e) {
            Log.error('getPrayerDays failed:', e);
            return [];
        }
    });

    // Mark today as prayed and add `durationSeconds` to today's total prayer
    // time. Returns the day key recorded. Idempotent for the day itself; when
    // today already exists and durationSeconds is 0 it's a no-op (no sync log),
    // a positive duration accumulates and emits an `updated` log.
    ipcMain.handle('markPrayedToday', async (_event, durationSeconds: number = 0) => {
        try {
            const day = todayKey();
            const now = new Date().toISOString();
            const add = Math.max(0, Math.floor(durationSeconds || 0));
            const existing = await StoreDB('prayer_days').where({ day }).first();

            if (existing) {
                if (add <= 0) return day;
                const total = (existing.duration ?? 0) + add;
                const createdAt = existing.created_at ?? now;
                await StoreDB('prayer_days').where({ day }).update({ duration: total, updated_at: now });
                try {
                    await logSyncChange({
                        table_name: 'prayer_days',
                        record_key: day,
                        action: 'updated',
                        payload: { day, duration: total, created_at: createdAt, updated_at: now },
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('Failed to log sync change for prayer day:', e);
                }
                return day;
            }

            await StoreDB('prayer_days').insert({
                day,
                duration: add,
                created_at: now,
                updated_at: now,
            });

            try {
                await logSyncChange({
                    table_name: 'prayer_days',
                    record_key: day,
                    action: 'created',
                    payload: { day, duration: add, created_at: now, updated_at: now },
                    synced: 0,
                });
            } catch (e) {
                Log.error('Failed to log sync change for prayer day:', e);
            }
            return day;
        } catch (e) {
            Log.error('markPrayedToday failed:', e);
            return null;
        }
    });
};
