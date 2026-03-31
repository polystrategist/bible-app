import knex from 'knex';
import { app } from 'electron';
import fs from 'fs';
import path from 'path';
import { setupPortableMode } from '../../../util/portable';

setupPortableMode();
const dataPath = app.getPath('userData');
const commentariesPath = path.join(dataPath, 'modules', 'commentaries');

const commentaryCache: Map<string, any> = new Map();

function findCommentaryFile(bibleVersion: string): string | null {
    if (!fs.existsSync(commentariesPath)) return null;

    const base = bibleVersion.replace(/\.SQLite3$/i, '');
    const candidates = [
        `${base}.commentaries.SQLite3`,
        `${base} Commentaries.SQLite3`,
        `${base} commentaries.SQLite3`,
    ];

    for (const name of candidates) {
        if (fs.existsSync(path.join(commentariesPath, name))) return name;
    }
    return null;
}

export function getCommentaryDb(bibleVersion: string): any | null {
    if (commentaryCache.has(bibleVersion)) {
        return commentaryCache.get(bibleVersion);
    }

    const fileName = findCommentaryFile(bibleVersion);
    if (!fileName) return null;

    const db = knex({
        client: 'sqlite3',
        useNullAsDefault: false,
        connection: { filename: path.join(commentariesPath, fileName) },
    });

    commentaryCache.set(bibleVersion, db);
    return db;
}

export function hasCommentaryFile(bibleVersion: string): boolean {
    return findCommentaryFile(bibleVersion) !== null;
}

export function clearCommentaryCache() {
    commentaryCache.forEach((db) => db.destroy());
    commentaryCache.clear();
}
