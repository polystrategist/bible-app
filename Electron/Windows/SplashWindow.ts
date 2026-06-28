import Log from 'electron-log';
import { BrowserWindow, screen, app } from 'electron';
import path from 'path';
import { isDev, isBeta } from '../config';
import { createWindowState } from '../util/window';

/**
 * Borderless "loading" window shown immediately at launch while the main window loads
 * the app hidden in the background. The main process closes this and reveals the main
 * window only once the renderer signals it is fully rendered (see the `app-ready` IPC
 * in main.ts), so the user never sees the app assembling.
 *
 * Branded "book cover" splash: a fixed deep-indigo cover (logo, scripture seal,
 * Hebrews 4:12 verse, version) shown regardless of the app's light/dark theme so it
 * always reads as a premium cover. The main process still matches the hidden main
 * window's background to the user's saved theme, so the swap into the app stays clean.
 *
 * Opaque window (not transparent — transparent frameless windows render black on
 * Windows); its backgroundColor is the cover's base color so any pre-paint frame is
 * on-brand rather than a white flash.
 */

// Base color of the cover gradient's darkest corner — used as the window backgroundColor
// so the splash never flashes white before splash.html paints. Keep in sync with the
// --cover-c value in splash.html.
const COVER_BG = '#1b1740';

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

// Minimal self-contained splash used only when splash.html cannot be loaded
// (e.g. a packaged build whose frontend dist predates the file). Guarantees the
// loading window is never a silent blank box — it still shows the branded cover
// color, name and a loading bar. Kept dependency-free (no external SVG) so it can
// never itself fail. Mirrors the cover palette of splash.html.
function fallbackSplashDataUrl(version: string): string {
    const ver = version ? `<div class="ver">v${version.replace(/^v/i, '')}</div>` : '';
    const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
        html,body{width:100%;height:100%;margin:0;overflow:hidden;color:#f6f7fb;
            font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;user-select:none}
        .cover{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
            justify-content:center;
            background:radial-gradient(120% 90% at 12% 8%,rgba(255,255,255,.12),transparent 46%),
            linear-gradient(135deg,#4f46e5 0%,#312e81 52%,#1b1740 100%)}
        .name{font-size:24px;font-weight:800;letter-spacing:3px}
        .name b{color:#e7c585}
        .ver{margin-top:10px;font-size:12px;color:rgba(246,247,251,.6)}
        .loader{position:absolute;left:0;right:0;bottom:0;height:3px;background:rgba(255,255,255,.1);overflow:hidden}
        .loader::before{content:"";position:absolute;top:0;left:0;height:100%;width:38%;
            background:linear-gradient(90deg,transparent,#e7c585 35%,#fff 50%,#e7c585 65%,transparent);
            animation:slide 1.35s cubic-bezier(.45,.05,.35,1) infinite}
        @keyframes slide{0%{transform:translateX(-120%)}100%{transform:translateX(360%)}}
    </style></head><body><div class="cover"><div class="name">BELIEVERS&nbsp;<b>SWORD</b></div>
        ${ver}<div class="loader"></div></div></body></html>`;
    return `data:text/html;charset=utf-8,${encodeURIComponent(html)}`;
}

export function createSplashWindow(): BrowserWindow {
    let iconPath = path.join(__dirname, 'assets', 'icon.ico');
    if (isDev || isBeta) iconPath = path.join('assets', 'icon.ico');

    const version = app.getVersion();
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
        backgroundColor: COVER_BG,
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
        splashWindow.loadURL(fallbackSplashDataUrl(version));
    });

    const query = { version };
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
