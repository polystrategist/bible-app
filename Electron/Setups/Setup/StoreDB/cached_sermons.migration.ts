import { StoreDB } from '../../../DataBase/DataBase';

/**
 * `cached_sermons` mirrors the top-N recent sermons from the backend so the
 * Sermons view has something to render when the server is unreachable.
 *
 * The table is replaced wholesale on every successful first-page fetch, so
 * there's no UNIQUE index beyond the primary key.
 */
export default async () => {
    await StoreDB.schema.hasTable('cached_sermons').then(async (exists) => {
        if (exists) return;
        try {
            await StoreDB.schema.createTable('cached_sermons', (table) => {
                table.integer('sermon_id').primary();
                table.integer('position').notNullable();
                table.text('payload').notNullable();
                table.string('cached_at').notNullable();
            });
        } catch (e) {
            console.log(e);
        }
    });
};
