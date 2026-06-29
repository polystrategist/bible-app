import Log from 'electron-log';
import { BrowserWindow, screen, app } from 'electron';
import path from 'path';
import { isDev } from '../config';
import { appConfig } from '../ElectronStore/Configuration';
import { createWindowState } from '../util/window';
import { appIconPath } from '../util/appIcon';

/**
 * Borderless "loading" window shown immediately at launch while the main window loads
 * the app hidden in the background. The main process closes this and reveals the main
 * window only once the renderer signals it is fully rendered (see the `app-ready` IPC
 * in main.ts), so the user never sees the app assembling.
 *
 * Branded "book cover" splash (logo, scripture seal, Hebrews 4:12 verse, version),
 * themed from the user's saved palette: the cover gradient is tinted from the theme
 * accent and switches between a dark cover and a light "parchment" cover based on the
 * theme background. splash.html does that derivation from the bg/text/accent query
 * params; persisted via the `set-splash-theme` IPC. The window backgroundColor is set
 * to the theme bg so any pre-paint frame matches (no white flash), and the main process
 * matches the hidden main window's background to the same bg, so the swap into the app
 * stays clean in both light and dark themes.
 *
 * Opaque window (not transparent — transparent frameless windows render black on Windows).
 */

type SplashTheme = { bg?: string; text?: string; accent?: string };

// Defaults for a fresh install with no saved theme yet: a light cover with the app's
// default indigo accent.
const DEFAULTS: Required<SplashTheme> = { bg: '#ffffff', text: '#1f2233', accent: '#4f46e5' };

const SPLASH_WIDTH = 480;
const SPLASH_HEIGHT = 300;

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
// loading window is never a silent blank box — it still shows a themed cover with
// the name and a loading bar. Kept dependency-free (no external SVG) so it can never
// itself fail. Uses the theme bg/text + accent so it matches the real splash.
function fallbackSplashDataUrl(theme: Required<SplashTheme>, version: string): string {
    const ver = version ? `<div class="ver">v${version.replace(/^v/i, '')}</div>` : '';
    const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
        html,body{width:100%;height:100%;margin:0;overflow:hidden;color:${theme.text};
            font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;user-select:none}
        .cover{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
            justify-content:center;background:${theme.bg}}
        .name{font-size:24px;font-weight:800;letter-spacing:3px}
        .name b{color:${theme.accent}}
        .ver{margin-top:10px;font-size:12px;opacity:.6}
        .loader{position:absolute;left:0;right:0;bottom:0;height:3px;
            background:color-mix(in srgb, ${theme.text} 14%, transparent);overflow:hidden}
        .loader::before{content:"";position:absolute;top:0;left:0;height:100%;width:38%;
            background:linear-gradient(90deg,transparent,${theme.accent} 45%,${theme.accent} 55%,transparent);
            animation:slide 1.35s cubic-bezier(.45,.05,.35,1) infinite}
        @keyframes slide{0%{transform:translateX(-120%)}100%{transform:translateX(360%)}}
    </style></head><body><div class="cover"><div class="name">BELIEVERS&nbsp;<b>SWORD</b></div>
        ${ver}<div class="loader"></div></div></body></html>`;
    return `data:text/html;charset=utf-8,${encodeURIComponent(html)}`;
}

export function createSplashWindow(): BrowserWindow {
    const iconPath = appIconPath();

    const version = app.getVersion();
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
        splashWindow.loadURL(fallbackSplashDataUrl(theme, version));
    });

    const query = { version, bg: theme.bg, text: theme.text, accent: theme.accent };
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
