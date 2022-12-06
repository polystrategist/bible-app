import { app } from 'electron';
import fs from 'fs';
import UPath from 'upath';
import Log from 'electron-log';
import { isNightly } from '../../config';

const isPackaged = app.isPackaged;

const dataPath = app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = dataPath + `\\modules\\bible\\KJ'1769.SQLite3`;

export const setDefaultBible = new Promise((resolve, reject) => {
    if (!fs.existsSync(filePath)) {
        fs.mkdir(dataPath + '/modules/bible/', { recursive: true }, (err) => {
            if (err) reject(err);

            const defaultBiblePath = isPackaged
                ? UPath.toUnix(UPath.join(__dirname, 'defaults', 'Modules', 'Bible', `KJ'1769.SQLite3`)).replace(
                      'app.asar/dist/Setups/Setup/',
                      ''
                  )
                : `./defaults/Modules/Bible/KJ'1769.SQLite3`;
            Log.info('Default Bible Path:', defaultBiblePath);

            fs.copyFile(defaultBiblePath, dataPath + `\\modules\\bible\\KJ'1769.SQLite3`, (err) => {
                Log.error(err);
                if (err) reject(err);
            });

            resolve('Setup Successful!');
        });
    } else {
        resolve('Database file already exist');
    }
});
