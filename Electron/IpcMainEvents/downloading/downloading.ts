import { ipcMain, BrowserWindow } from 'electron';
import { app } from 'electron';
import fs from 'fs';
import UPath, { resolve } from 'upath';
import Log from 'electron-log';
import { isNightly } from '../../config';
import { download } from 'electron-dl';

const isPackaged = app.isPackaged;

const dataPath = app.getPath('userData');
const filePath = dataPath + `\\modules\\bible\\`;

async function downloadModuleUrls(mainWindow: BrowserWindow, urls: Array<string>) {
    await Promise.all(
        urls.map(async (url) => {
            await download(mainWindow, url, {
                directory: filePath,
                onProgress: (progressObj) => {
                    // Calculate the download progress percentage
                    const downloadPercentage = Math.floor(progressObj.percent);

                    // Update UI with progress percentage
                    mainWindow.webContents.send('download-module-progress', downloadPercentage);
                },
                onCompleted: (data) => {
                    mainWindow.webContents.send('download-module-done');
                },
                onCancel: () => {
                    mainWindow.webContents.send('download-module-cancel');
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
        await downloadModuleUrls(mainWindow, urls);
    });
};
