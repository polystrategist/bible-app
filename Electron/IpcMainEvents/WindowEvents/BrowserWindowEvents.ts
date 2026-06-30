import { appConfig } from "./../../ElectronStore/Configuration";
import { app, BrowserWindow, clipboard, ipcMain, screen, shell } from "electron";
import { getCloseToTray, setCloseToTray } from "../../util/closeToTray";
import { applyAutoLaunch } from "../../Reminders/ReminderScheduler";

const MIN_SCALE = 0.75;
const MAX_SCALE = 1.5;

function normalizeScale(scale: number) {
    if (!Number.isFinite(scale)) return 1;
    return Math.min(MAX_SCALE, Math.max(MIN_SCALE, scale));
}

const minimizeWindow = (win: any) => {
    win.minimize();
};

const maximizeWindow = (win: BrowserWindow): boolean | void => {
    try {
        if (win.isMaximized()) {
            const { width, height } = screen.getPrimaryDisplay().workAreaSize;
            const appBounds: any = appConfig.get("setting.appBounds");

            if (appBounds !== undefined && appBounds !== null && appBounds.width > width && appBounds.height > height) {
                win.unmaximize();
                win.setSize(1180, 650, false);
                win.center();
            } else win.restore();
        } else win.maximize();
        return win.isMaximized();
    } catch (e) {
        console.log(e);
    }
};

const closeWindow = (win: BrowserWindow): void => {
    // Signal renderer to run a final sync before closing.
    // Give it up to 5 seconds; close regardless after timeout.
    win.webContents.send('app:sync-before-quit');
    const timer = setTimeout(() => win.close(), 5000);
    ipcMain.once('app:sync-before-quit-done', () => {
        clearTimeout(timer);
        win.close();
    });
};

const getAppScale = (win: BrowserWindow): number => {
    const savedScale = Number(appConfig.get('setting.appScale', 1));
    const normalizedScale = normalizeScale(savedScale);

    if (savedScale !== normalizedScale) {
        appConfig.set('setting.appScale', normalizedScale);
    }

    if (win.webContents.getZoomFactor() !== normalizedScale) {
        win.webContents.setZoomFactor(normalizedScale);
    }

    return normalizedScale;
};

const setAppScale = (win: BrowserWindow, scale: number): number => {
    const normalizedScale = normalizeScale(scale);
    appConfig.set('setting.appScale', normalizedScale);
    win.webContents.setZoomFactor(normalizedScale);
    return normalizedScale;
};

export const windowBrowserEvents = (win: BrowserWindow) => {
    win.on('maximize', () => win.webContents.send('window:maximized', true));
    win.on('unmaximize', () => win.webContents.send('window:maximized', false));

    ipcMain.handle("minimizeWindow", () => minimizeWindow(win));
    ipcMain.handle("maximizeWindow", () => maximizeWindow(win));
    ipcMain.handle("closeWindow", () => closeWindow(win));
    ipcMain.handle("isWindowBrowserMaximized", () => {
        return win.isMaximized();
    });
    ipcMain.handle('getAppScale', () => getAppScale(win));
    ipcMain.handle('setAppScale', (_event, scale: number) => setAppScale(win, scale));
    // Persist current theme colors so the next launch's loading splash matches them.
    ipcMain.handle('set-splash-theme', (_event, payload) => {
        appConfig.set('setting.splashTheme', payload);
    });
    // Close-to-tray preference: when on, the window's X hides to the tray
    // instead of quitting the app.
    ipcMain.handle('window:get-close-to-tray', () => getCloseToTray());
    ipcMain.handle('window:set-close-to-tray', (_event, value: boolean) => {
        setCloseToTray(value);
        // The login item rides on close-to-tray, so re-apply it when this changes.
        applyAutoLaunch();
        return getCloseToTray();
    });
    ipcMain.handle('openExternal', (_event, url: string) => shell.openExternal(url));
    // Native clipboard write. navigator.clipboard is unreliable in the renderer
    // (needs a secure context/focus and silently rejects), so verse copy routes
    // through Electron's clipboard module instead.
    ipcMain.handle('writeClipboard', (_event, text: string) => clipboard.writeText(text ?? ''));
};
