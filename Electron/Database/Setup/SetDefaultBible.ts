import { app } from 'electron';
import fs from 'fs';
import UPath from 'upath';

const isPackaged = app.isPackaged;
const isNightly = process.env.IS_NIGHTLY == 'yes';

const dataPath = app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = dataPath + `\\modules\\bible\\KJV1769+.SQLite3`;

export const setDefaultBible = new Promise((resolve, reject) => {
    if (!fs.existsSync(filePath)) {
        fs.mkdir(dataPath + '/modules/bible/', { recursive: true }, (err) => {
            if (err) reject(err);

            const defaultBiblePath = isPackaged
                ? UPath.toUnix(UPath.join(__dirname, 'defaults', 'Modules', 'Bible', 'KJV1769+.SQLite3')).replace('app.asar/', '')
                : './defaults/Modules/Bible/KJV1769+.SQLite3';

            fs.copyFile(defaultBiblePath, dataPath + `\\modules\\bible\\KJV1769+.SQLite3`, (err) => {
                if (err) reject(err);
            });

            resolve('Setup Successful!');
        });
    } else {
        resolve('Database file already exist');
    }
});
