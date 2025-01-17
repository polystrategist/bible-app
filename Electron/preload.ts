import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('browserWindow', {
    minimizeWindow: () => ipcRenderer.invoke('minimizeWindow'),
    maximizeWindow: () => ipcRenderer.invoke('maximizeWindow'),
    closeWindow: () => ipcRenderer.invoke('closeWindow'),
    isWindowBrowserMaximized: () => ipcRenderer.invoke('isWindowBrowserMaximized'),
    versions: () => ipcRenderer.invoke('versions'),
    getAvailableBibles: () => ipcRenderer.invoke('availableBibles'),
    getVerses: (args: string) => ipcRenderer.invoke('getVerses', JSON.parse(args)),
    getVersesCount: (args: string) => ipcRenderer.invoke('getVersesCount', JSON.parse(args)),
    searchBible: (args: string) => ipcRenderer.invoke('searchBible', JSON.parse(args)),
    download: (args: any) => ipcRenderer.send('download', args),
    downloadModule: ({ urls, done }: { urls: Array<string>; done: Function }) => {
        ipcRenderer.send('download-module', urls);
        ipcRenderer.on('download-module-done', () => {
            done();
        });
    },

    // Bookmarks Stuff
    saveBookMark: (args: any) => ipcRenderer.invoke('save-bookmark', JSON.parse(args)),
    getBookMarks: () => ipcRenderer.invoke('get-bookmarks'),
    deleteBookmark: (args: any) => ipcRenderer.invoke('delete-bookmark', JSON.parse(args)),

    // Highlights
    getChapterHighlights: (args: any) =>
        ipcRenderer.invoke('getChapterHighlights', JSON.parse(args)),
    getHighlights: (args: any) => ipcRenderer.invoke('getHighLights', JSON.parse(args)),
    saveHighlight: (args: any) => ipcRenderer.invoke('saveHighlight', JSON.parse(args)),
    deleteHighlight: (args: { study_space_id: number | string; key: string }) =>
        ipcRenderer.invoke('deleteHighlight', args),

    // Clip Notes
    getClipNotes: (args: any) => ipcRenderer.invoke('getClipNotes', JSON.parse(args)),
    storeClipNote: (args: any) => ipcRenderer.invoke('storeClipNote', JSON.parse(args)),
    getChapterClipNotes: (args: any) => ipcRenderer.invoke('getChapterClipNotes', JSON.parse(args)),
    deleteChapterClipNotes: (args: any) =>
        ipcRenderer.invoke('deleteChapterClipNotes', JSON.parse(args)),

    // Prayer List
    getPrayerLists: () => ipcRenderer.invoke('getPrayerLists'),
    savePrayerItem: (args: any) => ipcRenderer.invoke('savePrayerItem', JSON.parse(args)),
    resetPrayerListItems: (args: any) =>
        ipcRenderer.invoke('resetPrayerListItems', JSON.parse(args)),
    deletePrayerListItem: (args: any) => ipcRenderer.invoke('deletePrayerListItem', args),
    updateDownloadProgress: (progress: { percentage: Function; done: Function }) => {
        // Listen for the event from the main process
        ipcRenderer.on('download-progress', (_, percentage) => {
            progress.percentage(percentage);
        });

        ipcRenderer.on('update-downloaded', () => {
            progress.done();
        });
    },

    // WINDOW OPENERS
    openDonateWindow: () => ipcRenderer.invoke('open-donate-window'),

    // Space Study Events
    getSpaceStudyList: (args: any) => ipcRenderer.invoke('getSpaceStudyList', args),
    storeSpaceStudy: (args: any) => ipcRenderer.invoke('storeSpaceStudy', JSON.parse(args)),
    deleteSpaceStudy: (id: number) => ipcRenderer.invoke('deleteSpaceStudy', id),
    selectStudySpace: (id: number | string) => ipcRenderer.invoke('selectStudySpace', id),
    getSelectedSpaceStudy: () => ipcRenderer.invoke('getSelectedSpaceStudy'),

    // Note
    getNote: (space_study_id: number) => ipcRenderer.invoke('getNote', space_study_id),
    saveNote: (args: any) => ipcRenderer.invoke('saveNote', args),
});
