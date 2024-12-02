import { StoreDB } from '../../../DataBase/DataBase';

export default async () => {
    await StoreDB.schema.hasTable('clip_notes').then(async (exists) => {
        if (!exists) {
            console.log('clip_notes Does Not Exist, Creating Table');
            await StoreDB.schema
                .createTable('clip_notes', function (table) {
                    table.increments('id').primary();
                    table.string('key').unique();
                    table.integer('book_number');
                    table.integer('chapter');
                    table.integer('verse');
                    table.string('content');
                    table.string('color', 50);
                    table.timestamps(true);
                })
                .then();
        } else {
            // updates if table exists check if column study_space_id exists
            await StoreDB.schema.hasColumn('clip_notes', 'study_space_id').then(async (exists) => {

                if (!exists) {
                    console.log('ada met kanu ti study_space_id');
                    await StoreDB.schema
                        .table('clip_notes', function (table) {
                            table.integer('study_space_id').after('id');
                        })
                        .then();
                }
            });
        }
    });
};
