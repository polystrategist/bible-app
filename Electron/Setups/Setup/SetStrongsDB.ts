import { app } from 'electron';
import fs from 'fs';
import UPath from 'upath';
import Log from 'electron-log';
import { setupPortableMode } from '../../util/portable';

setupPortableMode();
const isPackaged = app.isPackaged;
const dataPath = app.getPath('userData');
const dbFilePath = UPath.join(dataPath, 'StoreDB', 'strongs.db');
const installedVersionPath = UPath.join(dataPath, 'StoreDB', 'strongs.version.json');

export const setStrongsDB = new Promise<void>(async (resolve, reject) => {
    const defaultDbPath = isPackaged
        ? UPath.toUnix(UPath.join(__dirname, 'defaults', 'Main', 'strongs.db')).replace(
            'app.asar/dist/Setups/Setup/',
            ''
        )
        : './defaults/Main/strongs.db';

    const defaultVersionPath = isPackaged
        ? UPath.toUnix(UPath.join(__dirname, 'defaults', 'Main', 'strongs.version.json')).replace(
            'app.asar/dist/Setups/Setup/',
            ''
        )
        : './defaults/Main/strongs.version.json';

    let defaultVersion: number;
    try {
        defaultVersion = JSON.parse(fs.readFileSync(defaultVersionPath, 'utf-8')).version;
    } catch (err) {
        Log.error('Failed to read strongs.version.json:', err);
        return reject(err);
    }

    const copyDB = () => {
        try {
            fs.mkdirSync(UPath.join(dataPath, 'StoreDB'), { recursive: true });
            fs.copyFileSync(defaultDbPath, dbFilePath);
            fs.writeFileSync(installedVersionPath, JSON.stringify({ version: defaultVersion }));
        } catch (err) {
            Log.error('Failed to copy strongs.db:', err);
            return reject(err);
        }
    };

    if (!fs.existsSync(dbFilePath)) {
        copyDB();
        Log.info('Copied strongs.db version', defaultVersion);
        resolve();
    } else {
        const installedVersion = fs.existsSync(installedVersionPath)
            ? JSON.parse(fs.readFileSync(installedVersionPath, 'utf-8')).version
            : 0;

        if (defaultVersion !== installedVersion) {
            copyDB();
            Log.info('Updated strongs.db to version', defaultVersion);
        } else {
            Log.info('strongs.db is up to date (version', defaultVersion + ')');
        }
        resolve();
    }
});
