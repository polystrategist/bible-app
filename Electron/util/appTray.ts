import { Tray, Menu } from 'electron';

let tray: Tray | null = null;

export function createAppTray(opts: {
    iconPath: string;
    onOpen: () => void;
    onQuit: () => void;
}): void {
    if (tray) return;
    tray = new Tray(opts.iconPath);
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
