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

    // Purge sync_logs that were already pushed and are older than 7 days.
    (() => {
        const cutoff = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();
        StoreDB('sync_logs').where('synced', 1).where('created_at', '<', cutoff).delete()
            .catch((err: any) => Log.error('sync_logs cleanup failed:', err));
    })();

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
        prayer_days?: any[];
        devotion_days?: any[];
        notes?: any[];
        sermon_favorites?: any[];
        ai_conversations?: any[];
        game_lives?: any[];
        qa_group_progress?: any[];
        tf_group_progress?: any[];
    }) => {
        const now = new Date().toISOString();
        // Earlier of two nullable ISO timestamps (mirrors mobile _earliestTimestamp).
        const earliest = (a: string | null | undefined, b: string | null | undefined): string | null => {
            if (!a) return b ?? null;
            if (!b) return a ?? null;
            return a <= b ? a : b;
        };

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
                    case 'prayer_days':
                        await StoreDB('prayer_days').where({ day: key }).delete();
                        break;
                    case 'devotion_days':
                        await StoreDB('devotion_days').where({ day: key }).delete();
                        break;
                    case 'notes':
                        await StoreDB('notes').where('note_id', key).delete();
                        break;
                    case 'sermon_favorites': {
                        const id = Number(key);
                        if (!Number.isNaN(id)) {
                            await StoreDB('sermon_favorites').where({ sermon_id: id }).delete();
                        }
                        break;
                    }
                    case 'ai_conversations':
                        await StoreDB('ai_conversations').where({ id: key }).delete();
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
                // The authoritative original creation time, when the server has it.
                const clientCreatedAt = pl.client_created_at ?? null;
                const existing = await StoreDB('prayer_lists').where('key', pl.key).first();
                if (existing) {
                    const update: any = { title: pl.title, content: pl.content, group: pl.group, index: pl.index, status: pl.status, updated_at: now };
                    // Only heal created_at from the authoritative client value; never
                    // let a server insert-time overwrite a correct local created_at.
                    if (clientCreatedAt) update.created_at = clientCreatedAt;
                    await StoreDB('prayer_lists').where('key', pl.key).update(update);
                } else {
                    // New local row: prefer client created_at, fall back to server time, then now.
                    const createdAt = clientCreatedAt ?? pl.created_at ?? now;
                    await StoreDB('prayer_lists').insert({
                        key: pl.key, title: pl.title, content: pl.content,
                        group: pl.group, index: pl.index, status: pl.status,
                        created_at: createdAt, updated_at: now,
                    });
                }
            }

            // 4b. Prayer-streak days (union-merged). Per-day `duration` (total
            //     prayer seconds) is merged as a MAX so the larger total wins —
            //     idempotent, never double-counts on re-sync.
            for (const pd of pullData.prayer_days ?? []) {
                if (!pd.day) continue;
                const incoming = Number(pd.duration ?? 0) || 0;
                const existing = await StoreDB('prayer_days').where('day', pd.day).first();
                if (!existing) {
                    await StoreDB('prayer_days').insert({
                        day: pd.day,
                        duration: incoming,
                        created_at: pd.created_at ?? now,
                        updated_at: pd.updated_at ?? now,
                    });
                } else if (incoming > (existing.duration ?? 0)) {
                    await StoreDB('prayer_days').where('day', pd.day).update({ duration: incoming, updated_at: now });
                }
            }

            // 4c. Devotion-streak days (created-only, idempotent union)
            for (const dd of pullData.devotion_days ?? []) {
                if (!dd.day) continue;
                const existing = await StoreDB('devotion_days').where('day', dd.day).first();
                if (!existing) {
                    await StoreDB('devotion_days').insert({
                        day: dd.day,
                        created_at: dd.created_at ?? now,
                        updated_at: dd.updated_at ?? now,
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

            // 6. Sermon favorites — backend only stores sermon_id, so preserve
            //    any local payload. If we've never cached the sermon, insert a
            //    placeholder JSON that will be filled in next time the sermon
            //    is opened or appears in a fetched list.
            for (const fav of pullData.sermon_favorites ?? []) {
                const sermonId = fav?.sermon_id;
                if (typeof sermonId !== 'number') continue;
                const existing = await StoreDB('sermon_favorites').where({ sermon_id: sermonId }).first();
                if (existing) continue;
                await StoreDB('sermon_favorites').insert({
                    sermon_id: sermonId,
                    payload: JSON.stringify({ id: sermonId }),
                    created_at: now,
                    updated_at: now,
                });
            }

            // 7. AI conversations — keyed by the client conversation id. The
            //    server stores messages as a JSON string in `messages`; keep it
            //    verbatim so the renderer can parse it the same way it saved it.
            for (const conv of pullData.ai_conversations ?? []) {
                const id: string | undefined = conv?.conversation_id ?? conv?.id;
                if (!id) continue;
                const messages = typeof conv.messages === 'string'
                    ? conv.messages
                    : JSON.stringify(conv.messages ?? []);
                const title = conv.title ?? 'New chat';
                const existing = await StoreDB('ai_conversations').where({ id }).first();
                if (existing) {
                    await StoreDB('ai_conversations').where({ id })
                        .update({ title, messages, deleted: 0, updated_at: now });
                } else {
                    await StoreDB('ai_conversations').insert({
                        id, title, messages, deleted: 0,
                        created_at: now, updated_at: now,
                    });
                }
            }

            // 8. game_lives — the backend stores the full-precision `life_key`
            //    plus a truncated MySQL `life_lost_at`. Match on life_key; delete
            //    any phantom row that an earlier truncated value created, and
            //    never downgrade recovered=1 (mirrors mobile _applyPullGameLives).
            for (const life of pullData.game_lives ?? []) {
                const lifeKey: string | undefined =
                    (typeof life.life_key === 'string' && life.life_key.length > 0)
                        ? life.life_key
                        : (life.life_lost_at as string | undefined);
                if (!lifeKey) continue;

                const incomingRecovered = (life.recovered === true || life.recovered === 1) ? 1 : 0;

                const backendLifeLostAt: string | undefined = life.life_lost_at;
                if (backendLifeLostAt && backendLifeLostAt.length > 0 && backendLifeLostAt !== lifeKey) {
                    await StoreDB('game_lives').where('life_lost_at', backendLifeLostAt).delete();
                }

                const existing = await StoreDB('game_lives').where('life_lost_at', lifeKey).first();
                if (!existing) {
                    await StoreDB('game_lives').insert({
                        life_lost_at: lifeKey,
                        recovered: incomingRecovered,
                        created_at: now,
                    });
                } else if (incomingRecovered === 1 && !existing.recovered) {
                    await StoreDB('game_lives').where('life_lost_at', lifeKey).update({ recovered: 1 });
                }
            }

            // 9. qa_group_progress — upsert; high score MAX, is_completed OR,
            //    times_played MAX, completed_at earliest (mirrors mobile).
            for (const p of pullData.qa_group_progress ?? []) {
                if (p.group_id == null) continue;
                const incomingCompleted = (p.is_completed === true || p.is_completed === 1) ? 1 : 0;
                const incomingScore = Number(p.high_score_percentage ?? 0) || 0;
                const incomingPlayed = Number(p.times_played ?? 0) || 0;
                const existing = await StoreDB('qa_group_progress').where('group_id', p.group_id).first();
                if (!existing) {
                    await StoreDB('qa_group_progress').insert({
                        group_id: p.group_id,
                        is_completed: incomingCompleted,
                        high_score_percentage: incomingScore,
                        times_played: incomingPlayed,
                        completed_at: p.completed_at ?? null,
                        updated_at: now,
                    });
                } else {
                    await StoreDB('qa_group_progress').where('group_id', p.group_id).update({
                        is_completed: (existing.is_completed === 1 || incomingCompleted === 1) ? 1 : 0,
                        high_score_percentage: Math.max(existing.high_score_percentage ?? 0, incomingScore),
                        times_played: Math.max(existing.times_played ?? 0, incomingPlayed),
                        completed_at: earliest(existing.completed_at, p.completed_at),
                        updated_at: now,
                    });
                }
            }

            // 10. tf_group_progress — same merge semantics as qa_group_progress.
            for (const p of pullData.tf_group_progress ?? []) {
                if (p.group_id == null) continue;
                const incomingCompleted = (p.is_completed === true || p.is_completed === 1) ? 1 : 0;
                const incomingScore = Number(p.high_score_percentage ?? 0) || 0;
                const incomingPlayed = Number(p.times_played ?? 0) || 0;
                const existing = await StoreDB('tf_group_progress').where('group_id', p.group_id).first();
                if (!existing) {
                    await StoreDB('tf_group_progress').insert({
                        group_id: p.group_id,
                        is_completed: incomingCompleted,
                        high_score_percentage: incomingScore,
                        times_played: incomingPlayed,
                        completed_at: p.completed_at ?? null,
                        updated_at: now,
                    });
                } else {
                    await StoreDB('tf_group_progress').where('group_id', p.group_id).update({
                        is_completed: (existing.is_completed === 1 || incomingCompleted === 1) ? 1 : 0,
                        high_score_percentage: Math.max(existing.high_score_percentage ?? 0, incomingScore),
                        times_played: Math.max(existing.times_played ?? 0, incomingPlayed),
                        completed_at: earliest(existing.completed_at, p.completed_at),
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
