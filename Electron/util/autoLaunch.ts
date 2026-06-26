import { app } from 'electron';
import Log from 'electron-log';

/** Mirror the reminders setting into the OS login-item registration. */
export function setAutoLaunch(enabled: boolean): void {
    if (!app.isPackaged) return; // don't touch login items during dev
    try {
        app.setLoginItemSettings({
            openAtLogin: enabled,
            openAsHidden: true, // macOS hint
            args: ['--hidden'], // Windows: detect a login-launch
        });
    } catch (e) {
        Log.warn('[Reminders] setLoginItemSettings failed:', e);
    }
}

/** True when the app was auto-started at login (should stay in the tray). */
export function startedHidden(): boolean {
    if (process.argv.includes('--hidden')) return true;
    try {
        return app.getLoginItemSettings().wasOpenedAtLogin === true;
    } catch {
        return false;
    }
}
