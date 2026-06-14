import { StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

/**
 * `game_lives` tracks each life lost across all game types (shared 7-life pool).
 * `life_lost_at` is an ISO8601 UTC string and doubles as the sync record_key.
 * The backend stores it as `life_key` (full precision) alongside a truncated
 * `life_lost_at` MySQL timestamp — applyPullData reconciles the two. recovered=1
 * is permanent (a life that has recovered after the 2h timer). Mirrors mobile.
 */
export default async () => {
    try {
        const exists = await StoreDB.schema.hasTable('game_lives');
        if (!exists) {
            await StoreDB.schema.createTable('game_lives', (table) => {
                table.increments('id').primary();
                table.string('life_lost_at').notNullable();
                table.integer('recovered').defaultTo(0);
                table.string('created_at').notNullable();
            });
        }
    } catch (e) {
        Log.error('[game_lives migration]', e);
    }
};
