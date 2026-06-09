import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB, updateOrCreate } from '../../DataBase/DataBase';

/**
 * IPC handlers for the local AI insight/sermon cache (`ai_insights`).
 *
 * This is a device-local convenience cache only — it is never synced. Entries
 * older than 3 days are pruned (on every read and via an explicit prune call on
 * app start), so the cache stays small and content is periodically refreshed.
 */

const MAX_AGE_MS = 3 * 24 * 60 * 60 * 1000; // 3 days

interface InsightPayload {
    key: string;
    mode: string; // 'insight' | 'sermon'
    reference: string;
    version?: string | null;
    content: string;
}

async function pruneStale(): Promise<void> {
    const cutoff = new Date(Date.now() - MAX_AGE_MS).toISOString();
    await StoreDB('ai_insights').where('created_at', '<', cutoff).del();
}

export default () => {
    // Return a cached entry by key, or null when missing/stale. Prunes first so
    // an expired entry is never served (and the table is kept tidy).
    ipcMain.handle('getAiInsight', async (_event, key: string) => {
        try {
            await pruneStale();
            const row = await StoreDB('ai_insights').where({ key }).first();
            if (!row) return null;
            return {
                key: row.key,
                mode: row.mode,
                reference: row.reference,
                version: row.version ?? null,
                content: row.content,
                created_at: row.created_at,
            };
        } catch (e) {
            Log.error('getAiInsight failed:', e);
            return null;
        }
    });

    // Upsert by key. `created_at` is set to now on every write, so regenerating
    // refreshes both the content and its 3-day lifetime.
    ipcMain.handle('saveAiInsight', async (_event, payload: InsightPayload) => {
        try {
            await updateOrCreate(
                'ai_insights',
                { key: payload.key },
                {
                    mode: payload.mode,
                    reference: payload.reference,
                    version: payload.version ?? null,
                    content: payload.content,
                    created_at: new Date().toISOString(),
                }
            );
            return true;
        } catch (e) {
            Log.error('saveAiInsight failed:', e);
            return false;
        }
    });

    // Explicit prune (called on app start).
    ipcMain.handle('pruneAiInsights', async () => {
        try {
            await pruneStale();
            return true;
        } catch (e) {
            Log.error('pruneAiInsights failed:', e);
            return false;
        }
    });
};
