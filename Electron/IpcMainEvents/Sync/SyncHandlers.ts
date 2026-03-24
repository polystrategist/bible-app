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
};
