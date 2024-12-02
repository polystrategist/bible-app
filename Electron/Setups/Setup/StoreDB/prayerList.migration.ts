import { StoreDB } from '../../../DataBase/DataBase';

export default async () => {
    await StoreDB.schema.hasTable('prayer_lists').then(async (exists) => {
        if (!exists) {
            console.log('prayer_lists Does Not Exist, Creating Table');
            await StoreDB.schema
                .createTable('prayer_lists', function (table) {
                    table.increments('id').primary();
                    table.string('key').unique();
                    table.string('title');
                    table.string('content');
                    table.string('group');
                    table.integer('index');
                    table.string('status').comment('ongoing,answered');
                    table.timestamps(true);
                })
                .then();
        } else {
            // updates if table exists check if column study_space_id exists
            await StoreDB.schema.hasColumn('prayer_lists', 'study_space_id').then(async (exists) => {
                if (!exists) {
                    await StoreDB.schema
                        .table('prayer_lists', function (table) {
                            table.integer('study_space_id').after('id');
                        })
                        .then();
                }
            });
        }
    });
};
