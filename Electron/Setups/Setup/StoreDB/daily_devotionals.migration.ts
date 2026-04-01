import { StoreDB } from '../../../DataBase/DataBase';
import { devotionalsData, DEVOTIONALS_DATA_VERSION } from './devotionals-data';
import { appConfig } from '../../../ElectronStore/Configuration';
import Log from 'electron-log';

const VERSION_KEY = 'devotionals_data_version';

export default async () => {
    try {
        const tableExists = await StoreDB.schema.hasTable('daily_devotionals');

        if (!tableExists) {
            await StoreDB.schema.createTable('daily_devotionals', (table) => {
                table.increments('id').primary();
                table.string('title').notNullable();
                table.integer('day_number').notNullable().unique();
                table.text('pause').notNullable();
                table.text('listen').notNullable();
                table.text('think').notNullable();
                table.text('pray').notNullable();
                table.text('go_action').notNullable();
                table.text('verses').notNullable().defaultTo('[]');
                table.timestamps(true);
            });
            Log.info('daily_devotionals table created');
        }

        // Skip if data version hasn't changed
        const lastVersion = appConfig.get(VERSION_KEY, 0) as number;
        if (lastVersion >= DEVOTIONALS_DATA_VERSION) return;

        // Upsert: insert new entries, update existing ones
        const existingRows = await StoreDB('daily_devotionals').select('day_number');
        const existingDays = new Set(existingRows.map((r: any) => r.day_number));

        const toInsert = devotionalsData.filter((d) => !existingDays.has(d.day_number));
        const toUpdate = devotionalsData.filter((d) => existingDays.has(d.day_number));

        if (toInsert.length > 0) {
            const batchSize = 50;
            for (let i = 0; i < toInsert.length; i += batchSize) {
                await StoreDB('daily_devotionals').insert(
                    toInsert.slice(i, i + batchSize)
                );
            }
            Log.info(`daily_devotionals: inserted ${toInsert.length} new entries`);
        }

        if (toUpdate.length > 0) {
            for (const entry of toUpdate) {
                await StoreDB('daily_devotionals')
                    .where('day_number', entry.day_number)
                    .update({
                        title: entry.title,
                        pause: entry.pause,
                        listen: entry.listen,
                        think: entry.think,
                        pray: entry.pray,
                        go_action: entry.go_action,
                        verses: entry.verses,
                    });
            }
            Log.info(`daily_devotionals: updated ${toUpdate.length} existing entries`);
        }

        appConfig.set(VERSION_KEY, DEVOTIONALS_DATA_VERSION);
    } catch (e) {
        Log.error('daily_devotionals migration error:', e);
    }
};
