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
    await StoreDB.schema.hasTable('prayer_days').then(async (exists) => {
        if (exists) return;
        try {
            await StoreDB.schema.createTable('prayer_days', (table) => {
                table.string('day').primary();
                table.string('created_at').notNullable();
                table.string('updated_at').notNullable();
            });
        } catch (e) {
            Log.error(e);
        }
    });
};
