import { ipcMain, app } from 'electron';
import fs from 'fs';
import path from 'path';
import { setupPortableMode } from '../../../util/portable';

setupPortableMode();
const commentariesPath = path.join(app.getPath('userData'), 'modules', 'commentaries');

export default () => {
    ipcMain.handle('availableCommentaries', () => {
        if (!fs.existsSync(commentariesPath)) return [];
        return fs.readdirSync(commentariesPath);
    });
};
