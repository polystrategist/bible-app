import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('browserWindow', {
    minimizeWindow: () => ipcRenderer.invoke('minimizeWindow'),
    maximizeWindow: () => ipcRenderer.invoke('maximizeWindow'),
    closeWindow: () => ipcRenderer.invoke('closeWindow'),
    isWindowBrowserMaximized: () => ipcRenderer.invoke('isWindowBrowserMaximized'),
    getAppScale: () => ipcRenderer.invoke('getAppScale'),
    setAppScale: (scale: number) => ipcRenderer.invoke('setAppScale', scale),
    versions: () => ipcRenderer.invoke('versions'),
    getAvailableBibles: () => ipcRenderer.invoke('availableBibles'),
    getVerses: (args: string) => ipcRenderer.invoke('getVerses', JSON.parse(args)),
    getVersesCount: (args: string) => ipcRenderer.invoke('getVersesCount', JSON.parse(args)),
    searchBible: (args: string) => ipcRenderer.invoke('searchBible', JSON.parse(args)),
    download: (args: any) => ipcRenderer.send('download', args),
    downloadModule: ({ urls, done, percentage, cancel }: { urls: Array<string>; percentage: Function; done: Function; cancel: Function }, moduleData?: { title: string; description: string; is_zipped: boolean, file_name: string }) => {
        ipcRenderer.send('download-module', urls, moduleData);
        // Listen for the event from the main process
        ipcRenderer.on('download-module-progress', (_, progressValue) => {
            percentage(progressValue);
        });
        ipcRenderer.on('download-module-done', () => {
            done();
        });
        ipcRenderer.on('download-module-cancel', () => {
            cancel();
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

    // Dictionary
    searchDictionary: (args: any) => ipcRenderer.invoke('searchDictionary', args),
    getDefinitions: (word: string) => ipcRenderer.invoke('getDefinitions', word),

    // Piper TTS
    piperStatus: () => ipcRenderer.invoke('piper:status'),
    piperInstall: () => ipcRenderer.invoke('piper:install'),
    piperUninstall: () => ipcRenderer.invoke('piper:uninstall'),
    piperSpeak: (text: string, modelId?: string) => ipcRenderer.invoke('piper:speak', text, modelId),
    piperVoices: () => ipcRenderer.invoke('piper:voices'),
    piperInstallModel: (voiceId: string) => ipcRenderer.invoke('piper:installModel', voiceId),
    piperDeleteModel: (voiceId: string) => ipcRenderer.invoke('piper:deleteModel', voiceId),
    piperOnInstallProgress: (cb: (data: { step: string; percent: number }) => void) => {
        ipcRenderer.removeAllListeners('piper:install-progress');
        ipcRenderer.on('piper:install-progress', (_event, data) => cb(data));
    },
    piperOnModelProgress: (cb: (data: { voiceId: string; percent: number }) => void) => {
        ipcRenderer.removeAllListeners('piper:model-progress');
        ipcRenderer.on('piper:model-progress', (_event, data) => cb(data));
    },

    // Compare Verse Window
    openCompareVerseWindow: (args: { book_number: number; chapter: number; verse: number; book_name: string }) =>
        ipcRenderer.invoke('compareVerse:open', args),
    compareVerseGetVerse: (args: { book_number: number; chapter: number; verse: number }) =>
        ipcRenderer.invoke('compareVerse:getVerse', args),
    closeCurrentWindow: () => ipcRenderer.invoke('closeCurrentWindow'),

    // Daily Devotional
    getTodayDevotional: () => ipcRenderer.invoke('getTodayDevotional'),
    getDevotionalByDay: (day: number) => ipcRenderer.invoke('getDevotionalByDay', day),

    // Commentaries
    getCommentaryForVerse: (args: string) => ipcRenderer.invoke('getCommentaryForVerse', JSON.parse(args)),
    hasCommentary: (version: string) => ipcRenderer.invoke('hasCommentary', version),
    getAvailableCommentaries: () => ipcRenderer.invoke('availableCommentaries'),

    // Updates
    checkForUpdates: () => ipcRenderer.invoke('check-for-updates'),
    installUpdate: () => ipcRenderer.invoke('install-update'),
    onUpdateAvailable: (cb: () => void) => {
        ipcRenderer.removeAllListeners('update-available');
        ipcRenderer.on('update-available', cb);
    },
    onUpdateDownloaded: (cb: () => void) => {
        ipcRenderer.removeAllListeners('update-downloaded');
        ipcRenderer.on('update-downloaded', cb);
    },
    onUpdateProgress: (cb: (percent: number) => void) => {
        ipcRenderer.removeAllListeners('download-progress');
        ipcRenderer.on('download-progress', (_e, percent) => cb(percent));
    },

    // Bible Import
    importBibleSelectFile: () => ipcRenderer.invoke('import-bible:select-file'),
    importBibleValidate: (filePath: string) => ipcRenderer.invoke('import-bible:validate', filePath),
    importBibleCheckDuplicate: (title: string) => ipcRenderer.invoke('import-bible:check-duplicate', title),
    importBible: (args: { filePath: string; title: string; description: string }) => ipcRenderer.invoke('import-bible:import', args),

    // Sync Operations
    logSyncChange: (entry: any) => ipcRenderer.invoke('logSyncChange', entry),
    getUnsyncedChanges: () => ipcRenderer.invoke('getUnsyncedChanges'),
    markAsSynced: (ids: number[]) => ipcRenderer.invoke('markAsSynced', ids),
    getLastSyncTimestamp: () => ipcRenderer.invoke('getLastSyncTimestamp'),
    updateLastSyncTimestamp: (timestamp: string) => ipcRenderer.invoke('updateLastSyncTimestamp', timestamp),
    getSyncSetting: (key: string) => ipcRenderer.invoke('getSyncSetting', key),
    setSyncSetting: (key: string, value: any) => ipcRenderer.invoke('setSyncSetting', key, value),
    applyPullData: (data: any) => ipcRenderer.invoke('applyPullData', data),

    // Export
    exportToPdf: (args: { html: string; filename: string }) => ipcRenderer.invoke('exportToPdf', args),
    exportToDocx: (args: { html: string; filename: string }) => ipcRenderer.invoke('exportToDocx', args),
});
