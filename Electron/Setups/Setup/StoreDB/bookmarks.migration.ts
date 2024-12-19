import { StoreDB } from '../../../DataBase/DataBase';

export default async () => {
    await StoreDB.schema.hasTable('bookmarks').then(async (exists) => {
        if (!exists) {
            await StoreDB.schema
                .createTable('bookmarks', function (table) {
                    table.increments('id').primary();
                    table.integer('study_space_id');
                    table.string('key');
                    table.integer('book_number');
                    table.integer('chapter');
                    table.integer('verse');
                    table.timestamps(true);
                })
                .then();
        } else {
            // updates if table exists check if column study_space_id exists
            await StoreDB.schema.hasColumn('bookmarks', 'study_space_id').then(async (exists) => {
                if (!exists) {
                    await StoreDB.schema
                        .table('bookmarks', function (table) {
                            table.integer('study_space_id').after('id');
                        })
                        .then();
                }
            });

            // 
        }
    });
};
