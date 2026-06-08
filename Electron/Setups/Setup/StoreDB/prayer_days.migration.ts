import { StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

/**
 * `prayer_days` stores one row per local calendar date (YYYY-MM-DD) the user
 * finished a prayer session — the source for the prayer day-streak. Rows are
 * created-only and idempotent; across devices they merge as a union, so the
 * streak itself is computed client-side from the full day set. Synced via
 * table_name 'prayer_days' (record_key = day). Mirrors the mobile Store.db.
 */
export default async () => {
    try {
        const exists = await StoreDB.schema.hasTable('prayer_days');
        if (!exists) {
            // `duration` = total prayer time (seconds) accumulated that day,
            // synced as a per-day MAX. Mirrors the mobile Store.db schema.
            await StoreDB.schema.createTable('prayer_days', (table) => {
                table.string('day').primary();
                table.integer('duration').defaultTo(0);
                table.string('created_at').notNullable();
                table.string('updated_at').notNullable();
            });
            return;
        }
        // Existing table: add the duration column if it isn't there yet.
        const hasDuration = await StoreDB.schema.hasColumn('prayer_days', 'duration');
        if (!hasDuration) {
            await StoreDB.schema.alterTable('prayer_days', (table) => {
                table.integer('duration').defaultTo(0);
            });
        }
    } catch (e) {
        Log.error(e);
    }
};
