import { removeUniqueConstraint, StoreDB } from '../../../DataBase/DataBase';

export default async () => {
    await StoreDB.schema.hasTable('bookmarks').then(async (exists) => {
        try {
            if (!exists) {
                await StoreDB.schema
                    .createTable('bookmarks', function (table) {
                        table.increments('id').primary();
                        table.string('key');
                        table.integer('book_number');
                        table.integer('chapter');
                        table.integer('verse');
                        table.timestamps(true);
                    })
                    .then();
            } else {
                await removeUniqueConstraint('bookmarks', 'key');
            }
        } catch (e) {
            console.log(e);
        }
    });
};
