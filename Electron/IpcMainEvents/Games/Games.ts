import { ipcMain, app } from 'electron';
import path from 'path';
import Log from 'electron-log';
import { StoreDB, QaGamesDB, TfGamesDB, FpGamesDB } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

const MAX_LIVES = 7;
const RECOVERY_MS = 2 * 60 * 60 * 1000; // 2 hours, matches mobile games_service.dart

/**
 * Mark any lost lives whose 2h recovery window has elapsed as recovered, and
 * log a sync change for each so the recovery propagates to other devices.
 * recovered=1 is permanent.
 */
async function processRecoveries(): Promise<void> {
    const cutoff = new Date(Date.now() - RECOVERY_MS).toISOString();
    const rows = await StoreDB('game_lives')
        .where('recovered', 0)
        .where('life_lost_at', '<=', cutoff)
        .select('life_lost_at');

    if (rows.length === 0) return;

    await StoreDB('game_lives')
        .where('recovered', 0)
        .where('life_lost_at', '<=', cutoff)
        .update({ recovered: 1 });

    for (const row of rows) {
        try {
            await logSyncChange({
                table_name: 'game_lives',
                record_key: row.life_lost_at,
                action: 'updated',
                payload: { life_lost_at: row.life_lost_at, recovered: 1 },
                synced: 0,
            });
        } catch (e) {
            Log.error('[Games] logSync recovery failed:', e);
        }
    }
}

async function lostCount(): Promise<number> {
    const result = await StoreDB('game_lives').where('recovered', 0).count('id as cnt').first() as any;
    return Number(result?.cnt ?? 0);
}

/** Shared upsert for qa/tf group progress. Returns { newlyPassed }. */
async function saveGroupProgress(
    table: 'qa_group_progress' | 'tf_group_progress',
    recordKeyPrefix: 'qa_group_' | 'tf_group_',
    args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }
): Promise<{ newlyPassed: boolean }> {
    const { groupId, correctCount, totalCount, passingScore } = args;
    const percentage = totalCount === 0 ? 0 : Math.round((correctCount / totalCount) * 100);
    const passed = percentage >= passingScore;
    const now = new Date().toISOString();
    const existing = await StoreDB(table).where('group_id', groupId).first();

    if (!existing) {
        const row = {
            group_id: groupId,
            is_completed: passed ? 1 : 0,
            high_score_percentage: percentage,
            times_played: 1,
            completed_at: passed ? now : null,
            updated_at: now,
        };
        await StoreDB(table).insert(row);
        await logSyncChange({
            table_name: table,
            record_key: `${recordKeyPrefix}${groupId}`,
            action: 'created',
            payload: row,
            synced: 0,
        });
        return { newlyPassed: passed };
    }

    const wasCompleted = Boolean(existing.is_completed);
    const newCompleted = wasCompleted || passed;
    const newScore = Math.max(existing.high_score_percentage ?? 0, percentage);
    // Keep the earliest completion time; set it the first time the group passes.
    const newCompletedAt = existing.completed_at ?? (passed ? now : null);
    const row = {
        group_id: groupId,
        is_completed: newCompleted ? 1 : 0,
        high_score_percentage: newScore,
        times_played: (existing.times_played ?? 0) + 1,
        completed_at: newCompletedAt,
        updated_at: now,
    };
    await StoreDB(table).where('group_id', groupId).update({
        is_completed: row.is_completed,
        high_score_percentage: row.high_score_percentage,
        times_played: row.times_played,
        completed_at: row.completed_at,
        updated_at: row.updated_at,
    });
    await logSyncChange({
        table_name: table,
        record_key: `${recordKeyPrefix}${groupId}`,
        action: 'updated',
        payload: row,
        synced: 0,
    });
    return { newlyPassed: passed && !wasCompleted };
}

