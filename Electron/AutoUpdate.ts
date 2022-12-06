import { app, dialog } from 'electron';
import { autoUpdater, UpdateInfo } from 'electron-updater';

export default () => {
    autoUpdater.checkForUpdates();
    autoUpdater.addListener('update-downloaded', (info: UpdateInfo) => {
        dialog
            .showMessageBox({
                title: 'Restart Believers Sword',
                type: 'info',
                message: `New version "Believers Sword ${info.version}" has been successfully downloaded.`,
                buttons: ['Yes', 'Later'],
                cancelId: 1,
            })
            .then(({ response }) => {
                if (response == 0) {
                    app.relaunch();
                    app.exit();
                }
            });
    });
};
