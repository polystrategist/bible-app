import { app, BrowserWindow, ipcMain, shell } from 'electron';
import { autoUpdater, UpdateInfo } from 'electron-updater';
import Log from 'electron-log';
import { saveWindowState } from './util/window';

let errorAlreadyShown = false;

type UpdateProvider = 'electron-updater' | 'microsoft-store' | 'unavailable';

type UpdateConfig = {
    provider: UpdateProvider;
    canCheckForUpdates: boolean;
    message: string;
};

const registerHandler = <T extends Parameters<typeof ipcMain.handle>[1]>(channel: string, handler: T) => {
    ipcMain.removeHandler(channel);
    ipcMain.handle(channel, handler);
};

const getUpdateProvider = (): UpdateProvider => {
    if (!app.isPackaged) {
        return 'unavailable';
    }

    if (process.windowsStore) {
        return 'microsoft-store';
    }

    if (process.platform === 'linux' && !process.env.APPIMAGE) {
        return 'unavailable';
    }

    return 'electron-updater';
};

const getUpdateConfig = (): UpdateConfig => {
    const provider = getUpdateProvider();

    if (provider === 'microsoft-store') {
        return {
            provider,
            canCheckForUpdates: false,
            message: 'This installation is managed by Microsoft Store. Publish a new Store submission with a higher version, then users receive the update through Store.',
        };
    }

    if (provider === 'unavailable') {
        return {
            provider,
            canCheckForUpdates: false,
            message: 'Automatic update checks are only available in packaged desktop builds.',
        };
    }

    return {
        provider,
        canCheckForUpdates: true,
        message: 'Check for updates from the configured release feed.',
    };
};

export default (mainWindow: BrowserWindow) => {
    const updateConfig = getUpdateConfig();

    registerHandler('get-update-config', async () => updateConfig);
    registerHandler('open-store-updates', async () => {
        if (getUpdateProvider() !== 'microsoft-store') {
            return { success: false, error: 'Microsoft Store updates are only available for Store installations.' };
        }

        await shell.openExternal('ms-windows-store://downloadsandupdates');
        return { success: true };
    });

    if (updateConfig.provider === 'electron-updater') {
        autoUpdater.autoDownload = false;
        autoUpdater.autoInstallOnAppQuit = true;

        registerHandler('install-update', () => {
            saveWindowState();
            autoUpdater.quitAndInstall(process.platform === 'win32', true);
        });

        registerHandler('download-update', () => {
            autoUpdater.downloadUpdate();
        });

        registerHandler('check-for-updates', async () => {
            try {
                const result = await autoUpdater.checkForUpdates();
                const latestVersion = result?.updateInfo?.version;
                const currentVersion = app.getVersion();
                const updateAvailable = !!latestVersion && latestVersion !== currentVersion;
                return { success: true, updateAvailable, provider: updateConfig.provider };
            } catch (err: any) {
                return {
                    success: false,
                    error: err?.message ?? 'Failed to check for updates',
                    provider: updateConfig.provider,
                };
            }
        });

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
        registerHandler('check-for-updates', async () => {
            return {
                success: updateConfig.provider === 'microsoft-store',
                updateAvailable: false,
                error: updateConfig.provider === 'microsoft-store' ? undefined : updateConfig.message,
                provider: updateConfig.provider,
                message: updateConfig.message,
            };
        });
        registerHandler('install-update', async () => {});
        registerHandler('download-update', async () => {});
    }

    autoUpdater.on('error', (error) => {
        if (!errorAlreadyShown) {
            errorAlreadyShown = true;
            Log.error('Update error:', error);
        }
    });
};
