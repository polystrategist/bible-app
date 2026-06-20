import { BrowserWindow } from 'electron';
import path from 'path';
import { isDev, isBeta } from '../config';
import { appConfig } from '../ElectronStore/Configuration';

/**
 * Borderless "loading" window shown immediately at launch while the main window loads
 * the app hidden in the background. The main process closes this and reveals the main
 * window only once the renderer signals it is fully rendered (see the `app-ready` IPC
 * in main.ts), so the user never sees the app assembling.
 *
 * Opaque window (not transparent — transparent frameless windows render black on
 * Windows). Background follows the user's saved theme; defaults to white when nothing
 * is saved yet (e.g. first launch). The renderer persists these colors via the
 * `set-splash-theme` IPC.
 */

type SplashTheme = { bg?: string; text?: string; accent?: string };

const DEFAULTS: Required<SplashTheme> = { bg: '#ffffff', text: '#333333', accent: '#279EFF' };

let splashWindow: BrowserWindow | null = null;

function resolveTheme(): Required<SplashTheme> {
    const saved = (appConfig.get('setting.splashTheme') as SplashTheme | undefined) || {};
    const pick = (v: string | undefined, fallback: string) =>
        typeof v === 'string' && v.trim() ? v.trim() : fallback;
    return {
        bg: pick(saved.bg, DEFAULTS.bg),
        text: pick(saved.text, DEFAULTS.text),
        accent: pick(saved.accent, DEFAULTS.accent),
    };
}

export function createSplashWindow(): BrowserWindow {
    let iconPath = path.join(__dirname, 'assets', 'icon.ico');
    if (isDev || isBeta) iconPath = path.join('assets', 'icon.ico');

    const theme = resolveTheme();

    splashWindow = new BrowserWindow({
        width: 440,
        height: 320,
        center: true,
        frame: false,
        resizable: false,
        movable: false,
        alwaysOnTop: true,
        skipTaskbar: true,
        show: false,
        backgroundColor: theme.bg,
        icon: iconPath,
        webPreferences: {
            devTools: false,
        },
    });

    splashWindow.once('ready-to-show', () => {
        if (splashWindow && !splashWindow.isDestroyed()) splashWindow.show();
    });

    const query = { bg: theme.bg, text: theme.text, accent: theme.accent };
    if (isDev) {
        const qs = new URLSearchParams(query).toString();
        splashWindow.loadURL(`http://localhost:3000/splash.html?${qs}`);
    } else {
        splashWindow.loadFile(path.join(__dirname, 'splash.html'), { query });
    }

    splashWindow.on('closed', () => {
        splashWindow = null;
    });

    return splashWindow;
}

export function closeSplash(): void {
    if (splashWindow && !splashWindow.isDestroyed()) splashWindow.close();
    splashWindow = null;
}
