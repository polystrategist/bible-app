import { ipcMain, BrowserWindow } from 'electron';
import { app } from 'electron';
import { download } from 'electron-dl';
import { setupPortableMode } from '../../util/portable';

const isPackaged = app.isPackaged;

setupPortableMode();
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
