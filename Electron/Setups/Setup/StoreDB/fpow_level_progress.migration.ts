import { StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

/**
 * `fpow_level_progress` stores per-level progress for 4 Pictures 1 Word (one row
 * per level_id). DEVICE-LOCAL ONLY on desktop: the backend's sync allowlist does
 * not include this table, so it is never pushed or pulled. Mirrors the mobile
 * Store.db schema for parity. `solved_at` non-null means the level is solved.
 */
export default async () => {
    try {
        const exists = await StoreDB.schema.hasTable('fpow_level_progress');
        if (!exists) {
            await StoreDB.schema.createTable('fpow_level_progress', (table) => {
                table.integer('level_id').primary();
                table.string('solved_at').nullable();
                table.string('hint_state').nullable();
            });
        }
    } catch (e) {
        Log.error('[fpow_level_progress migration]', e);
    }
};
