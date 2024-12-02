import { StoreDB } from '../../../DataBase/DataBase';

export default async () => {
    await StoreDB.schema.hasTable('study_spaces').then(async (exists) => {
        if (!exists) {
            await StoreDB.schema
                .createTable('study_spaces', function (table) {
                    table.increments('id').primary();
                    table.string('title');
                    table.string('description');
                    table.timestamps(true);
                })
                .then();
        }
    });
};
