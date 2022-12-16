import { ipcMain, BrowserWindow } from 'electron';
import { app } from 'electron';
import fs from 'fs';
import UPath, { resolve } from 'upath';
import Log from 'electron-log';
import { isNightly } from '../../config';
import { download } from 'electron-dl';

const isPackaged = app.isPackaged;

const dataPath = app.getPath('appData') + (!isNightly ? '\\believers-sword' : '\\believers-sword-nightly');
const filePath = dataPath + `\\modules\\bible\\`;

async function downloadModuleUrls(mainWindow: BrowserWindow, urls: Array<string>) {
    await Promise.all(
        urls.map(async (url) => {
            await download(mainWindow, url, {
                directory: filePath,
                onProgress: (data) => {
                    // console.log(data);
                    // mainWindow.webContents.send('download-module-inprogress', data);
                },
                overwrite: true,
                saveAs: false,
            });
        })
    );
}

export default (mainWindow: BrowserWindow) => {
    ipcMain.on('download', async (event, args) => {
        // console.log(args);
    });

    ipcMain.on('download-module', async (event, urls: Array<string>) => {
        try {
            await downloadModuleUrls(mainWindow, urls);
            mainWindow.webContents.send('download-module-done');
        } catch (e) {
            Log.warn('Download was interrupted.');
        }
    });
};
