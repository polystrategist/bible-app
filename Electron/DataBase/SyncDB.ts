import { StoreDB } from './DataBase';

export type SyncLogEntry = {
    id?: number;
    table_name: string;
    record_key: string;
    action: 'created' | 'updated' | 'deleted';
    payload: any;
    synced: 0 | 1;
    created_at?: Date;
    updated_at?: Date;
};

export type SyncSetting = {
    id?: number;
    key: string;
    value: any;
    created_at?: Date;
    updated_at?: Date;
};

/**
 * Log a data change for sync tracking
 */
export async function logSyncChange(entry: SyncLogEntry): Promise<{ action: string; id: number }> {
    const now = new Date();
    const data = {
        table_name: entry.table_name,
        record_key: entry.record_key,
        action: entry.action,
        payload: entry.payload,
        synced: 0,
        created_at: now,
        updated_at: now,
    };

    const id = await StoreDB('sync_logs').insert(data);
    return { action: 'logged', id: id[0] };
}

/**
 * Get all unsynced changes
 */
export async function getUnsyncedChanges(): Promise<SyncLogEntry[]> {
    return await StoreDB('sync_logs')
        .select()
        .where('synced', 0)
        .orderBy('created_at', 'asc');
}

/**
 * Mark changes as synced
 */
export async function markAsSynced(ids: number[]): Promise<void> {
    await StoreDB('sync_logs')
        .whereIn('id', ids)
        .update({ synced: 1, updated_at: new Date() });
}

/**
 * Get changes for a specific table
 */
export async function getTableChanges(tableName: string, synced?: number): Promise<SyncLogEntry[]> {
    const query = StoreDB('sync_logs').where('table_name', tableName);
    if (synced !== undefined) {
        query.where('synced', synced);
    }
    return await query.orderBy('created_at', 'desc');
}

/**
 * Clear old synced changes (cleanup)
 */
export async function clearOldSyncedChanges(daysOld: number = 30): Promise<void> {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - daysOld);
    
    await StoreDB('sync_logs')
        .where('synced', 1)
        .where('created_at', '<', cutoffDate.toISOString())
        .del();
}

/**
 * Get sync setting value
 */
export async function getSyncSetting(key: string): Promise<any> {
    const setting = await StoreDB('sync_settings').where('key', key).first();
    return setting ? setting.value : null;
}

/**
 * Update or create sync setting
 */
export async function setSyncSetting(key: string, value: any): Promise<void> {
    const existing = await StoreDB('sync_settings').where('key', key).first();
    
    if (existing) {
        await StoreDB('sync_settings')
            .where('key', key)
            .update({ value, updated_at: new Date() });
    } else {
        await StoreDB('sync_settings').insert({
            key,
            value,
            created_at: new Date(),
            updated_at: new Date(),
        });
    }
}

/**
 * Get last sync timestamp
 */
export async function getLastSyncTimestamp(): Promise<string> {
    return await getSyncSetting('last_sync_timestamp') || '0';
}

/**
 * Update last sync timestamp
 */
export async function updateLastSyncTimestamp(timestamp: string): Promise<void> {
    await setSyncSetting('last_sync_timestamp', timestamp);
}
