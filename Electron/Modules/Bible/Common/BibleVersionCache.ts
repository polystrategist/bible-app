import knex from 'knex';
import { app } from 'electron';
import { setupPortableMode } from '../../../util/portable';

setupPortableMode();
const dataPath = app.getPath('userData');
const bibleModulesPath = dataPath + `\\modules\\bible\\`;

// Cache for Bible version database connections
const bibleVersionCache: Map<string, any> = new Map();

/**
 * Get or create a cached knex instance for a Bible version
 * This prevents creating new database connections on every query
 */
export function getBibleVersionDb(version: string) {
    if (!bibleVersionCache.has(version)) {
        const db = knex({
            client: 'sqlite3',
            useNullAsDefault: false,
            connection: {
                filename: bibleModulesPath + version,
            },
        });
        bibleVersionCache.set(version, db);
    }
    return bibleVersionCache.get(version);
}

/**
 * Clear the Bible version cache (useful for cleanup or reload)
 */
export function clearBibleVersionCache() {
    bibleVersionCache.forEach((db) => db.destroy());
    bibleVersionCache.clear();
}
