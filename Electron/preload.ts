import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('browserWindow', {
    minimizeWindow: () => ipcRenderer.invoke('minimizeWindow'),
    maximizeWindow: () => ipcRenderer.invoke('maximizeWindow'),
    closeWindow: () => ipcRenderer.invoke('closeWindow'),
    isWindowBrowserMaximized: () => ipcRenderer.invoke('isWindowBrowserMaximized'),
    getAppScale: () => ipcRenderer.invoke('getAppScale'),
    setAppScale: (scale: number) => ipcRenderer.invoke('setAppScale', scale),
    // Tell main the app has fully rendered, so it can close the splash and show the window.
    appReady: () => ipcRenderer.send('app-ready'),
    // Persist the current theme colors so the next launch's splash can match them.
    setSplashTheme: (payload: { bg: string; text: string; accent: string }) =>
        ipcRenderer.invoke('set-splash-theme', payload),
    versions: () => ipcRenderer.invoke('versions'),
    getAvailableBibles: () => ipcRenderer.invoke('availableBibles'),
    deleteBible: (fileName: string) => ipcRenderer.invoke('deleteBible', fileName),
    getVerses: (args: string) => ipcRenderer.invoke('getVerses', JSON.parse(args)),
    getVersesCount: (args: string) => ipcRenderer.invoke('getVersesCount', JSON.parse(args)),
    searchBible: (args: string) => ipcRenderer.invoke('searchBible', JSON.parse(args)),
    download: (args: any) => ipcRenderer.send('download', args),
    downloadModule: ({ urls, done, percentage, cancel }: { urls: Array<string>; percentage: Function; done: Function; cancel: Function }, moduleData?: { title: string; description: string; is_zipped: boolean; file_name: string; module_type?: string }) => {
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
    deleteHighlight: (args: { key: string }) =>
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
    reorderPrayerListItems: (args: any) =>
        ipcRenderer.invoke('reorderPrayerListItems', JSON.parse(args)),
    deletePrayerListItem: (args: any) => ipcRenderer.invoke('deletePrayerListItem', args),

    // Prayer-streak days
    getPrayerDays: () => ipcRenderer.invoke('getPrayerDays'),
    markPrayedToday: (durationSeconds?: number) => ipcRenderer.invoke('markPrayedToday', durationSeconds),

    // Devotion-streak days
    getDevotionDays: () => ipcRenderer.invoke('getDevotionDays'),
    markDevotionToday: () => ipcRenderer.invoke('markDevotionToday'),
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

    // Notes
    getNotes: () => ipcRenderer.invoke('getNotes'),
    upsertNote: (args: any) => ipcRenderer.invoke('upsertNote', args),
    deleteNote: (args: any) => ipcRenderer.invoke('deleteNote', args),

    // Dictionary
    searchDictionary: (args: any) => ipcRenderer.invoke('searchDictionary', args),
    getDefinitions: (word: string) => ipcRenderer.invoke('getDefinitions', word),

    // Strong's lexicon
    getStrongsDefinition: (strongNumber: string) =>
        ipcRenderer.invoke('getStrongsDefinition', strongNumber),

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
    getTodayDevotional: (languageCode: string = 'en') => ipcRenderer.invoke('getTodayDevotional', languageCode),
    getDevotionalByDay: (day: number, languageCode: string = 'en') => ipcRenderer.invoke('getDevotionalByDay', day, languageCode),

    // AI Assistant conversation history
    getAiConversations: () => ipcRenderer.invoke('getAiConversations'),
    getAiConversation: (id: string) => ipcRenderer.invoke('getAiConversation', id),
    saveAiConversation: (payload: any) => ipcRenderer.invoke('saveAiConversation', payload),
    deleteAiConversation: (id: string) => ipcRenderer.invoke('deleteAiConversation', id),

    // AI insight/sermon local cache
    getAiInsight: (key: string) => ipcRenderer.invoke('getAiInsight', key),
    saveAiInsight: (payload: any) => ipcRenderer.invoke('saveAiInsight', payload),
    pruneAiInsights: () => ipcRenderer.invoke('pruneAiInsights'),

    // Commentaries
    getCommentaryForVerse: (args: string) => ipcRenderer.invoke('getCommentaryForVerse', JSON.parse(args)),
    hasCommentary: (version: string) => ipcRenderer.invoke('hasCommentary', version),
    getAvailableCommentaries: () => ipcRenderer.invoke('availableCommentaries'),

    // Updates
    getUpdateConfig: () => ipcRenderer.invoke('get-update-config'),
    checkForUpdates: () => ipcRenderer.invoke('check-for-updates'),
    installUpdate: () => ipcRenderer.invoke('install-update'),
    downloadUpdate: () => ipcRenderer.invoke('download-update'),
    openStoreUpdates: () => ipcRenderer.invoke('open-store-updates'),
    onWindowMaximized: (cb: (isMaximized: boolean) => void) => {
        ipcRenderer.removeAllListeners('window:maximized');
        ipcRenderer.on('window:maximized', (_e, value) => cb(value));
    },
    onUpdateAvailable: (cb: (version: string) => void) => {
        ipcRenderer.removeAllListeners('update-available');
        ipcRenderer.on('update-available', (_e, version) => cb(version));
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
    importBibleSelectFile: (source: string) => ipcRenderer.invoke('import-bible:select-file', source),
    importBibleValidate: (args: { filePath: string; source: string }) => ipcRenderer.invoke('import-bible:validate', args),
    importBibleCheckDuplicate: (title: string) => ipcRenderer.invoke('import-bible:check-duplicate', title),
    importBible: (args: { filePath: string; title: string; description: string; source: string }) => ipcRenderer.invoke('import-bible:import', args),

    // Sync Operations
    logSyncChange: (entry: any) => ipcRenderer.invoke('logSyncChange', entry),
    getUnsyncedChanges: () => ipcRenderer.invoke('getUnsyncedChanges'),
    markAsSynced: (ids: number[]) => ipcRenderer.invoke('markAsSynced', ids),
    getLastSyncTimestamp: () => ipcRenderer.invoke('getLastSyncTimestamp'),
    updateLastSyncTimestamp: (timestamp: string) => ipcRenderer.invoke('updateLastSyncTimestamp', timestamp),
    getSyncSetting: (key: string) => ipcRenderer.invoke('getSyncSetting', key),
    setSyncSetting: (key: string, value: any) => ipcRenderer.invoke('setSyncSetting', key, value),
    applyPullData: (data: any) => ipcRenderer.invoke('applyPullData', data),

    // Sermons offline cache + favorites
    replaceCachedSermons: (sermons: any[]) => ipcRenderer.invoke('replaceCachedSermons', sermons),
    getCachedSermons: () => ipcRenderer.invoke('getCachedSermons'),
    getSermonFavorites: () => ipcRenderer.invoke('getSermonFavorites'),
    getSermonFavoriteIds: () => ipcRenderer.invoke('getSermonFavoriteIds'),
    addSermonFavorite: (sermon: any) => ipcRenderer.invoke('addSermonFavorite', sermon),
    removeSermonFavorite: (sermonId: number) => ipcRenderer.invoke('removeSermonFavorite', sermonId),
    onSyncBeforeQuit: (cb: () => void) => ipcRenderer.on('app:sync-before-quit', cb),
    notifySyncBeforeQuitDone: () => ipcRenderer.send('app:sync-before-quit-done'),

    // Export
    exportToPdf: (args: { html: string; filename: string }) => ipcRenderer.invoke('exportToPdf', args),
    exportToDocx: (args: { html: string; filename: string }) => ipcRenderer.invoke('exportToDocx', args),

    // Shell
    openExternal: (url: string) => ipcRenderer.invoke('openExternal', url),

    // Clipboard (native — navigator.clipboard is unreliable in the renderer)
    writeClipboard: (text: string) => ipcRenderer.invoke('writeClipboard', text),

    // Cross References
    getCrossReferences: (args: { book_number: number; chapter: number; verse: number }) =>
        ipcRenderer.invoke('getCrossReferences', args),
    getVerseText: (args: { bible_versions: string[]; book_number: number; chapter: number; verse: number }) =>
        ipcRenderer.invoke('getVerseText', args),

    // Games — lives
    gameGetLives: () => ipcRenderer.invoke('game:getLives'),
    gameLoseLife: () => ipcRenderer.invoke('game:loseLife'),
    gameNextRecoveryAt: () => ipcRenderer.invoke('game:nextRecoveryAt'),
    gameRefillLives: () => ipcRenderer.invoke('game:refillLives'),
    gameResetProgress: () => ipcRenderer.invoke('game:resetProgress'),

    // Games — Q&A
    qaGetGroups: () => ipcRenderer.invoke('qa:getGroups'),
    qaGetQuestionsForGroup: (groupId: number) => ipcRenderer.invoke('qa:getQuestionsForGroup', groupId),
    qaGetAllGroupProgress: () => ipcRenderer.invoke('qa:getAllGroupProgress'),
    qaSaveGroupProgress: (args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }) =>
        ipcRenderer.invoke('qa:saveGroupProgress', args),

    // Games — True/False
    tfGetGroups: () => ipcRenderer.invoke('tf:getGroups'),
    tfGetStatementsForGroup: (groupId: number) => ipcRenderer.invoke('tf:getStatementsForGroup', groupId),
    tfGetAllGroupProgress: () => ipcRenderer.invoke('tf:getAllGroupProgress'),
    tfSaveGroupProgress: (args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }) =>
        ipcRenderer.invoke('tf:saveGroupProgress', args),

    // Games — Four Pictures (local-only)
    fpGetLevels: () => ipcRenderer.invoke('fp:getLevels'),
    fpGetSolvedLevelIds: () => ipcRenderer.invoke('fp:getSolvedLevelIds'),
    fpMarkLevelSolved: (levelId: number) => ipcRenderer.invoke('fp:markLevelSolved', levelId),
    fpGetImagesBasePath: () => ipcRenderer.invoke('fp:getImagesBasePath'),

    // Encouragement reminders
    getReminderEnabled: () => ipcRenderer.invoke('reminders:get-enabled'),
    setReminderEnabled: (value: boolean) => ipcRenderer.invoke('reminders:set-enabled', value),
    getReminderAutoStart: () => ipcRenderer.invoke('reminders:get-autostart'),
    setReminderAutoStart: (value: boolean) => ipcRenderer.invoke('reminders:set-autostart', value),
    reminderRecordActivity: () => ipcRenderer.invoke('reminders:record-activity'),
});
