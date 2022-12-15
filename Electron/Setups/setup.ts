import { setDefaultBible } from './Setup/SetDefaultBible';
import { setStoreDB } from './Setup/SetStoreDB';

export const setupDefault = new Promise(async (resolve, reject): Promise<void> => {
    await setDefaultBible.catch((e) => reject(e));
    await setStoreDB.catch((e) => reject(e));
    resolve('Default is Set up');
});
