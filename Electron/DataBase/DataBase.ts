import { app } from 'electron';
import knex from 'knex';
import { isNightly } from '../config';
import UPath from 'upath';

const dataPath = UPath.join(
    app.getPath('appData'),
    !isNightly ? 'believers-sword' : 'believers-sword-nightly'
);

export const StoreDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\StoreDB\\Store.db`,
    },
});

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
        console.error('Error in updateOrCreate:', error);
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
            console.log(
                `The '${columnName}' column in table '${tableName}' has a unique constraint. Dropping it.`
            );
            await StoreDB.schema.alterTable(tableName, (table) => {
                table.dropUnique([columnName, uniqueIndexName]);
            });
            console.log(
                `Unique constraint removed from the '${columnName}' column in table '${tableName}'.`
            );
        } else {
            console.log(
                `The '${columnName}' column in table '${tableName}' does not have a unique constraint. Skipping.`
            );
        }
    } catch (error: any) {
        console.error(`Error checking or removing unique constraint: ${error.message}`);
    } finally {
        // await StoreDB.destroy(); // Close the database connection
    }
}
