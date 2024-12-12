import { StoreDB } from '../../../DataBase/DataBase';
import { DAYJS } from '../../../util/dayjs';

export default async () => {
    await StoreDB.schema.hasTable('study_spaces').then(async (exists) => {
        if (!exists) {
            await StoreDB.schema
                .createTable('study_spaces', function (table) {
                    table.increments('id').primary();
                    table.string('title').unique();
                    table.string('description');
                    table.timestamps(true);
                })
                .then();
        } else {
            // check if has data, if not create default data
            const count = await StoreDB('study_spaces')
                .count('id as rowCount')
                .then((data) => {
                    return data[0].rowCount;
                });

            if (count == 0) {
                await StoreDB('study_spaces').insert([
                    {
                        title: 'My Study Space',
                        description: 'My Study Space',
                        created_at: DAYJS().utc().format(),
                        updated_at: DAYJS().utc().format(),
                    },
                ]);
            }
        }
    });
};
