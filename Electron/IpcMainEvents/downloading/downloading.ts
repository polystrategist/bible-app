import { ipcMain, BrowserWindow } from 'electron';
import { app } from 'electron';
import fs from 'fs';
import UPath from 'upath';
import Log from 'electron-log';
import { isNightly } from '../../config';
import { download } from 'electron-dl';

const isPackaged = app.isPackaged;

const dataPath = app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = dataPath + `\\modules\\bible\\`;

export default (mainWindow: BrowserWindow) => {
    ipcMain.on('download', async (event, args) => {
        console.log(args);
    });

    ipcMain.on('download-module', async (event, url) => {
        try {
            await download(mainWindow, url, {
                directory: filePath,
                onProgress: (data) => {
                    mainWindow.webContents.send('download-module-inprogress', data);
                },
                overwrite: true,
            });
        } catch (e) {
            Log.warn('Download was interrupted.');
        }

        mainWindow.webContents.send('download-module-done');
    });
};
