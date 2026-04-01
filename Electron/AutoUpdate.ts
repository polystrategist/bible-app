import { app, BrowserWindow, dialog, ipcMain } from 'electron';
import { autoUpdater, UpdateInfo } from 'electron-updater';
import Log from 'electron-log';

let errorAlreadyShown = false;
export default (mainWindow: BrowserWindow) => {
    if (app.isPackaged) {
        autoUpdater.autoDownload = false;
        autoUpdater.autoInstallOnAppQuit = true;

        if (process.platform === 'linux' && !process.env.APPIMAGE) {
            Log.warn('APPIMAGE env var not set — auto-update skipped (not running as AppImage, or AppImageLauncher did not pass the env var)');
            return;
        }

        autoUpdater.checkForUpdates();

        autoUpdater.on('update-available', () => {
            dialog
                .showMessageBox({
                    type: 'info',
                    buttons: ['Download Update', 'Cancel'],
                    title: 'Update Available',
                    message: 'A new update is available. Do you want to download and install it?',
                })
                .then((response) => {
                    if (response.response === 0) {
                        autoUpdater.downloadUpdate();
                    }
                });
        });

        autoUpdater.on('download-progress', (progressObj) => {
            const downloadPercentage = Math.floor(progressObj.percent);
            mainWindow.webContents.send('download-progress', downloadPercentage);
        });

        autoUpdater.addListener('update-downloaded', (_info: UpdateInfo) => {
            mainWindow.webContents.send('update-downloaded');
            dialog
                .showMessageBox({
                    type: 'info',
                    buttons: ['Install and Restart', 'Later'],
                    title: 'Update Ready',
                    message: 'The update has been downloaded. Do you want to install and restart the application?',
                })
                .then(({ response }) => {
                    if (response == 0 || response == 2) {
                        autoUpdater.quitAndInstall();
                    }
                });
        });

        ipcMain.handle('check-for-updates', async () => {
            try {
                const result = await autoUpdater.checkForUpdates();
                const latestVersion = result?.updateInfo?.version;
                const currentVersion = app.getVersion();
                const updateAvailable = !!latestVersion && latestVersion !== currentVersion;
                return { success: true, updateAvailable };
            } catch (err: any) {
                return { success: false, error: err?.message ?? 'Failed to check for updates' };
            }
        });
    } else {
        ipcMain.handle('check-for-updates', async () => {
            return { success: false, error: 'Updates are only available in packaged builds.' };
        });
    }

    autoUpdater.on('error', (error) => {
        if (!errorAlreadyShown) {
            errorAlreadyShown = true;
            Log.error('Update error:', error);
        }
    });
};
