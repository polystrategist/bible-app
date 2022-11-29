import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('browserWindow', {
    minimizeWindow: () => ipcRenderer.invoke('minimizeWindow'),
    maximizeWindow: () => ipcRenderer.invoke('maximizeWindow'),
    closeWindow: () => ipcRenderer.invoke('closeWindow'),
    isWindowBrowserMaximized: () => ipcRenderer.invoke('isWindowBrowserMaximized'),
    versions: () => ipcRenderer.invoke('versions'),
    getAvailableBibles: () => ipcRenderer.invoke('availableBibles'),
    getVerses: (args: string) => ipcRenderer.invoke('getVerses', JSON.parse(args)),
    searchBible: (args: string) => ipcRenderer.invoke('searchBible', JSON.parse(args)),
    download: (args: any) => {
        ipcRenderer.send('download', args);
    },
    downloadModule: ({ url, progress, done }: { url: string; progress: Function; done: Function }) => {
        ipcRenderer.send('download-module', url);
        ipcRenderer.on('download-module-inprogress', (event, percentage) => {
            progress(percentage);
        });
        ipcRenderer.on('download-module-done', (event, args) => {
            done();
        });
    },
});
