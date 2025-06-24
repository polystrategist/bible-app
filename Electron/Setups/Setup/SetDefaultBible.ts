import { app } from 'electron';
import fs from 'fs';
import UPath from 'upath';
import Log from 'electron-log';
import { setupPortableMode } from '../../util/portable';

setupPortableMode();
const dataPath = app.getPath('userData');
const defaultBibleFile = `King James Version - 1769.SQLite3`;
const isPackaged = app.isPackaged;
const filePath = dataPath + `\\modules\\bible\\${defaultBibleFile}`;

export const setDefaultBible = new Promise((resolve, reject) => {
    if (!fs.existsSync(filePath)) {
        fs.mkdir(dataPath + '/modules/bible/', { recursive: true }, (err) => {
            if (err) reject(err);

            const defaultBiblePath = isPackaged
                ? UPath.toUnix(UPath.join(__dirname, 'defaults', 'Modules', 'Bible', defaultBibleFile)).replace(
                    'app.asar/dist/Setups/Setup/',
                    ''
                )
                : `./defaults/Modules/Bible/${defaultBibleFile}`;
            Log.info('Default Bible Path:', defaultBiblePath);

            fs.copyFile(defaultBiblePath, dataPath + `\\modules\\bible\\King James Version - 1769.SQLite3`, (err) => {
                Log.error(err);
                if (err) reject(err);
            });

            resolve('Setup Successful!');
        });
    } else {
        resolve(`${defaultBibleFile} Database file already exist`);
    }
});
