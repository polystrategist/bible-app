import { app, ipcMain } from 'electron';
import fs from 'fs';

const dataPath = app.getPath('userData');
const filePath = dataPath + `\\modules\\bible\\`;

export default () => {
    ipcMain.handle('availableBibles', () => fs.readdirSync(filePath));
};
