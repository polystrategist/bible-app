import { app, BrowserWindow, dialog } from 'electron';
import { autoUpdater, UpdateInfo } from 'electron-updater';

export default (mainWindow: BrowserWindow) => {
    if (app.isPackaged) {
        autoUpdater.autoDownload = false;
        autoUpdater.autoInstallOnAppQuit = true;
        autoUpdater.checkForUpdates();

        autoUpdater.on('update-available', () => {
            // Show a dialog to the user indicating that an update is available
            dialog.showMessageBox({
                type: 'info',
                buttons: ['Download Update', 'Cancel'],
                title: 'Update Available',
                message: 'A new update is available. Do you want to download and install it?'
            }).then((response) => {
                if (response.response === 0) {
                    // If the user clicks 'Download Update'
                    autoUpdater.downloadUpdate();
                }
            });
        });

        autoUpdater.on('download-progress', (progressObj) => {
            // Calculate the download progress percentage
            const downloadPercentage = Math.floor(progressObj.percent);

            // Update UI with progress percentage
            mainWindow.webContents.send('download-progress', downloadPercentage);
        });

        autoUpdater.addListener('update-downloaded', (info: UpdateInfo) => {
            // Update UI with progress percentage
            mainWindow.webContents.send('update-downloaded');
            dialog
                .showMessageBox({
                    type: 'info',
                    buttons: ['Install and Restart', 'Later'],
                    title: 'Update Ready',
                    message: 'The update has been downloaded. Do you want to install and restart the application?'
                })
                .then(({ response }) => {
                    if (response == 0 || response == 2) {
                        autoUpdater.quitAndInstall();
                    }
                });
        });
    }

    autoUpdater.on('error', (error) => {
        // Handle update error
        dialog
            .showMessageBox({
                type: 'error',
                buttons: ['OK'],
                title: 'Error Updating!',
                message: 'Their is an Error Updating, the developer is working on a fix right now.'
            })
            .then(({ response }) => {
                if (response == 0 || response == 2) {
                    autoUpdater.quitAndInstall();
                }
            });
    });
};
