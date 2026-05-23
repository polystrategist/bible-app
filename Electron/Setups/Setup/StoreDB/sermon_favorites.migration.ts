import { StoreDB } from '../../../DataBase/DataBase';

/**
 * `sermon_favorites` holds sermons the user has starred. The full sermon
 * payload is stored alongside the id so favorited sermons remain readable
 * offline even if removed from the backend.
 *
 * Synced to the backend table `user_sermon_favorites` via sync_logs entries
 * with table_name = 'sermon_favorites' (record_key = sermon_id).
 */
export default async () => {
    await StoreDB.schema.hasTable('sermon_favorites').then(async (exists) => {
        if (exists) return;
        try {
            await StoreDB.schema.createTable('sermon_favorites', (table) => {
                table.integer('sermon_id').primary();
                table.text('payload').notNullable();
                table.string('created_at').notNullable();
                table.string('updated_at').notNullable();
            });
        } catch (e) {
            console.log(e);
        }
    });
};
