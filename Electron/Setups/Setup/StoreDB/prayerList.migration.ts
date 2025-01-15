import { StoreDB } from '../../../DataBase/DataBase';

export default async () => {
    await StoreDB.schema.hasTable('prayer_lists').then(async (exists) => {
        try {
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
            }
        } catch (e) {
            console.log(e);
        }
    });
};
