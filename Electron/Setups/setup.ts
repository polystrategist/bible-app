import { setDefaultBible } from './Setup/SetDefaultBible';
import SetStoreDatabase from './Setup/SetStoreDatabase';
import { setStoreDB } from './Setup/SetStoreDB';
import { setDictionaryDB } from './Setup/SetDictionaryDb';
import { setCrossReferencesDB } from './Setup/SetCrossReferencesDB';
import { setStrongsDB } from './Setup/SetStrongsDB';
import { setDevotionalsDB } from './Setup/SetDevotionalsDB';
import { setGamesDB } from './Setup/SetGamesDB';
import { createDatabaseIndexes } from './Setup/CreateDatabaseIndexes';

export const setupDefault = new Promise(async (resolve, reject): Promise<void> => {
    await setDefaultBible.catch((e) => reject(e));
    await setStoreDB.catch((e) => reject(e));
    await setDictionaryDB.catch((e) => reject(e));
    await setCrossReferencesDB.catch((e) => reject(e));
    await setStrongsDB.catch((e) => reject(e));
    await setDevotionalsDB.catch((e) => reject(e));
    await setGamesDB.catch((e) => reject(e));

    SetStoreDatabase();
    await createDatabaseIndexes().catch((e) => reject(e));

    resolve('Default is Set up');
});
