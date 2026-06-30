import { appConfig } from '../ElectronStore/Configuration';

/**
 * Whether clicking the window's X hides the app to the tray instead of quitting.
 * Device-local, not synced. Defaults to true.
 */
export function getCloseToTray(): boolean {
    return appConfig.get('setting.closeToTray', true) as boolean;
}

export function setCloseToTray(v: boolean): void {
    appConfig.set('setting.closeToTray', v);
}
