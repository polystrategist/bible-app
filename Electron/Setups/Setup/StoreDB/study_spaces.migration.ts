import { StoreDB } from '../../../DataBase/DataBase';
import { DAYJS } from '../../../util/dayjs';

export default async () => {
    await StoreDB.schema.hasTable('study_spaces').then(async (exists) => {
        try {
            if (!exists) {
                await StoreDB.schema
                    .createTable('study_spaces', function (table) {
                        table.increments('id').primary();
                        table.string('title').unique();
                        table.string('description');
                        table.boolean('is_selected').defaultTo(false);
                        table.timestamps(true);
                    })
                    .then();
            }

            // check if has data, if not create default data
            const count = await StoreDB('study_spaces')
                .count('id as rowCount')
                .then((data) => {
                    return data[0].rowCount;
                });

            if (count == 0) {
                // if their is no set study space, create a study space and add every bookmarks
                // clip notes, etc, as the study space
                const data = await StoreDB('study_spaces')
                    .insert([
                        {
                            title: 'My Study Space',
                            description: 'My Study Space',
                            is_selected: true,
                            created_at: DAYJS().utc().format(),
                            updated_at: DAYJS().utc().format(),
                        },
                    ])
                    .returning('*');

                const studySpaceId = data[0].id;

                // set bookmarks
                await StoreDB('bookmarks')
                    .update({
                        study_space_id: studySpaceId,
                    })
                    .where('study_space_id', null);

                // set clip notes
                await StoreDB('clip_notes')
                    .update({
                        study_space_id: studySpaceId,
                    })
                    .where('study_space_id', null);

                // set highlights
                await StoreDB('highlights')
                    .update({
                        study_space_id: studySpaceId,
                    })
                    .where('study_space_id', null);
            }
        } catch (e) {
            console.log(e);
        }
    });
};
