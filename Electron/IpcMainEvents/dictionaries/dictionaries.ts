import { ipcMain } from 'electron';
import { DictionaryDB } from '../../DataBase/DataBase';

export default () => {
    ipcMain.handle('searchDictionary', async (event, search: string) => {
        const results = await DictionaryDB.select('word')
            .from('entries')
            .groupBy('word')
            .where('word', 'like', `${search}%`)
            .limit(50);
        return results;
    });

    ipcMain.handle('getDefinitions', async (event, word: string) => {
        const results = await DictionaryDB.from('entries')
            .where('word', '=', word);
        return results;
    });
};
