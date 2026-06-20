import { app, BrowserWindow } from 'electron';
import windowStateKeeper from 'electron-window-state';
import * as path from 'path';
import * as fs from 'fs';

let currentWindow: BrowserWindow | null = null;

export function createWindowState() {
    return windowStateKeeper({
        defaultWidth: 1200,
        defaultHeight: 750,
        // Do NOT auto-restore maximize/fullscreen here: manage() would call
        // win.maximize(), which forces a `show: false` window visible — popping the
        // main window open next to the splash. We restore these ourselves when the
        // window is actually revealed (see revealMainWindow in main.ts).
        maximize: false,
        fullScreen: false,
    });
}

export function attachWindowStateManager(win: BrowserWindow, windowState: ReturnType<typeof windowStateKeeper>) {
    currentWindow = win;
    windowState.manage(win);
}

/**
 * Manually save window bounds to the state file.
 * Call before force-quit scenarios (e.g., auto-update quitAndInstall).
 */
export function saveWindowState() {
    if (!currentWindow || currentWindow.isDestroyed()) return;
    try {
        const bounds = currentWindow.getBounds();
        const statePath = path.join(app.getPath('userData'), 'window-state.json');
        const state = {
            x: bounds.x,
            y: bounds.y,
            width: bounds.width,
            height: bounds.height,
            isMaximized: currentWindow.isMaximized(),
            isFullScreen: currentWindow.isFullScreen(),
        };
        fs.writeFileSync(statePath, JSON.stringify(state));
    } catch { /* ignore */ }
}

