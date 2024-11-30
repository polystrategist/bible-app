import { setDefaultBible } from './Setup/SetDefaultBible';
import SetStoreDatabase from './Setup/SetStoreDatabase';
import { setStoreDB } from './Setup/SetStoreDB';
import { isNightly } from '../config';

export const setupDefault = new Promise(async (resolve, reject): Promise<void> => {
    const result = await setDefaultBible.catch((e) => reject(e));
    if (isNightly) console.log(result);
    const result2 = await setStoreDB.catch((e) => reject(e));
    if (isNightly) console.log(result2);

    SetStoreDatabase();
    resolve('Default is Set up');
});
