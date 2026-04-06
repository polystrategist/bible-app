import { ipcMain, BrowserWindow } from 'electron';
import Log from 'electron-log';
import {
    logSyncChange,
    getUnsyncedChanges,
    markAsSynced,
    getSyncSetting,
    setSyncSetting,
    getLastSyncTimestamp,
    updateLastSyncTimestamp,
    SyncLogEntry,
} from '../../DataBase/SyncDB';
import { StoreDB } from '../../DataBase/DataBase';

/**
 * IPC Handlers for Sync Operations
 */
export const SyncHandlers = (win: BrowserWindow) => {

    /**
     * Log a sync change to the local database
     */
    ipcMain.handle(
        'logSyncChange',
        async (event, entry: SyncLogEntry) => {
            try {
                const result = await logSyncChange(entry);
                return result;
            } catch (error) {
                Log.error('Failed to log sync change:', error);
                throw error;
            }
        }
    );

    /**
     * Get all unsynced changes
     */
    ipcMain.handle('getUnsyncedChanges', async () => {
        try {
            return await getUnsyncedChanges();
        } catch (error) {
            Log.error('Failed to get unsynced changes:', error);
            return [];
        }
    });

    /**
     * Mark changes as synced after successful backend sync
     */
    ipcMain.handle('markAsSynced', async (event, ids: number[]) => {
        try {
            await markAsSynced(ids);
            return { success: true };
        } catch (error) {
            Log.error('Failed to mark as synced:', error);
            throw error;
        }
    });

    /**
     * Get last sync timestamp
     */
    ipcMain.handle('getLastSyncTimestamp', async () => {
        try {
            return await getLastSyncTimestamp();
        } catch (error) {
            Log.error('Failed to get last sync timestamp:', error);
            return '0';
        }
    });

    /**
     * Update last sync timestamp
     */
    ipcMain.handle('updateLastSyncTimestamp', async (event, timestamp: string) => {
        try {
            await updateLastSyncTimestamp(timestamp);
            return { success: true };
        } catch (error) {
            Log.error('Failed to update last sync timestamp:', error);
            throw error;
        }
    });

    /**
     * Get sync setting
     */
    ipcMain.handle('getSyncSetting', async (event, key: string) => {
        try {
            return await getSyncSetting(key);
        } catch (error) {
            Log.error('Failed to get sync setting:', error);
            return null;
        }
    });

    /**
     * Set sync setting
     */
    ipcMain.handle('setSyncSetting', async (event, key: string, value: any) => {
        try {
            await setSyncSetting(key, value);
            return { success: true };
        } catch (error) {
            Log.error('Failed to set sync setting:', error);
            throw error;
        }
    });

    /**
     * Apply pulled data from the server to local SQLite tables.
     * Does NOT log sync changes — this is a one-way remote->local write.
     */
    ipcMain.handle('applyPullData', async (event, pullData: {
        sync_logs?: any[];
        bookmarks?: any[];
        highlights?: any[];
        clip_notes?: any[];
        prayer_lists?: any[];
        notes?: any[];
    }) => {
        const now = new Date();

        try {
            // 0. Process deletions from sync_logs
            for (const log of pullData.sync_logs ?? []) {
                if (log.action !== 'deleted') continue;
                const key: string | undefined = log.record_key;
                if (!key) continue;
                switch (log.table_name) {
                    case 'bookmarks':
                        await StoreDB('bookmarks').where({ key }).delete();
                        break;
                    case 'highlights':
                        await StoreDB('highlights').where({ key }).delete();
                        break;
                    case 'clip_notes':
                        await StoreDB('clip_notes').where({ key }).delete();
                        break;
                    case 'prayer_lists':
                        await StoreDB('prayer_lists').where({ key }).delete();
                        break;
                    case 'notes':
                        await StoreDB('notes').where('note_id', key).delete();
                        break;
                }
            }

            // 1. Bookmarks
            for (const bm of pullData.bookmarks ?? []) {
                const existing = await StoreDB('bookmarks').where({ key: bm.key }).first();
                if (existing) {
                    await StoreDB('bookmarks').where({ key: bm.key })
                        .update({ book_number: bm.book_number, chapter: bm.chapter, verse: bm.verse, updated_at: now });
                } else {
                    await StoreDB('bookmarks').insert({
                        key: bm.key,
                        book_number: bm.book_number, chapter: bm.chapter, verse: bm.verse,
                        created_at: now, updated_at: now,
                    });
                }
            }

            // 2. Highlights
            for (const hl of pullData.highlights ?? []) {
                const existing = await StoreDB('highlights').where({ key: hl.key }).first();
                if (existing) {
                    await StoreDB('highlights').where({ key: hl.key })
                        .update({ book_number: hl.book_number, chapter: hl.chapter, verse: hl.verse, content: hl.content, updated_at: now });
                } else {
                    await StoreDB('highlights').insert({
                        key: hl.key,
                        book_number: hl.book_number, chapter: hl.chapter, verse: hl.verse, content: hl.content,
                        created_at: now, updated_at: now,
                    });
                }
            }

            // 3. Clip notes
            for (const cn of pullData.clip_notes ?? []) {
                const existing = await StoreDB('clip_notes').where({ key: cn.key }).first();
                if (existing) {
                    await StoreDB('clip_notes').where({ key: cn.key })
                        .update({ book_number: cn.book_number, chapter: cn.chapter, verse: cn.verse, content: cn.content, color: cn.color, updated_at: now });
                } else {
                    await StoreDB('clip_notes').insert({
                        key: cn.key,
                        book_number: cn.book_number, chapter: cn.chapter, verse: cn.verse,
                        content: cn.content, color: cn.color ?? '#FFD26A',
                        created_at: now, updated_at: now,
                    });
                }
            }

            // 4. Prayer lists
            for (const pl of pullData.prayer_lists ?? []) {
                const existing = await StoreDB('prayer_lists').where('key', pl.key).first();
                if (existing) {
                    await StoreDB('prayer_lists').where('key', pl.key)
                        .update({ title: pl.title, content: pl.content, group: pl.group, index: pl.index, status: pl.status, updated_at: now });
                } else {
                    await StoreDB('prayer_lists').insert({
                        key: pl.key, title: pl.title, content: pl.content,
                        group: pl.group, index: pl.index, status: pl.status,
                        created_at: now, updated_at: now,
                    });
                }
            }

            // 5. Notes (one row per note, keyed by note_id)
            for (const note of pullData.notes ?? []) {
                const noteId = note.note_id;
                if (!noteId) continue;
                const existing = await StoreDB('notes').where('note_id', noteId).first();
                if (existing) {
                    await StoreDB('notes').where('note_id', noteId)
                        .update({ title: note.title ?? '', content: note.content ?? '', updated_at: now });
                } else {
                    await StoreDB('notes').insert({
                        note_id: noteId,
                        title: note.title ?? '',
                        content: note.content ?? '',
                        created_at: now,
                        updated_at: now,
                    });
                }
            }

            return { success: true };
        } catch (error) {
            Log.error('Failed to apply pull data:', error);
            return { success: false, error: String(error) };
        }
    });
};
