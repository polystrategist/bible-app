import { app, ipcMain } from 'electron';
import fs from 'fs';
import path from 'path';
import { setupPortableMode } from '../../../util/portable';
import { getBibleVersionDb } from './BibleVersionCache';

setupPortableMode();
const dataPath = app.getPath('userData');
const biblePath = path.join(dataPath, 'modules', 'bible');

// Access the cache via getBibleVersionDb to destroy the connection before deleting
import { clearBibleVersionCache } from './BibleVersionCache';

export default () => {
    ipcMain.handle('deleteBible', async (_event, fileName: string) => {
        try {
            if (!fileName || fileName.includes('..') || fileName.includes('/') || fileName.includes('\\')) {
                return { success: false, error: 'Invalid file name.' };
            }

            const fullPath = path.join(biblePath, fileName);

            if (!fs.existsSync(fullPath)) {
                return { success: false, error: 'Bible module file not found.' };
            }

            // Destroy the cached DB connection for this module if it exists
            try {
                const db = getBibleVersionDb(fileName);
                if (db) {
                    await db.destroy();
                }
            } catch {
                // Ignore cache miss — file may not have been opened yet
            }

            // Re-initialize cache without the deleted entry
            clearBibleVersionCache();

            fs.unlinkSync(fullPath);

            return { success: true };
        } catch (err: any) {
            return { success: false, error: err.message || 'Failed to delete Bible module.' };
        }
    });
};
