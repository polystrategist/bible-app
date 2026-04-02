import Log from 'electron-log';
import { app, BrowserWindow, screen } from 'electron';
import path from 'path';
import { isDev, isNightly } from './config';
import { setupDefault } from './Setups/setup';
import { appConfig } from './ElectronStore/Configuration';
import IpcMainEvents from './IpcMainEvents/IpcMainEvents';
import BibleModules from './Modules/Bible/Bible';
import AppUpdater from './AutoUpdate';
import { setupPortableMode } from './util/portable';
import { createWindowState, attachWindowStateManager } from './util/window';
import { clearBibleVersionCache } from './Modules/Bible/Common/BibleVersionCache';

// Check if running in portable mode
setupPortableMode();

async function createWindow() {
    const savedScale = Number(appConfig.get('setting.appScale', 1));
    const appScale = Number.isFinite(savedScale) ? Math.min(1.5, Math.max(0.75, savedScale)) : 1;

    let iconPath = path.join(__dirname, 'assets', 'icon.ico');

    if (isDev || isNightly) iconPath = path.join('assets', 'icon.ico');

    const windowState = createWindowState();

    const mainWindow = new BrowserWindow({
        x: windowState.x,
        y: windowState.y,
        width: windowState.width,
        height: windowState.height,
        minWidth: 1226,
        minHeight: 700,
        icon: iconPath,
        webPreferences: {
            preload: __dirname + '/preload.js',
            devTools: isDev || isNightly,
        },
        show: false,
        alwaysOnTop: true,
        frame: false,
    });

    // Allow local font access so the renderer can call queryLocalFonts()
    mainWindow.webContents.session.setPermissionRequestHandler((_wc, permission, callback) => {
        callback((permission as string) === 'local-fonts');
    });

    mainWindow.webContents.setZoomFactor(appScale);

    // Tracks resize, move, close and persists window state automatically
    attachWindowStateManager(mainWindow, windowState);

    // Ensure a single instance of the app
    const gotTheLock = app.requestSingleInstanceLock();

    if (!gotTheLock) {
        // Quit if another instance is already running
        app.quit();
    }

    // run ipcMain events before loading the window
    IpcMainEvents(mainWindow);

    // Modules
    BibleModules();

    // auto updater (always called so IPC handlers are registered; internal check skips auto-update in dev/nightly)
    AppUpdater(mainWindow);

    // and load the index.html of the app.
    await mainWindow.loadURL(isDev ? 'http://localhost:3000' : `file://${path.join(__dirname, './index.html')}`);

    mainWindow.show();

    if (windowState.isFullScreen) {
        mainWindow.setFullScreen(true);
    } else if (windowState.isMaximized) {
        mainWindow.maximize();
    }

    // this will turn off always on top after opening the application
    setTimeout(() => {
        mainWindow.setAlwaysOnTop(false);
        mainWindow.focus();
    }, 1000);
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(async () => {
    if (isDev) {
        try {
            const { default: installExtension } = await import('electron-devtools-installer');
            await installExtension('nhdogjmejiglipccpnnnanhbledajbpd');
            Log.info('Vue DevTools installed');
        } catch (e) {
            Log.warn('Vue DevTools failed to install:', e);
        }
    }

    // check and set up the database
    try {
        await setupDefault;
        Log.info('Database setup completed successfully');
    } catch (e) {
        Log.error('Database setup failed:', e);
        app.quit();
        return;
    }

    await createWindow();
    app.on('activate', function () {
        // On macOS, it's common to re-create a window in the app when the
        // dock icon is clicked and there are no other windows open.
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        // Clean up Bible version cache to prevent memory leaks
        clearBibleVersionCache();
        app.quit();
    }
});

// Clean up resources before quitting
app.on('before-quit', () => {
    clearBibleVersionCache();
    Log.info('Application cleanup completed');
});
