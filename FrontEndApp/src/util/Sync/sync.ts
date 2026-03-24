import axios from 'axios';
import { useUserStore } from '../../store/userStore';

const API_BASE_URL = 'http://localhost:8000/api'; // Backend server URL

export interface SyncPayload {
    table_name: string;
    record_key: string;
    action: 'created' | 'updated' | 'deleted';
    payload: any;
    timestamp: string;
}

export interface SyncResponse {
    status: 'success' | 'error';
    message?: string;
    synced_items?: number;
}

/**
 * Sync data to backend server
 * Called when local data changes (create/update/delete)
 */
export async function syncData(payload: SyncPayload): Promise<SyncResponse> {
    const userStore = useUserStore();
    
    // Check if sync is enabled
    if (!userStore.syncData) {
        return { status: 'success', message: 'Sync disabled' };
    }

    // Check if user is authenticated
    if (!userStore.user || !userStore.user.token) {
        console.warn('User not authenticated, sync skipped');
        return { status: 'error', message: 'User not authenticated' };
    }

    try {
        const response = await axios.post(`${API_BASE_URL}/sync`, {
            sync_logs: [payload],
            user_id: userStore.user.id,
        }, {
            headers: {
                'Authorization': `Bearer ${userStore.user.token}`,
                'Content-Type': 'application/json',
            },
        });

        return response.data as SyncResponse;
    } catch (error: any) {
        console.error('Sync error:', error);
        return {
            status: 'error',
            message: error.response?.data?.message || error.message,
        };
    }
}

/**
 * Batch sync multiple changes
 */
export async function batchSyncData(payloads: SyncPayload[]): Promise<SyncResponse> {
    const userStore = useUserStore();
    
    if (!userStore.syncData || !userStore.user || !userStore.user.token) {
        return { status: 'success', message: 'Sync disabled or not authenticated' };
    }

    try {
        const response = await axios.post(`${API_BASE_URL}/sync`, {
            sync_logs: payloads,
            user_id: userStore.user.id,
        }, {
            headers: {
                'Authorization': `Bearer ${userStore.user.token}`,
                'Content-Type': 'application/json',
            },
        });

        return response.data as SyncResponse;
    } catch (error: any) {
        console.error('Batch sync error:', error);
        return {
            status: 'error',
            message: error.response?.data?.message || error.message,
        };
    }
}

/**
 * Pull changes from backend (download sync data)
 */
export async function pullSyncData(lastSyncTimestamp?: string): Promise<any> {
    const userStore = useUserStore();
    
    if (!userStore.syncData || !userStore.user || !userStore.user.token) {
        return { status: 'error', message: 'Sync disabled or not authenticated' };
    }

    try {
        const response = await axios.get(`${API_BASE_URL}/sync/pull`, {
            params: {
                since: lastSyncTimestamp || '0',
            },
            headers: {
                'Authorization': `Bearer ${userStore.user.token}`,
                'Content-Type': 'application/json',
            },
        });

        return response.data;
    } catch (error: any) {
        console.error('Pull sync error:', error);
        return {
            status: 'error',
            message: error.response?.data?.message || error.message,
        };
    }
}

/**
 * Trigger sync for specific data types
 */
export async function triggerSync(
    tableName: string,
    recordKey: string,
    action: 'created' | 'updated' | 'deleted',
    payload: any
): Promise<void> {
    // This will be called from IPC handlers after local DB operations
    const syncPayload: SyncPayload = {
        table_name: tableName,
        record_key: recordKey,
        action,
        payload,
        timestamp: new Date().toISOString(),
    };

    // Log to local sync_logs table via IPC
    await window.browserWindow.logSyncChange(syncPayload);
    
    // Send to backend
    await syncData(syncPayload);
}