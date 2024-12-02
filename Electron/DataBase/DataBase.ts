import { app } from 'electron';
import knex from 'knex';
import { isNightly } from '../config';
import UPath from 'upath';

const dataPath = UPath.join(app.getPath('appData'), !isNightly ? 'believers-sword' : 'believers-sword-nightly');

export const StoreDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\StoreDB\\Store.db`,
    },
});
