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
    download: (args: any) => ipcRenderer.send('download', args),
    downloadModule: ({ urls, progress, done }: { urls: Array<string>; progress: Function; done: Function }) => {
        ipcRenderer.send('download-module', urls);
        ipcRenderer.on('download-module-done', (event, args) => {
            done();
        });
    },

    // Bookmarks Stuff
    saveBookMark: (args: any) => ipcRenderer.invoke('save-bookmark', JSON.parse(args)),
    getBookMarks: () => ipcRenderer.invoke('get-bookmarks'),
    deleteBookmark: (args: any) => ipcRenderer.invoke('delete-bookmark', JSON.parse(args)),

    // Highlights
    getChapterHighlights: (args: any) => ipcRenderer.invoke('getChapterHighlights', JSON.parse(args)),
    getHighlights: (args: any) => ipcRenderer.invoke('getHighLights', JSON.parse(args)),
    saveHighlight: (args: any) => ipcRenderer.invoke('saveHighlight', JSON.parse(args)),
});
