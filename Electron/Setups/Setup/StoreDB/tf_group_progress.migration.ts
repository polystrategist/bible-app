import { StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

/**
 * `tf_group_progress` stores per-group True/False progress (one row per
 * group_id). Synced via table_name 'tf_group_progress' (record_key
 * `tf_group_<id>`). Same merge semantics as qa_group_progress. Mirrors mobile.
 */
export default async () => {
    try {
        const exists = await StoreDB.schema.hasTable('tf_group_progress');
        if (!exists) {
            await StoreDB.schema.createTable('tf_group_progress', (table) => {
                table.integer('group_id').primary();
                table.integer('is_completed').defaultTo(0);
                table.integer('high_score_percentage').defaultTo(0);
                table.integer('times_played').defaultTo(0);
                table.string('completed_at').nullable();
                table.string('updated_at').notNullable();
            });
        }
    } catch (e) {
        Log.error('[tf_group_progress migration]', e);
    }
};
