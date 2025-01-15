import { removeUniqueConstraint, StoreDB } from '../../../DataBase/DataBase';

export default async () => {
    await StoreDB.schema.hasTable('notes').then(async (exists) => {
        if (!exists) {
            await StoreDB.schema
                .createTable('notes', function (table) {
                    table.increments('id').primary();
                    table.integer('study_space_id').unique();
                    table.text('content');
                    table.timestamps(true);
                })
                .then();
        } else {
        }
    });
};
