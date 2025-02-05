import { ipcMain } from 'electron';
import { DictionaryDB } from '../../DataBase/DataBase';

export default () => {
    ipcMain.handle('searchDictionary', async (event, search: string) => {
        return await DictionaryDB.select('word')
            .from('entries')
            .groupBy('word')
            .where('word', 'like', `${search}%`)
            .limit(50)
            .then((row) => {
                return row;
            });
    });

    ipcMain.handle('getDefinitions', async (event, word: string) => {
        return await DictionaryDB.from('entries')
            .where('word', '=', word)
            .then((row) => {
                return row;
            });
    });
};
