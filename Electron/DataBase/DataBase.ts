import { app } from 'electron';
import knex from 'knex';
import Log from 'electron-log';
import { setupPortableMode } from '../util/portable';


setupPortableMode();
const dataPath = app.getPath('userData');

export const StoreDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\StoreDB\\Store.db`,
    },
});

export const DictionaryDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\StoreDB\\Dictionary.db`,
    },
});

export const CrossReferencesDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\StoreDB\\cross_references.db`,
    },
});

export const DevotionalsDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\StoreDB\\devotionals.db`,
    },
});

// Strong's lexicon (read-only shipped content). Keyed on strong_number
// (e.g. "G2424", "H7225"). Seeded by SetStrongsDB.ts from defaults/Main.
export const StrongsDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\StoreDB\\strongs.db`,
    },
});

// Game content DBs (read-only seeded content). User data (lives, progress)
// lives in StoreDB. Seeded by SetGamesDB.ts into userData\Games\.
export const QaGamesDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\Games\\qa_games.db`,
    },
});

export const TfGamesDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\Games\\tf_games.db`,
    },
});

export const FpGamesDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\Games\\fp_games.db`,
    },
});

export const setDB = (pathOfDb: string) => {
    return knex({
        client: 'sqlite3',
        useNullAsDefault: false,
        connection: {
            filename: pathOfDb,
        },
    });
};

export async function updateOrCreate(
    tableName: string,
    whereCondition: { [key: string]: any },
    updateData: { [key: string]: any }
) {
    try {
        // Check if the record exists
        const existingRecord = await StoreDB(tableName).where(whereCondition).first();

        if (existingRecord) {
            // Update the record if it exists
            await StoreDB(tableName).where(whereCondition).update(updateData);
            return { action: 'updated', data: updateData };
        } else {
            // Create the record if it doesn't exist
            const newRecord = { ...whereCondition, ...updateData };
            await StoreDB(tableName).insert(newRecord);
            return { action: 'created', data: newRecord };
        }
    } catch (error) {
        Log.error('Error in updateOrCreate:', error);
        throw error;
    }
}

export async function removeUniqueConstraint(tableName: string, columnName: string) {
    try {
        // Check for unique constraint using PRAGMA
        const constraints = await StoreDB.raw(`PRAGMA index_list('${tableName}')`);
        const uniqueIndexes = constraints.filter((index: any) => index.unique);

        // Find if the column is part of a unique index
        let uniqueIndexName = null;
        for (const index of uniqueIndexes) {
            const indexInfo = await StoreDB.raw(`PRAGMA index_info('${index.name}')`);
            const columns = indexInfo.map((info: any) => info.name);
            if (columns.includes(columnName)) {
                uniqueIndexName = index.name;
                break;
            }
        }

        if (uniqueIndexName) {
            Log.info(
                `The '${columnName}' column in table '${tableName}' has a unique constraint. Dropping it.`
            );
            await StoreDB.schema.alterTable(tableName, (table) => {
                table.dropUnique([columnName, uniqueIndexName]);
            });
            Log.info(
                `Unique constraint removed from the '${columnName}' column in table '${tableName}'.`
            );
        } else {
            Log.info(
                `The '${columnName}' column in table '${tableName}' does not have a unique constraint. Skipping.`
            );
        }
    } catch (error: any) {
        Log.error(`Error checking or removing unique constraint: ${error.message}`);
    } finally {
        // await StoreDB.destroy(); // Close the database connection
    }
}
