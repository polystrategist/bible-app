import { setDefaultBible } from './Setup/SetDefaultBible';

export const setupDefault = new Promise(async (resolve, reject): Promise<void> => {
    await setDefaultBible.catch((e) => reject(e));

    resolve('Default is Set up');
});
