import { Tray, Menu, nativeImage } from 'electron';
import Log from 'electron-log';

let tray: Tray | null = null;

export function createAppTray(opts: {
    iconPath: string;
    onOpen: () => void;
    onQuit: () => void;
}): void {
    if (tray) return;
    // Build the icon through nativeImage so a bad path is detectable: a missing
    // file yields an empty image and an invisible tray instead of a hard crash.
    const image = nativeImage.createFromPath(opts.iconPath);
    if (image.isEmpty()) {
        Log.error(`[tray] icon failed to load from "${opts.iconPath}" — tray will be invisible.`);
    }
    tray = new Tray(image.isEmpty() ? opts.iconPath : image);
    tray.setToolTip('Believers Sword');
    tray.setContextMenu(
        Menu.buildFromTemplate([
            { label: 'Open Believers Sword', click: opts.onOpen },
            { type: 'separator' },
            { label: 'Quit', click: opts.onQuit },
        ]),
    );
    tray.on('click', opts.onOpen);
    tray.on('double-click', opts.onOpen);
}

export function destroyAppTray(): void {
    tray?.destroy();
    tray = null;
}
