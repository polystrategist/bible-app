import { app } from 'electron';
import fs from 'fs';
import UPath from 'upath';
import Log from 'electron-log';
import { setupPortableMode } from '../../util/portable';

setupPortableMode();
const isPackaged = app.isPackaged;
const dataPath = app.getPath('userData');
const gamesDataPath = UPath.join(dataPath, 'Games');

function defaultsBase(): string {
    return isPackaged
        ? UPath.toUnix(
              UPath.join(__dirname, 'defaults', 'Main', 'games')
          ).replace('app.asar/dist/Setups/Setup/', '')
        : './defaults/Main/games';
}

function readVersion(versionPath: string): number {
    return JSON.parse(fs.readFileSync(versionPath, 'utf-8')).version as number;
}

function seedGameDb(type: 'qa' | 'tf' | 'fp', targetFilename: string): void {
    const base = defaultsBase();
    const defaultDbPath = UPath.join(base, type, 'game_seed.db');
    const defaultVersionPath = UPath.join(base, type, 'version.json');
    const targetDbPath = UPath.join(gamesDataPath, targetFilename);
    const installedVersionPath = UPath.join(gamesDataPath, `${type}_version.json`);

    const defaultVersion = readVersion(defaultVersionPath);
    fs.mkdirSync(gamesDataPath, { recursive: true });

    const copyDb = () => {
        fs.copyFileSync(defaultDbPath, targetDbPath);
        fs.writeFileSync(installedVersionPath, JSON.stringify({ version: defaultVersion }));
        Log.info(`[SetGamesDB] ${type} game DB seeded to version ${defaultVersion}`);
    };

    if (!fs.existsSync(targetDbPath)) {
        copyDb();
        return;
    }

    const installedVersion = fs.existsSync(installedVersionPath)
        ? readVersion(installedVersionPath)
        : 0;

    if (defaultVersion !== installedVersion) {
        copyDb();
    } else {
        Log.info(`[SetGamesDB] ${type} game DB up to date (v${defaultVersion})`);
    }
}

function seedFpImages(): void {
    const base = defaultsBase();
    const srcImages = UPath.join(base, 'fp', 'images');
    const destImages = UPath.join(gamesDataPath, 'fp_images');
    const defaultVersion = readVersion(UPath.join(base, 'fp', 'version.json'));
    const fpImagesVersionPath = UPath.join(gamesDataPath, 'fp_images_version.json');

    const installedVersion = fs.existsSync(fpImagesVersionPath)
        ? readVersion(fpImagesVersionPath)
        : 0;

    // Copy images on first run or whenever the FP DB version changes, so newly
    // added levels always have their images on disk.
    if (!fs.existsSync(destImages) || defaultVersion !== installedVersion) {
        fs.mkdirSync(destImages, { recursive: true });
        fs.cpSync(srcImages, destImages, { recursive: true });
        fs.writeFileSync(fpImagesVersionPath, JSON.stringify({ version: defaultVersion }));
        Log.info(`[SetGamesDB] FP images synced to version ${defaultVersion}`);
    } else {
        Log.info(`[SetGamesDB] FP images up to date (v${defaultVersion})`);
    }
}

export const setGamesDB = new Promise<void>((resolve, reject) => {
    try {
        seedGameDb('qa', 'qa_games.db');
        seedGameDb('tf', 'tf_games.db');
        seedGameDb('fp', 'fp_games.db');
        seedFpImages();
        resolve();
    } catch (err) {
        Log.error('[SetGamesDB] Setup failed:', err);
        reject(err);
    }
});
