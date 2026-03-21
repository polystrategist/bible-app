import { BrowserWindow } from 'electron';
import { appConfig } from '../ElectronStore/Configuration';

let resizeOrMoveTimeout: NodeJS.Timeout | null = null;

function onAfterResizeOrMove(win: BrowserWindow) {
    if (resizeOrMoveTimeout) clearTimeout(resizeOrMoveTimeout);

    // Reduced timeout from 1000ms to 500ms for better responsiveness
    resizeOrMoveTimeout = setTimeout(() => {
        const bounds = win.getBounds();
        appConfig.set('setting.appBounds', bounds);
    }, 500);
}

export function attachResizeListener(win: BrowserWindow) {
    win.on('resize', () => onAfterResizeOrMove(win));
    win.on('move', () => onAfterResizeOrMove(win));
    win.on('enter-full-screen', () => appConfig.set('setting.isFullScreen', true));
    // leave-full-screen is intentionally NOT saved here.
    // closeWindow() in BrowserWindowEvents reads win.isFullScreen() at the correct moment.
    // On Windows, win.destroy() fires a synthetic leave-full-screen event which would
    // overwrite the correctly-saved true value back to false.
}

