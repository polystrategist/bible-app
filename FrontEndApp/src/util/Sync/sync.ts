import axios from 'axios';
import { useAuthStore } from '../../store/authStore';

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

let isSyncing = false;

/**
 * Push all unsynced local changes to the backend.
 * Returns the number of items synced, or -1 on failure.
 */
async function pushSync(token: string): Promise<number> {
    const unsyncedChanges: any[] = await window.browserWindow.getUnsyncedChanges();

    if (!unsyncedChanges.length) return 0;

    const payload = unsyncedChanges.map((entry: any) => ({
        table_name: entry.table_name,
        record_key: entry.record_key,
        action: entry.action,
        payload: typeof entry.payload === 'string' ? JSON.parse(entry.payload) : entry.payload,
        timestamp: entry.created_at,
    }));

    const response = await axios.post(
        `${API_BASE_URL}/sync`,
        { sync_logs: payload },
        { headers: { Authorization: `Bearer ${token}` } }
    );

    if (response.data.status === 'success') {
        const ids = unsyncedChanges.map((e: any) => e.id);
        await window.browserWindow.markAsSynced(ids);
        console.info(`[Sync] Pushed ${ids.length} change(s) to backend.`);
        return ids.length;
    }

    console.warn('[Sync] Push rejected by backend:', response.data);
    return -1;
}

/**
 * Pull remote changes since the last sync timestamp and apply them locally.
 */
async function pullSync(token: string): Promise<void> {
    const lastTimestamp: string = await window.browserWindow.getLastSyncTimestamp();

    const response = await axios.get(`${API_BASE_URL}/sync/pull`, {
        params: { since: lastTimestamp },
        headers: { Authorization: `Bearer ${token}` },
    });

    if (response.data.status !== 'success') return;

    const { bookmarks, highlights, clip_notes, prayer_lists, study_spaces, notes, last_sync_timestamp } = response.data;

    await window.browserWindow.applyPullData({
        study_spaces,
        bookmarks,
        highlights,
        clip_notes,
        prayer_lists,
        notes,
    });

    if (last_sync_timestamp) {
        await window.browserWindow.updateLastSyncTimestamp(last_sync_timestamp);
    }
}

/**
 * Run a full sync cycle: push local changes, then pull remote changes.
 * Safe to call repeatedly — skips if already running or conditions not met.
 */
export async function runSync(): Promise<void> {
    if (isSyncing) return;

    const authStore = useAuthStore();
    if (!authStore.syncEnabled || !authStore.isAuthenticated || !authStore.token) return;

    isSyncing = true;
    try {
        await pushSync(authStore.token);
        await pullSync(authStore.token);
    } catch (error: any) {
        const status = error?.response?.status;
        if (status === 401) {
            // Token expired or revoked — force logout so the user is prompted to log back in
            console.warn('[Sync] Token rejected (401) — logging out.');
            authStore.logout();
            return;
        }
        const data = error?.response?.data;
        console.error(`[Sync] Error (HTTP ${status ?? 'network'}):`, data ?? error?.message ?? error);
    } finally {
        isSyncing = false;
    }
}
