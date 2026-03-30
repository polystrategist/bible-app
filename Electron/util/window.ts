import { BrowserWindow } from 'electron';
import windowStateKeeper from 'electron-window-state';

export function createWindowState() {
    return windowStateKeeper({
        defaultWidth: 1200,
        defaultHeight: 750,
    });
}

export function attachWindowStateManager(win: BrowserWindow, windowState: ReturnType<typeof windowStateKeeper>) {
    // Automatically tracks resize, move, and close events and persists state
    windowState.manage(win);
}

