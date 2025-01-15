import { removeUniqueConstraint, StoreDB } from '../../../DataBase/DataBase';

export default async () => {
    await StoreDB.schema.hasTable('highlights').then(async (exists) => {
        try {
            if (!exists) {
                await StoreDB.schema
                    .createTable('highlights', function (table) {
                        table.increments('id').primary();
                        table.integer('study_space_id');
                        table.string('key');
                        table.integer('book_number');
                        table.integer('chapter');
                        table.integer('verse');
                        table.string('content');
                        table.timestamps(true);
                    })
                    .then();
            } else {
                await removeUniqueConstraint('highlights', 'key');

                // updates if table exists check if column study_space_id exists
                await StoreDB.schema
                    .hasColumn('highlights', 'study_space_id')
                    .then(async (exists) => {
                        if (!exists) {
                            await StoreDB.schema
                                .table('highlights', function (table) {
                                    table.integer('study_space_id').after('id');
                                })
                                .then();
                        }
                    });
            }
        } catch (e) {
            console.log(e);
        }
    });
};
