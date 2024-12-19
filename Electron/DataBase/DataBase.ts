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
