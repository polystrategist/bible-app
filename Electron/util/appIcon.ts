import { app } from 'electron';
import path from 'path';

// Resolve the app icon (.ico). In a packaged build (prod or beta) the icon ships
// via electron-builder `extraResources` and lives next to the asar in
// `resources/`; in dev it is read from the project's `assets/` folder relative to
// the CWD.
//
// NOTE: do not use `path.join(__dirname, 'assets', 'icon.ico')` — in production
// `__dirname` is inside the asar at `dist/`, and `dist/assets` only holds Vite
// frontend bundles, not the icon. That path loads an empty image, which makes the
// system tray icon invisible (the original "app not showing in system tray" bug).
export function appIconPath(): string {
    return app.isPackaged
        ? path.join(process.resourcesPath, 'icon.ico')
        : path.join('assets', 'icon.ico');
}
