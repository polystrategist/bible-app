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
     * Does NOT log sync changes — this is a one-way remote→local write.
     */
    ipcMain.handle('applyPullData', async (event, pullData: {
        study_spaces?: any[];
        bookmarks?: any[];
        highlights?: any[];
        clip_notes?: any[];
        prayer_lists?: any[];
        notes?: any[];
    }) => {
        const now = new Date();

        async function getStudySpaceId(spaceName: string): Promise<number | null> {
            const space = await StoreDB('study_spaces').where('title', spaceName).first();
            return space?.id ?? null;
        }

        try {
            // 1. Study spaces
            for (const space of pullData.study_spaces ?? []) {
                const existing = await StoreDB('study_spaces').where('title', space.name).first();
                if (existing) {
                    await StoreDB('study_spaces').where('title', space.name)
                        .update({ description: space.description ?? null, updated_at: now });
                } else {
                    await StoreDB('study_spaces').insert({
                        title: space.name,
                        description: space.description ?? null,
                        is_selected: false,
                        created_at: now,
                        updated_at: now,
                    });
                }
            }

            // 2. Bookmarks
            for (const bm of pullData.bookmarks ?? []) {
                const spaceId = await getStudySpaceId(bm.study_space_name);
                if (spaceId == null) continue;
                const existing = await StoreDB('bookmarks').where({ key: bm.key, study_space_id: spaceId }).first();
                if (existing) {
                    await StoreDB('bookmarks').where({ key: bm.key, study_space_id: spaceId })
                        .update({ book_number: bm.book_number, chapter: bm.chapter, verse: bm.verse, updated_at: now });
                } else {
                    await StoreDB('bookmarks').insert({
                        key: bm.key, study_space_id: spaceId,
                        book_number: bm.book_number, chapter: bm.chapter, verse: bm.verse,
                        created_at: now, updated_at: now,
                    });
                }
            }

            // 3. Highlights
            for (const hl of pullData.highlights ?? []) {
                const spaceId = await getStudySpaceId(hl.study_space_name);
                if (spaceId == null) continue;
                const existing = await StoreDB('highlights').where({ key: hl.key, study_space_id: spaceId }).first();
                if (existing) {
                    await StoreDB('highlights').where({ key: hl.key, study_space_id: spaceId })
                        .update({ book_number: hl.book_number, chapter: hl.chapter, verse: hl.verse, content: hl.content, updated_at: now });
                } else {
                    await StoreDB('highlights').insert({
                        key: hl.key, study_space_id: spaceId,
                        book_number: hl.book_number, chapter: hl.chapter, verse: hl.verse, content: hl.content,
                        created_at: now, updated_at: now,
                    });
                }
            }

            // 4. Clip notes
            for (const cn of pullData.clip_notes ?? []) {
                const spaceId = await getStudySpaceId(cn.study_space_name);
                if (spaceId == null) continue;
                const existing = await StoreDB('clip_notes').where({ key: cn.key, study_space_id: spaceId }).first();
                if (existing) {
                    await StoreDB('clip_notes').where({ key: cn.key, study_space_id: spaceId })
                        .update({ book_number: cn.book_number, chapter: cn.chapter, verse: cn.verse, content: cn.content, color: cn.color, updated_at: now });
                } else {
                    await StoreDB('clip_notes').insert({
                        key: cn.key, study_space_id: spaceId,
                        book_number: cn.book_number, chapter: cn.chapter, verse: cn.verse,
                        content: cn.content, color: cn.color ?? '#FFD700',
                        created_at: now, updated_at: now,
                    });
                }
            }

            // 5. Prayer lists
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

            // 6. Notes (keyed by study_space_id, one note per space)
            for (const note of pullData.notes ?? []) {
                const spaceId = await getStudySpaceId(note.study_space_name);
                if (spaceId == null) continue;
                const existing = await StoreDB('notes').where('study_space_id', spaceId).first();
                if (existing) {
                    await StoreDB('notes').where('study_space_id', spaceId)
                        .update({ content: note.content, updated_at: now });
                } else {
                    await StoreDB('notes').insert({
                        study_space_id: spaceId, content: note.content,
                        created_at: now, updated_at: now,
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
