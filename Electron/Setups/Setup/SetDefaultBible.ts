import { app } from 'electron';
import fs from 'fs';
import UPath from 'upath';
import Log from 'electron-log';
import { setupPortableMode } from '../../util/portable';

setupPortableMode();
const dataPath = app.getPath('userData');
const defaultBibleFiles = [`King James Version - 1769.SQLite3`, `bs_NASB - 1971.SQLite3`];
const isPackaged = app.isPackaged;
const bibleDir = dataPath + `\\modules\\bible`;

const resolveDefaultSource = (fileName: string) =>
    isPackaged
        ? UPath.toUnix(UPath.join(__dirname, 'defaults', 'Modules', 'Bible', fileName)).replace(
              'app.asar/dist/Setups/Setup/',
              ''
          )
        : `./defaults/Modules/Bible/${fileName}`;

const copyDefaultBible = (fileName: string) =>
    new Promise<void>((resolve, reject) => {
        const destPath = `${bibleDir}\\${fileName}`;
        if (fs.existsSync(destPath)) {
            resolve();
            return;
        }

        const sourcePath = resolveDefaultSource(fileName);
        Log.info('Default Bible Path:', sourcePath);

        fs.copyFile(sourcePath, destPath, (err) => {
            if (err) {
                Log.error(err);
                reject(err);
                return;
            }
            resolve();
        });
    });

export const setDefaultBible = new Promise((resolve, reject) => {
    fs.mkdir(bibleDir, { recursive: true }, (err) => {
        if (err) {
            reject(err);
            return;
        }

        Promise.all(defaultBibleFiles.map(copyDefaultBible))
            .then(() => resolve('Setup Successful!'))
            .catch(reject);
    });
});
