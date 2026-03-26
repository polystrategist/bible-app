import { StoreDB } from '../../../DataBase/DataBase';

export default async () => {
    await StoreDB.schema.hasTable('sync_logs').then(async (exists: boolean) => {
        if (!exists) {
            await StoreDB.schema.createTable('sync_logs', function (table) {
                table.increments('id').primary();
                table.string('table_name').notNullable(); // e.g., 'bookmarks', 'highlights', 'prayer_lists'
                table.string('record_key').notNullable(); // Unique identifier for the record
                table.string('action').notNullable(); // 'created', 'updated', 'deleted'
                table.json('payload'); // The data that was changed
                table.integer('synced').defaultTo(0); // 0 = not synced, 1 = synced to backend
                table.timestamps(true);
                
                table.index(['table_name', 'synced']);
                table.index('created_at');
            });
        }
    });

    await StoreDB.schema.hasTable('sync_settings').then(async (exists: boolean) => {
        if (!exists) {
            await StoreDB.schema.createTable('sync_settings', function (table) {
                table.increments('id').primary();
                table.string('key').unique().notNullable();
                table.json('value');
                table.timestamps(true);
            });
        }
    });

    // Initialize default sync settings if not exists
    const existingSetting = await StoreDB('sync_settings').where('key', 'last_sync_timestamp').first();
    if (!existingSetting) {
        await StoreDB('sync_settings').insert({
            key: 'last_sync_timestamp',
            value: '0',
            created_at: new Date(),
            updated_at: new Date(),
        });
    }
};
