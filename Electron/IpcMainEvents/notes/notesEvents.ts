import { ipcMain } from 'electron';
import { StoreDB, updateOrCreate } from '../../DataBase/DataBase';

export default () => {
    ipcMain.handle('getNote', async (event, space_study_id: number) => {
        return await StoreDB.select().from('notes').where('study_space_id', space_study_id).first();
    });

    ipcMain.handle(
        'saveNote',
        async (event, { space_study_id, note }: { space_study_id: number; note: string }) => {
            try {
                await updateOrCreate(
                    'notes',
                    {
                        study_space_id: space_study_id,
                    },
                    {
                        content: note,
                        updated_at: new Date(),
                    }
                );
            } catch (e) {
                console.log(e);
            }
        }
    );
};
