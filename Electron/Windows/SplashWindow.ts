import Log from 'electron-log';
import { BrowserWindow, screen } from 'electron';
import path from 'path';
import { isDev, isBeta } from '../config';
import { appConfig } from '../ElectronStore/Configuration';
import { createWindowState } from '../util/window';

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

const DEFAULTS: Required<SplashTheme> = { bg: '#f5f5f5', text: '#333333', accent: '#4A3AFF' };

const SPLASH_WIDTH = 440;
const SPLASH_HEIGHT = 320;

let splashWindow: BrowserWindow | null = null;

// Center the splash on the same display the main window will open on (read from the
// saved window state) so, on multi-monitor setups, it doesn't appear on the wrong screen.
// Returns null (→ center on primary) when there is no saved position yet.
function splashPosition(): { x: number; y: number } | null {
    try {
        const ws = createWindowState();
        if (typeof ws.x === 'number' && typeof ws.y === 'number') {
            const display = screen.getDisplayMatching({
                x: ws.x,
                y: ws.y,
                width: ws.width || 1200,
                height: ws.height || 750,
            });
            const area = display.workArea;
            return {
                x: Math.round(area.x + (area.width - SPLASH_WIDTH) / 2),
                y: Math.round(area.y + (area.height - SPLASH_HEIGHT) / 2),
            };
        }
    } catch {
        /* fall back to centering on the primary display */
    }
    return null;
}

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

// Minimal self-contained splash used only when splash.html cannot be loaded
// (e.g. a packaged build whose frontend dist predates the file). Guarantees the
// loading window is never a silent blank box — it still shows the themed name
// and spinner. Kept dependency-free (no external SVG) so it can never itself fail.
function fallbackSplashDataUrl(theme: Required<SplashTheme>): string {
    const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
        html,body{width:100%;height:100%;margin:0;background:${theme.bg};overflow:hidden;
            font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;user-select:none}
        .wrap{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center}
        .name{font-size:26px;font-weight:800;letter-spacing:.5px;color:${theme.text}}
        .spinner{margin-top:28px;width:30px;height:30px;border-radius:50%;
            border:3px solid color-mix(in srgb, ${theme.text} 18%, transparent);
            border-top-color:${theme.accent};animation:spin .8s linear infinite}
        @keyframes spin{to{transform:rotate(360deg)}}
    </style></head><body><div class="wrap"><div class="name">Believers Sword</div>
        <div class="spinner"></div></div></body></html>`;
    return `data:text/html;charset=utf-8,${encodeURIComponent(html)}`;
}

export function createSplashWindow(): BrowserWindow {
    let iconPath = path.join(__dirname, 'assets', 'icon.ico');
    if (isDev || isBeta) iconPath = path.join('assets', 'icon.ico');

    const theme = resolveTheme();
    const pos = splashPosition();

    splashWindow = new BrowserWindow({
        width: SPLASH_WIDTH,
        height: SPLASH_HEIGHT,
        ...(pos ? { x: pos.x, y: pos.y } : { center: true }),
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

    // If splash.html can't be loaded (missing from a stale dist, dev server not
    // up yet, etc.) the window would otherwise paint only its backgroundColor and
    // look blank. Log the failure and swap in a self-contained fallback so the
    // loading screen always shows the themed name + spinner. Guard against the
    // fallback's own (data: URL) load to avoid a loop.
    let usedFallback = false;
    splashWindow.webContents.on('did-fail-load', (_e, errorCode, errorDescription, validatedURL) => {
        Log.warn(`[splash] failed to load (${errorCode} ${errorDescription}): ${validatedURL}`);
        if (usedFallback || !splashWindow || splashWindow.isDestroyed()) return;
        usedFallback = true;
        splashWindow.loadURL(fallbackSplashDataUrl(theme));
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
