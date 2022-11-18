import { isNightly } from '../../../config';
import { app, ipcMain } from 'electron';
import fs from 'fs';

const dataPath = app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = dataPath + `\\modules\\bible\\`;

export default () => {
    ipcMain.handle('availableBibles', () => fs.readdirSync(filePath));
};
