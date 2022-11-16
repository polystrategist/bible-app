import { isNightly } from '../../config';
import { app, ipcMain } from 'electron';
import fs from 'fs';

export type GetVerseArgs = {
    bible_versions: Array<string>;
    book_number: number;
    book_chapter: number;
};

const dataPath = app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = dataPath + `\\modules\\bible\\`;

export default () => {
    ipcMain.handle('availableBibles', () => fs.readdirSync(filePath));
    ipcMain.handle('getVerses', (args) => {
        console.log(args);
        return args;
    });
};
