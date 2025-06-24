import { app } from 'electron';
import fs from 'fs';
import UPath from 'upath';
import Log from 'electron-log';
import { isNightly } from '../../config';
import { setDB } from '../../DataBase/DataBase';
import { setupPortableMode } from '../../util/portable';

setupPortableMode();
const isPackaged = app.isPackaged;
const dataPath = app.getPath('userData');
const filePath = UPath.join(dataPath, `StoreDB`, `Dictionary.db`);

export const setDictionaryDB = new Promise(async (resolve, reject) => {
    const defaultBiblePath = isPackaged
        ? UPath.toUnix(UPath.join(__dirname, 'defaults', 'Main', `Dictionary.db`)).replace(
            'app.asar/dist/Setups/Setup/',
            ''
        )
        : `./defaults/Main/Dictionary.db`;

    if (!fs.existsSync(filePath)) {
        fs.mkdir(UPath.join(dataPath, 'StoreDB'), { recursive: true }, (err) => {
            if (err) {
                reject(err);
            }

            Log.info('Default Bible Path:', defaultBiblePath);

            fs.copyFile(defaultBiblePath, filePath, (err) => {
                if (err) {
                    Log.error(err);
                    reject(err);
                }
            });

            resolve('Copied dictionary!');
        });
    } else {
        // TODO: check if version is not the same
        const toBeCopiedDictionary = setDB(defaultBiblePath);
        const currentDictionary = setDB(filePath);

        const toBeCopiedVersion = await toBeCopiedDictionary
            .from('version')
            .select('dictionary_version')
            .first()
            .then((res) => res.dictionary_version);
        const currentVersion = await currentDictionary
            .from('version')
            .select('dictionary_version')
            .first()
            .then((res) => res.dictionary_version);

        // TODO: if version is not the same replace with the new version
        if (toBeCopiedVersion !== currentVersion) {
            fs.copyFile(defaultBiblePath, filePath, (err) => {
                if (err) {
                    Log.error(err);
                    reject(err);
                }
            });
            console.log('copied new version');
            resolve('copied new version');
        } else {
            console.log('not copied because version is the same');
            resolve('not copied because version is the same');
        }
    }
});
