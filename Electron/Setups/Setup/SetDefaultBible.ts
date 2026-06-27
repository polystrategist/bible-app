import { app } from 'electron';
import fs from 'fs';
import UPath from 'upath';
import Log from 'electron-log';
import { setupPortableMode } from '../../util/portable';

setupPortableMode();
const dataPath = app.getPath('userData');
const defaultBibleFiles = [`bs_KJV - 1769.SQLite3`, `bs_NASB - 1971.SQLite3`];
// Old default modules that have been replaced — removed from existing installs
// so they don't linger as orphaned, strongs-less duplicates.
const deprecatedBibleFiles = [`King James Version - 1769.SQLite3`];
const isPackaged = app.isPackaged;
const bibleDir = dataPath + `\\modules\\bible`;

// Bump whenever the *content* of a bundled bible changes (e.g. the KJV gained
// Strong's numbers). Existing installs only copy a default bible if it doesn't
// already exist, so without a version bump they keep their stale copy forever.
// Raising this forces a one-time overwrite of all default bibles on next launch.
// v2: KJV-1769 + bs_NASB reseeded with Strong's numbers and red-letter words.
const BUNDLED_BIBLE_VERSION = 2;
// Marker lives OUTSIDE the bible modules dir so it is never mistaken for a
// module by the directory scan (availableBibles).
const versionFilePath = `${dataPath}\\.bundled_bible_version`;
// Previous marker location, inside the modules dir — cleaned up on launch.
const legacyVersionFileName = `.bundled_version`;

const resolveDefaultSource = (fileName: string) =>
    isPackaged
        ? UPath.toUnix(UPath.join(__dirname, 'defaults', 'Modules', 'Bible', fileName)).replace(
              'app.asar/dist/Setups/Setup/',
              ''
          )
        : `./defaults/Modules/Bible/${fileName}`;

const readVersionFrom = (filePath: string): number => {
    try {
        const value = parseInt(fs.readFileSync(filePath, 'utf-8').trim(), 10);
        return Number.isNaN(value) ? 0 : value;
    } catch {
        return 0;
    }
};

const copyDefaultBible = (fileName: string, forceReseed: boolean) =>
    new Promise<void>((resolve, reject) => {
        const destPath = `${bibleDir}\\${fileName}`;
        if (fs.existsSync(destPath) && !forceReseed) {
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

        // Read the marker, falling back to the legacy location so installs that
        // already seeded the current version aren't needlessly reseeded.
        const seededVersion = Math.max(
            readVersionFrom(versionFilePath),
            readVersionFrom(`${bibleDir}\\${legacyVersionFileName}`)
        );
        const forceReseed = seededVersion < BUNDLED_BIBLE_VERSION;

        // Remove replaced modules and the legacy marker (the latter used to show
        // up in the version picker as a bogus ".bundled_version" module).
        for (const fileName of [...deprecatedBibleFiles, legacyVersionFileName]) {
            const removePath = `${bibleDir}\\${fileName}`;
            if (fs.existsSync(removePath)) {
                try {
                    fs.unlinkSync(removePath);
                } catch (e) {
                    Log.error(e);
                }
            }
        }

        Promise.all(defaultBibleFiles.map((fileName) => copyDefaultBible(fileName, forceReseed)))
            .then(() => {
                try {
                    fs.writeFileSync(versionFilePath, String(BUNDLED_BIBLE_VERSION));
                } catch (e) {
                    Log.error(e);
                }
                resolve('Setup Successful!');
            })
            .catch(reject);
    });
});
