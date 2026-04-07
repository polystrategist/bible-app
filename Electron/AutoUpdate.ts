import { app, BrowserWindow, ipcMain } from 'electron';
import { autoUpdater, UpdateInfo } from 'electron-updater';
import Log from 'electron-log';
import { saveWindowState } from './util/window';

let errorAlreadyShown = false;
export default (mainWindow: BrowserWindow) => {
    if (app.isPackaged) {
        autoUpdater.autoDownload = false;
        autoUpdater.autoInstallOnAppQuit = true;

        ipcMain.handle('install-update', () => {
            saveWindowState();
            autoUpdater.quitAndInstall(process.platform === 'win32', true);
        });

        ipcMain.handle('download-update', () => {
            autoUpdater.downloadUpdate();
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

        if (process.platform === 'linux' && !process.env.APPIMAGE) {
            Log.warn('APPIMAGE env var not set — auto-update skipped (not running as AppImage, or AppImageLauncher did not pass the env var)');
            return;
        }

        autoUpdater.checkForUpdates();

        autoUpdater.on('update-available', (info) => {
            mainWindow.webContents.send('update-available', info.version);
        });

        autoUpdater.on('download-progress', (progressObj) => {
            const downloadPercentage = Math.floor(progressObj.percent);
            mainWindow.webContents.send('download-progress', downloadPercentage);
        });

        autoUpdater.addListener('update-downloaded', (_info: UpdateInfo) => {
            mainWindow.webContents.send('update-downloaded');
        });
    } else {
        ipcMain.handle('check-for-updates', async () => {
            return { success: false, error: 'Updates are only available in packaged builds.' };
        });
        ipcMain.handle('install-update', async () => {});
        ipcMain.handle('download-update', async () => {});
    }

    autoUpdater.on('error', (error) => {
        if (!errorAlreadyShown) {
            errorAlreadyShown = true;
            Log.error('Update error:', error);
        }
    });
};
