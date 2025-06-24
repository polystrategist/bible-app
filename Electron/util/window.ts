import { BrowserWindow } from 'electron';
import { appConfig } from '../ElectronStore/Configuration';

let resizeOrMoveTimeout: NodeJS.Timeout | null = null;

function onAfterResizeOrMove(win: BrowserWindow) {
    if (resizeOrMoveTimeout) clearTimeout(resizeOrMoveTimeout);

    resizeOrMoveTimeout = setTimeout(() => {
        const bounds = win.getBounds();
        appConfig.set('setting.appBounds', bounds);
    }, 1000);
}

export function attachResizeListener(win: BrowserWindow) {
    win.on('resize', () => onAfterResizeOrMove(win));
    win.on('move', () => onAfterResizeOrMove(win));
}

