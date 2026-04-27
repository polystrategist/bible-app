/**
 * Browser-side shim for `window.browserWindow` (the Electron preload bridge).
 *
 * In Electron, `window.browserWindow` is exposed via contextBridge from
 * `Electron/preload.ts` and routes to IPC handlers. In the browser there is
 * no IPC, so this file installs a stub object with the same shape.
 *
 * Every method here returns a SAFE DEFAULT (empty list, no-op, or a shaped
 * "unavailable" response) instead of throwing — the goal of Phase 1 is to
 * load the UI on the web without crashes, not to provide real data. As the
 * web backend grows, replace stubs with real `fetch` calls one by one.
 *
 * Convention:
 *   - reads      -> return empty list / object / sensible default
 *   - writes     -> log a warning, resolve with a no-op success shape
 *   - listeners  -> no-op (callback never fires)
 *   - window/OS  -> no-op
 */

let warned = new Set<string>();
function warnOnce(method: string) {
    if (warned.has(method)) return;
    warned.add(method);
    // eslint-disable-next-line no-console
    console.warn(`[webBridge] ${method} is not implemented on web — returning a stub.`);
}

const stub: Window['browserWindow'] = {
    // ---------- Window / OS ----------
    versions: async () => ({
        chrome: '', node: '', electron: '', version: '', name: 'web',
    }),
    isWindowBrowserMaximized: async () => false,
    closeWindow: async () => { warnOnce('closeWindow'); },
    maximizeWindow: async () => { warnOnce('maximizeWindow'); },
    minimizeWindow: async () => { warnOnce('minimizeWindow'); },
    getAppScale: async () => 1,
    setAppScale: async (scale: number) => scale,

    // ---------- Bible reads ----------
    getAvailableBibles: async () => [],
    deleteBible: async () => { warnOnce('deleteBible'); return { success: false, error: 'Not available on web' }; },
    getVerses: async () => [],
    getVersesCount: async () => 0,
    searchBible: async () => ({ result: [], totalCount: 0 } as any),

    // ---------- Highlights ----------
    getChapterHighlights: async () => [],
    getHighlights: async () => [],
    saveHighlight: async () => { warnOnce('saveHighlight'); return null; },
    deleteHighlight: async () => { warnOnce('deleteHighlight'); return null; },

    // ---------- Downloads ----------
    downloadModule: () => { warnOnce('downloadModule'); },

    // ---------- Bookmarks ----------
    saveBookMark: async () => { warnOnce('saveBookMark'); return null; },
    getBookMarks: async () => ({}),
    deleteBookmark: async () => { warnOnce('deleteBookmark'); return null; },

    // ---------- Clip Notes ----------
    getClipNotes: async () => [],
    getChapterClipNotes: async () => ({} as any),
    storeClipNote: async () => { warnOnce('storeClipNote'); return null; },
    deleteChapterClipNotes: async () => { warnOnce('deleteChapterClipNotes'); return null; },

    // ---------- Prayer List ----------
    getPrayerLists: async () => [],
    savePrayerItem: async () => { warnOnce('savePrayerItem'); return null; },
    resetPrayerListItems: async () => { warnOnce('resetPrayerListItems'); return null; },
    reorderPrayerListItems: async () => { warnOnce('reorderPrayerListItems'); return null; },
    deletePrayerListItem: async () => { warnOnce('deletePrayerListItem'); return null; },

    // ---------- Misc ----------
    updateDownloadProgress: () => { /* no-op listener */ },
    openDonateWindow: () => { warnOnce('openDonateWindow'); },

    // ---------- Notes ----------
    getNotes: async () => [],
    upsertNote: async () => { warnOnce('upsertNote'); return null; },
    deleteNote: async () => { warnOnce('deleteNote'); return null; },

    // ---------- Dictionary ----------
    searchDictionary: async () => [],
    getDefinitions: async () => [],

    // ---------- Piper TTS (drop on web — Web Speech API fallback) ----------
    piperStatus: async () => ({ binaryReady: false, modelReady: false, modelName: '' }),
    piperInstall: async () => ({ success: false, error: 'Piper TTS is not available on web' }),
    piperUninstall: async () => ({ success: false, error: 'Piper TTS is not available on web' }),
    piperSpeak: async () => ({ success: false, error: 'Piper TTS is not available on web' }),
    piperVoices: async () => [],
    piperInstallModel: async () => ({ success: false, error: 'Piper TTS is not available on web' }),
    piperDeleteModel: async () => ({ success: false, error: 'Piper TTS is not available on web' }),
    piperOnInstallProgress: () => { /* no-op */ },
    piperOnModelProgress: () => { /* no-op */ },

    // ---------- Updates (drop on web) ----------
    getUpdateConfig: async () => ({
        provider: 'unavailable',
        canCheckForUpdates: false,
        message: 'Updates are managed by your browser on the web.',
    }),
    checkForUpdates: async () => ({
        success: false,
        provider: 'unavailable',
        message: 'Updates are managed by your browser on the web.',
    }),
    installUpdate: async () => { /* no-op */ },
    downloadUpdate: async () => { /* no-op */ },
    openStoreUpdates: async () => ({ success: false, error: 'Not available on web' }),
    onUpdateAvailable: () => { /* no-op */ },
    onUpdateProgress: () => { /* no-op */ },
    onUpdateDownloaded: () => { /* no-op */ },

    // ---------- Bible Import (drop on web — no FS access) ----------
    importBibleSelectFile: async () => ({ canceled: true }),
    importBibleValidate: async () => ({ valid: false, error: 'Bible import is not available on web' }),
    importBibleCheckDuplicate: async () => ({ exists: false }),
    importBible: async () => ({ success: false, error: 'Bible import is not available on web' }),

    // ---------- Sync (no-op on web; web talks to backend directly) ----------
    logSyncChange: async () => null,
    getUnsyncedChanges: async () => [],
    markAsSynced: async () => null,
    getLastSyncTimestamp: async () => '',
    updateLastSyncTimestamp: async () => null,
    getSyncSetting: async (key: string) => {
        if (key === 'sync_enabled') return '0';
        return null;
    },
    setSyncSetting: async () => null,
    applyPullData: async () => ({ success: true }),
    onSyncBeforeQuit: () => { /* no-op */ },
    notifySyncBeforeQuitDone: () => { /* no-op */ },

    // ---------- Export (TODO: replace with client-side jsPDF/docx libs) ----------
    exportToPdf: async () => { warnOnce('exportToPdf'); return { success: false, error: 'Not yet on web' }; },
    exportToDocx: async () => { warnOnce('exportToDocx'); return { success: false, error: 'Not yet on web' }; },

    // ---------- Shell ----------
    openExternal: async (url: string) => { window.open(url, '_blank', 'noopener,noreferrer'); },

    // ---------- Cross References ----------
    getCrossReferences: async () => [],
    getVerseText: async () => [],
};

export function installWebBridge() {
    if (window.isElectron) return;
    if (window.browserWindow) return;
    window.browserWindow = stub;
}
