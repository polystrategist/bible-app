import { StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

/**
 * `qa_group_progress` stores per-group Question & Answer progress (one row per
 * group_id). Synced via table_name 'qa_group_progress' (record_key
 * `qa_group_<id>`). high_score_percentage merges as MAX, is_completed as OR,
 * completed_at as the earliest timestamp. Mirrors mobile Store.db.
 */
export default async () => {
    try {
        const exists = await StoreDB.schema.hasTable('qa_group_progress');
        if (!exists) {
            await StoreDB.schema.createTable('qa_group_progress', (table) => {
                table.integer('group_id').primary();
                table.integer('is_completed').defaultTo(0);
                table.integer('high_score_percentage').defaultTo(0);
                table.integer('times_played').defaultTo(0);
                table.string('completed_at').nullable();
                table.string('updated_at').notNullable();
            });
        }
    } catch (e) {
        Log.error('[qa_group_progress migration]', e);
    }
};
