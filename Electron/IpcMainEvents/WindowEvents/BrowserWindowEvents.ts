import { appConfig } from "./../../ElectronStore/Configuration";
import { app, BrowserWindow, ipcMain, screen } from "electron";

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
    win.destroy();
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
    ipcMain.handle("minimizeWindow", () => minimizeWindow(win));
    ipcMain.handle("maximizeWindow", () => maximizeWindow(win));
    ipcMain.handle("closeWindow", () => closeWindow(win));
    ipcMain.handle("isWindowBrowserMaximized", () => {
        return win.isMaximized();
    });
    ipcMain.handle('getAppScale', () => getAppScale(win));
    ipcMain.handle('setAppScale', (_event, scale: number) => setAppScale(win, scale));
};
