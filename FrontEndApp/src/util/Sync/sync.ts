import axios from 'axios';
import { useAuthStore } from '../../store/authStore';
import useNoteStore from '../../store/useNoteStore';

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

let isSyncing = false;
let consecutiveFailures = 0;
let backoffUntil = 0;
let debounceTimer: ReturnType<typeof setTimeout> | null = null;

/**
 * Push all unsynced local changes to the backend.
 * Returns the number of items synced, or -1 on failure.
 */
async function pushSync(token: string): Promise<number> {
    const unsyncedChanges: any[] = await window.browserWindow.getUnsyncedChanges();

    if (!unsyncedChanges.length) return 0;

    // Discard legacy entries with no record_key (old single-blob note model)
    const stale = unsyncedChanges.filter((e: any) => !e.record_key);
    if (stale.length) {
        await window.browserWindow.markAsSynced(stale.map((e: any) => e.id));
    }

    const valid = unsyncedChanges.filter((e: any) => !!e.record_key);
    if (!valid.length) return 0;

    const payload = valid.map((entry: any) => ({
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
        const failedKeys: string[] = response.data.failed_keys ?? [];
        const syncedEntries = failedKeys.length
            ? valid.filter((e: any) => !failedKeys.includes(e.record_key))
            : valid;

        if (syncedEntries.length) {
            const ids = syncedEntries.map((e: any) => e.id);
            await window.browserWindow.markAsSynced(ids);
        }

        if (failedKeys.length) {
            console.warn(`[Sync] ${failedKeys.length} key(s) failed:`, failedKeys);
        }

        console.info(`[Sync] Pushed ${syncedEntries.length} change(s) to backend.`);
        return syncedEntries.length;
    }

    console.warn('[Sync] Push rejected by backend:', response.data);
    return -1;
}

/**
 * Pull remote changes since the last sync timestamp and apply them locally.
 * Handles paginated responses — keeps fetching while `has_more` is true.
 */
async function pullSync(token: string): Promise<void> {
    let since: string = await window.browserWindow.getLastSyncTimestamp();

    while (true) {
        const response = await axios.get(`${API_BASE_URL}/sync/pull`, {
            params: { since },
            headers: { Authorization: `Bearer ${token}` },
        });

        if (response.data.status !== 'success') return;

        const { bookmarks, highlights, clip_notes, prayer_lists, notes, has_more, next_cursor, last_sync_timestamp } = response.data;

        await window.browserWindow.applyPullData({
            bookmarks,
            highlights,
            clip_notes,
            prayer_lists,
            notes,
        });

        if (has_more && next_cursor) {
            since = next_cursor;
        } else {
            if (last_sync_timestamp) {
                await window.browserWindow.updateLastSyncTimestamp(last_sync_timestamp);
            }
            break;
        }
    }
}

/**
 * Debounced sync — resets a 3-second timer on each call, fires once after
 * the user stops making changes. Pushes local changes then pulls remote state.
 */
export function debouncedRunSync(): void {
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        debounceTimer = null;
        runSync();
    }, 3_000);
}

/**
 * Pull-only sync — fetches remote changes without pushing local ones.
 * Used by the periodic timer so the desktop never auto-pushes without user action.
 */
export async function runPullSync(): Promise<void> {
    if (isSyncing) return;
    if (Date.now() < backoffUntil) return;

    const authStore = useAuthStore();
    if (!authStore.syncEnabled || !authStore.isAuthenticated || !authStore.token) return;

    isSyncing = true;
    try {
        await pullSync(authStore.token);
        consecutiveFailures = 0;
        backoffUntil = 0;
        authStore.loadLastSyncAt();
        useNoteStore().loadNote();
    } catch (error: any) {
        const status = error?.response?.status;
        if (status === 401) {
            console.warn('[Sync] Token rejected (401) — logging out.');
            consecutiveFailures = 0;
            backoffUntil = 0;
            authStore.logout();
            return;
        }

        consecutiveFailures++;
        const delaySec = Math.min(300 * Math.pow(2, consecutiveFailures - 1), 3600);
        backoffUntil = Date.now() + delaySec * 1000;

        const data = error?.response?.data;
        console.error(`[Sync] Pull error (HTTP ${status ?? 'network'}), retry in ${delaySec}s:`, data ?? error?.message ?? error);
    } finally {
        isSyncing = false;
    }
}

/**
 * Full sync — push local changes then pull remote state.
 * Called by debouncedRunSync after user actions.
 */
export async function runSync(): Promise<void> {
    if (isSyncing) return;

    // Exponential backoff: skip this cycle if we're still in a cooldown period
    if (Date.now() < backoffUntil) return;

    const authStore = useAuthStore();
    if (!authStore.syncEnabled || !authStore.isAuthenticated || !authStore.token) return;

    isSyncing = true;
    try {
        await pushSync(authStore.token);
        await pullSync(authStore.token);
        consecutiveFailures = 0;
        backoffUntil = 0;
        authStore.loadLastSyncAt();
        useNoteStore().loadNote();
    } catch (error: any) {
        const status = error?.response?.status;
        if (status === 401) {
            console.warn('[Sync] Token rejected (401) — logging out.');
            consecutiveFailures = 0;
            backoffUntil = 0;
            authStore.logout();
            return;
        }

        consecutiveFailures++;
        // Backoff: 5min, 10min, 20min, capped at 60min
        const delaySec = Math.min(300 * Math.pow(2, consecutiveFailures - 1), 3600);
        backoffUntil = Date.now() + delaySec * 1000;

        const data = error?.response?.data;
        console.error(`[Sync] Error (HTTP ${status ?? 'network'}), retry in ${delaySec}s:`, data ?? error?.message ?? error);
    } finally {
        isSyncing = false;
    }
}
