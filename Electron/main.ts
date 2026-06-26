import Log from 'electron-log';
import { app, BrowserWindow, ipcMain, screen } from 'electron';
import path from 'path';
import { isDev, isBeta } from './config';
import { setupDefault } from './Setups/setup';
import { appConfig } from './ElectronStore/Configuration';
import IpcMainEvents from './IpcMainEvents/IpcMainEvents';
import BibleModules from './Modules/Bible/Bible';
import AppUpdater from './AutoUpdate';
import { setupPortableMode } from './util/portable';
import { createWindowState, attachWindowStateManager, saveWindowState } from './util/window';
import { clearBibleVersionCache } from './Modules/Bible/Common/BibleVersionCache';
import { registerGameImagesScheme, registerGameImagesProtocol } from './util/gameImagesProtocol';
import { createSplashWindow, closeSplash } from './Windows/SplashWindow';
import { startedHidden } from './util/autoLaunch';
import { createAppTray } from './util/appTray';
import { startReminderScheduler, recordActivity, getReminderEnabled, applyAutoLaunch } from './Reminders/ReminderScheduler';

// Custom scheme registration must happen before app `ready`.
registerGameImagesScheme();

// Suppress EPIPE errors when stdout/stderr pipe is closed (e.g. terminal closed after launch)
process.stdout.on('error', (err: NodeJS.ErrnoException) => { if (err.code === 'EPIPE') return; });
process.stderr.on('error', (err: NodeJS.ErrnoException) => { if (err.code === 'EPIPE') return; });

// Check if running in portable mode
setupPortableMode();

// When the loading splash was shown, so the main window can be held back until the
// splash has been visible for at least its minimum duration.
let splashShownAt = 0;
const MIN_SPLASH_MS = 3000;

// Tracks the live main window so the tray can re-show it, and whether the user
// chose a real Quit (vs. close-to-tray, which keeps the app alive for reminders).
let currentWindow: BrowserWindow | null = null;
let isQuiting = false;

async function createWindow() {
    const savedScale = Number(appConfig.get('setting.appScale', 1));
    const appScale = Number.isFinite(savedScale) ? Math.min(1.5, Math.max(0.75, savedScale)) : 1;

    let iconPath = path.join(__dirname, 'assets', 'icon.ico');

    if (isDev || isBeta) iconPath = path.join('assets', 'icon.ico');

    const windowState = createWindowState();

    // Match the hidden main window's background to the saved splash/theme background so
    // that, whenever it is finally shown, there is no white flash. Defaults to white.
    const savedSplashBg = appConfig.get('setting.splashTheme.bg') as string | undefined;
    const bgColor = savedSplashBg && savedSplashBg.trim() ? savedSplashBg.trim() : '#ffffff';
    let mainRevealed = false;

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
            devTools: true,
        },
        show: false,
        backgroundColor: bgColor,
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

    // Expose the live window to the tray / show helpers.
    currentWindow = mainWindow;
    mainWindow.on('closed', () => {
        if (currentWindow === mainWindow) currentWindow = null;
    });
    // Close-to-tray: keep the app alive so reminders can fire, unless the user
    // explicitly chose Quit (tray menu sets isQuiting) or reminders are off.
    mainWindow.on('close', (e) => {
        if (!isQuiting && getReminderEnabled()) {
            e.preventDefault();
            mainWindow.hide();
        }
    });

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

    // auto updater (always called so IPC handlers are registered; internal check skips auto-update on unpackaged dev builds)
    AppUpdater(mainWindow);

    // Reveal the main window only once the renderer signals it is fully rendered
    // (window.browserWindow.appReady()), and only after the splash has been visible for
    // at least MIN_SPLASH_MS. Until then the main window stays hidden behind the splash,
    // so the user never sees the app assembling.
    let fallbackTimer: ReturnType<typeof setTimeout> | undefined;
    const revealMainWindow = () => {
        if (mainRevealed || mainWindow.isDestroyed()) return;
        const minRemaining = Math.max(0, MIN_SPLASH_MS - (Date.now() - splashShownAt));
        setTimeout(() => {
            if (mainRevealed || mainWindow.isDestroyed()) return;
            mainRevealed = true;
            if (fallbackTimer) clearTimeout(fallbackTimer);

            mainWindow.show();
            if (windowState.isFullScreen) {
                mainWindow.setFullScreen(true);
            } else if (windowState.isMaximized) {
                mainWindow.maximize();
            }
            closeSplash();

            // this will turn off always on top after opening the application
            setTimeout(() => {
                if (mainWindow.isDestroyed()) return;
                mainWindow.setAlwaysOnTop(false);
                mainWindow.focus();
            }, 1000);
        }, minRemaining);
    };

    ipcMain.once('app-ready', revealMainWindow);
    // Safety net so the window is never stuck hidden if the ready signal never arrives.
    fallbackTimer = setTimeout(revealMainWindow, 20000);

    // and load the index.html of the app.
    await mainWindow.loadURL(isDev ? 'http://localhost:3000' : `file://${path.join(__dirname, './index.html')}`);
}

// Re-show the main window (recreating it if it was destroyed), e.g. from the tray.
async function showMainWindow() {
    if (!currentWindow || currentWindow.isDestroyed()) {
        await createWindow();
    }
    if (currentWindow) {
        if (currentWindow.isMinimized()) currentWindow.restore();
        currentWindow.show();
        currentWindow.focus();
    }
}

// Fully quit (bypasses close-to-tray).
function quitApp() {
    isQuiting = true;
    app.quit();
}

// Reveal the existing window when the app is launched a second time.
app.on('second-instance', () => {
    recordActivity();
    void showMainWindow();
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(async () => {
    // Quit a second instance before showing anything.
    if (!app.requestSingleInstanceLock()) {
        app.quit();
        return;
    }

    // When auto-started at login, stay in the tray without flashing the UI.
    const launchedHidden = startedHidden();

    // Show the loading splash immediately — before DB setup and before the main window
    // loads — so the whole startup is covered instead of a blank screen.
    if (!launchedHidden) {
        createSplashWindow();
        splashShownAt = Date.now();
    }

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
        closeSplash();
        app.quit();
        return;
    }

    // Serve 4 Pictures 1 Word images via gameimg:// (after images are seeded).
    registerGameImagesProtocol();

    await createWindow();
    if (launchedHidden) currentWindow?.hide();

    // Reminders: mirror the settings to the OS login-item, create the tray, and
    // start the inactivity scheduler so nudges fire even when the window is hidden.
    applyAutoLaunch();
    const trayIcon = (isDev || isBeta)
        ? path.join('assets', 'icon.ico')
        : path.join(__dirname, 'assets', 'icon.ico');
    createAppTray({ iconPath: trayIcon, onOpen: showMainWindow, onQuit: quitApp });
    startReminderScheduler();
    app.on('browser-window-focus', () => recordActivity());

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
    // Clean up Bible version cache to prevent memory leaks
    clearBibleVersionCache();
    // macOS keeps apps alive by convention.
    if (process.platform === 'darwin') return;
    // Stay alive in the tray while reminders are on (unless the user chose Quit),
    // so inactivity nudges can still fire after the window is closed.
    if (getReminderEnabled() && !isQuiting) return;
    app.quit();
});

// Clean up resources before quitting
app.on('before-quit', () => {
    saveWindowState();
    clearBibleVersionCache();
    Log.info('Application cleanup completed');
});
