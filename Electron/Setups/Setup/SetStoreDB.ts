import { app } from 'electron';
import fs from 'fs';
import UPath from 'upath';
import Log from 'electron-log';
import { isNightly } from '../../config';

const isPackaged = app.isPackaged;

const dataPath = app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = UPath.join(dataPath, `StoreDB`, `Store.db`);

export const setStoreDB = new Promise((resolve, reject) => {
    if (!fs.existsSync(filePath)) {
        fs.mkdir(UPath.join(dataPath, 'StoreDB'), { recursive: true }, (err) => {
            if (err) {
                reject(err);
            }

            const defaultBiblePath = isPackaged
                ? UPath.toUnix(UPath.join(__dirname, 'defaults', 'Main', `Store.db`)).replace('app.asar/dist/Setups/Setup/', '')
                : `./defaults/Main/Store.db`;

            Log.info('Default Bible Path:', defaultBiblePath);

            fs.copyFile(defaultBiblePath, filePath, (err) => {
                if (err) {
                    Log.error(err);
                    reject(err);
                }
            });

            resolve('Setup StoreDB Successful!');
        });
    } else {
        resolve(` ${filePath} Database file already exist`);
    }
});
