import axios from 'axios';
import { useAuthStore } from '../../store/authStore';
import useNoteStore from '../../store/useNoteStore';
import { useBookmarkStore } from '../../store/bookmark';
import { usePrayerListStore } from '../../store/prayerListStore';
import { usePrayerStreakStore } from '../../store/prayerStreakStore';
import { useBibleStore } from '../../store/BibleStore';
import { useClipNoteStore } from '../../store/ClipNotes';
import { useConversationStore } from '../../store/conversationStore';

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

    const ALLOWED_TABLES = ['bookmarks', 'highlights', 'clip_notes', 'prayer_lists', 'prayer_days', 'notes', 'sermon_favorites', 'ai_conversations'];
    const ALLOWED_ACTIONS = ['created', 'updated', 'deleted'];

    // Discard legacy entries: no record_key, unknown table name, or unknown action.
    // These are leftovers from old app versions and would cause the entire push to fail.
    const stale = unsyncedChanges.filter((e: any) =>
        !e.record_key ||
        !ALLOWED_TABLES.includes(e.table_name) ||
        !ALLOWED_ACTIONS.includes(e.action)
    );
    if (stale.length) {
        console.info(`[Sync] Discarding ${stale.length} stale/unknown sync_log entry(ies).`);
        await window.browserWindow.markAsSynced(stale.map((e: any) => e.id));
    }

    const valid = unsyncedChanges.filter((e: any) =>
        !!e.record_key &&
        ALLOWED_TABLES.includes(e.table_name) &&
        ALLOWED_ACTIONS.includes(e.action)
    );
    if (!valid.length) return 0;

    // The backend rejects batches larger than 500, so push in small chunks.
    // Each batch is marked synced as it succeeds, so a large offline backlog
    // drains incrementally and progress survives a mid-way failure.
    const BATCH_SIZE = 150;
    let totalSynced = 0;

    for (let i = 0; i < valid.length; i += BATCH_SIZE) {
        const batch = valid.slice(i, i + BATCH_SIZE);
        const payload = batch.map((entry: any) => ({
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

        if (response.data.status !== 'success') {
            console.warn('[Sync] Push rejected by backend:', response.data);
            return totalSynced > 0 ? totalSynced : -1;
        }

        const failedKeys: string[] = response.data.failed_keys ?? [];
        const syncedEntries = failedKeys.length
            ? batch.filter((e: any) => !failedKeys.includes(e.record_key))
            : batch;

        if (syncedEntries.length) {
            const ids = syncedEntries.map((e: any) => e.id);
            await window.browserWindow.markAsSynced(ids);
            totalSynced += syncedEntries.length;
        }

        if (failedKeys.length) {
            console.warn(`[Sync] ${failedKeys.length} key(s) failed:`, failedKeys);
        }
    }

    console.info(`[Sync] Pushed ${totalSynced} change(s) to backend.`);
    return totalSynced;
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

        const { sync_logs, bookmarks, highlights, clip_notes, prayer_lists, prayer_days, notes, sermon_favorites, ai_conversations, settings, has_more, next_cursor, last_sync_timestamp } = response.data;
        const authStore = useAuthStore();

        await window.browserWindow.applyPullData({
            sync_logs,
            bookmarks,
            highlights,
            clip_notes,
            prayer_lists,
            prayer_days,
            notes,
            sermon_favorites,
            ai_conversations,
            settings,
        });

        if (settings && !authStore.pendingSettingsUpdate) {
            authStore.remoteSettings = settings;
        }

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
 * Reload all Pinia stores that mirror pulled data so the UI reflects what was
 * just written to SQLite by applyPullData.
 */
function reloadStoresAfterPull() {
    useNoteStore().loadNote();
    useBookmarkStore().getBookmarks();
    usePrayerListStore().loadPrayerLists();
    usePrayerStreakStore().loadDays();
    useBibleStore().getChapterHighlights();
    useClipNoteStore().getClipNotes();
    useConversationStore().loadConversations();
}

/**
 * Debounced sync — resets a 3-second timer on each call, fires once after
 * the user stops making changes. Pushes local changes only — no pull,
 * no loadNote, so active editing is never interrupted.
 */
/** Clear exponential backoff so the next sync attempt runs immediately. */
export function resetSyncBackoff(): void {
    consecutiveFailures = 0;
    backoffUntil = 0;
}

export function debouncedRunSync(): void {
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        debounceTimer = null;
        runPushSync();
    }, 3_000);
}

/**
 * Push-only sync — pushes local unsynced changes without pulling remote state.
 * Used by debouncedRunSync after user actions so active editing is never interrupted.
 */
export async function runPushSync(): Promise<void> {
    if (isSyncing) return;
    if (Date.now() < backoffUntil) return;

    const authStore = useAuthStore();
    // Sync is a paid feature — never run it for a Free account, even if a stale
    // `syncEnabled` preference is set before the tier resolves.
    if (!authStore.isSyncEntitled || !authStore.syncEnabled || !authStore.isAuthenticated || !authStore.token) return;

    isSyncing = true;
    try {
        await pushSync(authStore.token);
        consecutiveFailures = 0;
        backoffUntil = 0;
        authStore.loadLastSyncAt();
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
        console.error(`[Sync] Push error (HTTP ${status ?? 'network'}), retry in ${delaySec}s:`, data ?? error?.message ?? error);
    } finally {
        isSyncing = false;
    }
}

/**
 * Pull-only sync — fetches remote changes without pushing local ones.
 * Used by the periodic timer so the desktop never auto-pushes without user action.
 */
export async function runPullSync(): Promise<void> {
    if (isSyncing) return;
    if (Date.now() < backoffUntil) return;

    const authStore = useAuthStore();
    // Sync is a paid feature — never run it for a Free account, even if a stale
    // `syncEnabled` preference is set before the tier resolves.
    if (!authStore.isSyncEntitled || !authStore.syncEnabled || !authStore.isAuthenticated || !authStore.token) return;

    isSyncing = true;
    try {
        await pullSync(authStore.token);
        consecutiveFailures = 0;
        backoffUntil = 0;
        authStore.loadLastSyncAt();
        reloadStoresAfterPull();
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
    // Sync is a paid feature — never run it for a Free account, even if a stale
    // `syncEnabled` preference is set before the tier resolves.
    if (!authStore.isSyncEntitled || !authStore.syncEnabled || !authStore.isAuthenticated || !authStore.token) return;

    isSyncing = true;
    try {
        await pushSync(authStore.token);
        await pullSync(authStore.token);
        consecutiveFailures = 0;
        backoffUntil = 0;
        authStore.loadLastSyncAt();
        reloadStoresAfterPull();
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
