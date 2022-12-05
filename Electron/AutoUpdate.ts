import { autoUpdater } from 'electron-updater';

export default () => {
    autoUpdater.checkForUpdatesAndNotify();
};
