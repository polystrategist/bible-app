import { app } from 'electron';
import knex from 'knex';
import { isNightly } from '../../config';
const dataPath = app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = dataPath + `\\StoreDB\\Store.db`;
const StoreDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: filePath,
    },
});

export default async () => {
    // setup clip_notes
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
        }
    });
};
