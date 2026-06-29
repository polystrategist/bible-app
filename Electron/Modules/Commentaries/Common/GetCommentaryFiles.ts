import { ipcMain, app } from 'electron';
import fs from 'fs';
import path from 'path';
import Log from 'electron-log';
import { setupPortableMode } from '../../../util/portable';
import { getCommentaryDbByFile, listCommentaryFiles } from './CommentaryVersionCache';

setupPortableMode();
const commentariesPath = path.join(app.getPath('userData'), 'modules', 'commentaries');

/** Human title for a commentary: its `info.description`, else the file base. */
async function commentaryTitle(file: string): Promise<string> {
    const fallback = file.replace(/\.commentaries\.SQLite3$/i, '').replace(/\.SQLite3$/i, '');
    try {
        const db = getCommentaryDbByFile(file);
        if (!db) return fallback;
        const row = await db('info').where('name', 'description').first();
        const value = (row?.value ?? '').toString().trim();
        return value || fallback;
    } catch (err) {
        Log.error('commentaryTitle failed for', file, err);
        return fallback;
    }
}

export default () => {
    // Raw file-name list (legacy — kept for callers that only need names).
    ipcMain.handle('availableCommentaries', () => {
        if (!fs.existsSync(commentariesPath)) return [];
        return fs.readdirSync(commentariesPath);
    });

    // Installed commentary modules with a friendly title, for the tab's selector.
    ipcMain.handle('getCommentaryModules', async () => {
        const files = listCommentaryFiles();
        const modules = await Promise.all(
            files.map(async (file) => ({ file, title: await commentaryTitle(file) })),
        );
        return modules.sort((a, b) => a.title.localeCompare(b.title));
    });
};
