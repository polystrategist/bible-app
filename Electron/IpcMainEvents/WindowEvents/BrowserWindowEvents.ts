import { appConfig } from "./../../ElectronStore/Configuration";
import { app, BrowserWindow, ipcMain, screen } from "electron";

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
    const appBounds = win.getBounds();
    appConfig.set('setting.appBounds', appBounds);
    win.destroy();
};

export const windowBrowserEvents = (win: BrowserWindow) => {
    ipcMain.handle("minimizeWindow", () => minimizeWindow(win));
    ipcMain.handle("maximizeWindow", () => maximizeWindow(win));
    ipcMain.handle("closeWindow", () => closeWindow(win));
    ipcMain.handle("isWindowBrowserMaximized", () => {
        return win.isMaximized();
    });
};