export default function Games() {
    // ── Lives ────────────────────────────────────────────────────────────────

    ipcMain.handle('game:getLives', async () => {
        try {
            await processRecoveries();
            return Math.max(0, MAX_LIVES - (await lostCount()));
        } catch (e) {
            Log.error('[Games] game:getLives error:', e);
            return MAX_LIVES;
        }
    });

    ipcMain.handle('game:loseLife', async () => {
        try {
            await processRecoveries();
            const lost = await lostCount();
            if (lost >= MAX_LIVES) return 0;

            const lifeKey = new Date().toISOString();
            await StoreDB('game_lives').insert({
                life_lost_at: lifeKey,
                recovered: 0,
                created_at: lifeKey,
            });
            await logSyncChange({
                table_name: 'game_lives',
                record_key: lifeKey,
                action: 'created',
                payload: { life_lost_at: lifeKey, recovered: 0 },
                synced: 0,
            });
            return Math.max(0, MAX_LIVES - lost - 1);
        } catch (e) {
            Log.error('[Games] game:loseLife error:', e);
            return MAX_LIVES;
        }
    });

    ipcMain.handle('game:nextRecoveryAt', async () => {
        try {
            await processRecoveries();
            const row = await StoreDB('game_lives')
                .where('recovered', 0)
                .orderBy('life_lost_at', 'asc')
                .first();
            if (!row) return null;
            return new Date(new Date(row.life_lost_at).getTime() + RECOVERY_MS).toISOString();
        } catch (e) {
            Log.error('[Games] game:nextRecoveryAt error:', e);
            return null;
        }
    });

    ipcMain.handle('game:refillLives', async () => {
        try {
            const rows = await StoreDB('game_lives').where('recovered', 0).select('life_lost_at');
            await StoreDB('game_lives').where('recovered', 0).update({ recovered: 1 });
            for (const row of rows) {
                try {
                    await logSyncChange({
                        table_name: 'game_lives',
                        record_key: row.life_lost_at,
                        action: 'updated',
                        payload: { life_lost_at: row.life_lost_at, recovered: 1 },
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('[Games] logSync refill failed:', e);
                }
            }
        } catch (e) {
            Log.error('[Games] game:refillLives error:', e);
        }
    });

    // ── Q&A ────────────────────────────────────────────────────────────────

    ipcMain.handle('qa:getGroups', async () => {
        try {
            return await QaGamesDB('question_groups').orderBy('display_order', 'asc').select();
        } catch (e) {
            Log.error('[Games] qa:getGroups error:', e);
            return [];
        }
    });

    ipcMain.handle('qa:getQuestionsForGroup', async (_, groupId: number) => {
        try {
            const rows = await QaGamesDB('questions')
                .where('group_id', groupId)
                .orderByRaw('RANDOM()')
                .select();
            // `options` is stored as a JSON array string — parse for the renderer.
            return rows.map((q: any) => ({
                ...q,
                options: typeof q.options === 'string' ? JSON.parse(q.options) : q.options,
            }));
        } catch (e) {
            Log.error('[Games] qa:getQuestionsForGroup error:', e);
            return [];
        }
    });

    ipcMain.handle('qa:getAllGroupProgress', async () => {
        try {
            return await StoreDB('qa_group_progress').select();
        } catch (e) {
            Log.error('[Games] qa:getAllGroupProgress error:', e);
            return [];
        }
    });

    ipcMain.handle('qa:saveGroupProgress', async (_, args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }) => {
        try {
            return await saveGroupProgress('qa_group_progress', 'qa_group_', args);
        } catch (e) {
            Log.error('[Games] qa:saveGroupProgress error:', e);
            return { newlyPassed: false };
        }
    });

    // ── True/False ─────────────────────────────────────────────────────────

    ipcMain.handle('tf:getGroups', async () => {
        try {
            return await TfGamesDB('tf_groups').orderBy('display_order', 'asc').select();
        } catch (e) {
            Log.error('[Games] tf:getGroups error:', e);
            return [];
        }
    });

    ipcMain.handle('tf:getStatementsForGroup', async (_, groupId: number) => {
        try {
            return await TfGamesDB('tf_statements')
                .where('group_id', groupId)
                .orderByRaw('RANDOM()')
                .select();
        } catch (e) {
            Log.error('[Games] tf:getStatementsForGroup error:', e);
            return [];
        }
    });

    ipcMain.handle('tf:getAllGroupProgress', async () => {
        try {
            return await StoreDB('tf_group_progress').select();
        } catch (e) {
            Log.error('[Games] tf:getAllGroupProgress error:', e);
            return [];
        }
    });

    ipcMain.handle('tf:saveGroupProgress', async (_, args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }) => {
        try {
            return await saveGroupProgress('tf_group_progress', 'tf_group_', args);
        } catch (e) {
            Log.error('[Games] tf:saveGroupProgress error:', e);
            return { newlyPassed: false };
        }
    });

    // ── Four Pictures (device-local only — not synced) ───────────────────────

    ipcMain.handle('fp:getLevels', async () => {
        try {
            return await FpGamesDB('fpow_levels').orderBy('level_order', 'asc').select();
        } catch (e) {
            Log.error('[Games] fp:getLevels error:', e);
            return [];
        }
    });

    ipcMain.handle('fp:getSolvedLevelIds', async () => {
        try {
            const rows = await StoreDB('fpow_level_progress')
                .whereNotNull('solved_at')
                .select('level_id');
            return rows.map((r: any) => r.level_id as number);
        } catch (e) {
            Log.error('[Games] fp:getSolvedLevelIds error:', e);
            return [];
        }
    });

    ipcMain.handle('fp:markLevelSolved', async (_, levelId: number) => {
        try {
            const now = new Date().toISOString();
            const existing = await StoreDB('fpow_level_progress').where('level_id', levelId).first();
            if (existing) {
                await StoreDB('fpow_level_progress').where('level_id', levelId).update({ solved_at: now, hint_state: null });
            } else {
                await StoreDB('fpow_level_progress').insert({ level_id: levelId, solved_at: now, hint_state: null });
            }
            // No logSync: fpow_level_progress is local-only (backend rejects it).
        } catch (e) {
            Log.error('[Games] fp:markLevelSolved error:', e);
        }
    });

    ipcMain.handle('fp:getImagesBasePath', () => {
        return path.join(app.getPath('userData'), 'Games', 'fp_images');
    });
}
