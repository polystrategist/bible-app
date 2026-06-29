import { ipcMain, BrowserWindow } from 'electron';
import { appIconPath } from '../util/appIcon';

export const WindowOpenerIpcEvents = (win: BrowserWindow) => {
    ipcMain.handle('open-donate-window', (event, payload) => {
        const { BrowserWindow, screen } = require('electron');

        // Get the primary screen's dimensions
        const primaryDisplay = screen.getPrimaryDisplay();
        const { height } = primaryDisplay.workAreaSize; // Gets usable height (excluding taskbars/docks)

        // Calculate 70% of the height
        const windowHeight = Math.round(height * 0.7);
        const iconPath = appIconPath();

        const win = new BrowserWindow({
            width: 700,
            height: windowHeight,
            autoHideMenuBar: true, // Hides the menu bar
            resizable: false,
            icon: iconPath, // Path to your icon
            webPreferences: {
                nodeIntegration: false, // If you need Node.js integration
            },
        });

        win.loadURL('https://buymeacoffee.com/jenuel.dev');
    });
};
