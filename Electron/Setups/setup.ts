import { setDefaultBible } from './Setup/SetDefaultBible';
import SetStoreDatabase from './Setup/SetStoreDatabase';
import { setStoreDB } from './Setup/SetStoreDB';
import { setDictionaryDB } from './Setup/SetDictionaryDb';

export const setupDefault = new Promise(async (resolve, reject): Promise<void> => {
    await setDefaultBible.catch((e) => reject(e));
    await setStoreDB.catch((e) => reject(e));
    await setDictionaryDB.catch((e) => reject(e));

    SetStoreDatabase();

    resolve('Default is Set up');
});
