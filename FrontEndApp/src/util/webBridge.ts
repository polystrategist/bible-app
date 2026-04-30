/**
 * Browser-side shim for `window.browserWindow` (the Electron preload bridge).
 *
 * In Electron, `window.browserWindow` is exposed via contextBridge from
 * `Electron/preload.ts` and routes to IPC handlers. In the browser there is
 * no IPC, so this file routes calls to the REST API backend instead.
 *
 * Convention:
 *   - Bible reads  -> real fetch calls to /api/bible/*
 *   - writes       -> log a warning, resolve with a no-op success shape
 *   - listeners    -> no-op (callback never fires)
 *   - window/OS    -> no-op
 */

const API_BASE = `${import.meta.env.VITE_API_BASE_URL ?? ''}/api`;

async function apiFetch<T>(path: string, fallback: T, options: RequestInit = {}): Promise<T> {
    try {
        const token = localStorage.getItem('auth_token');
        const isPublic = path.startsWith('/bible/');
        if (!isPublic && !token) return fallback;
        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            ...(options.headers as Record<string, string> ?? {}),
        };
        if (token) headers['Authorization'] = `Bearer ${token}`;
        const r = await fetch(`${API_BASE}${path}`, { ...options, headers });
        if (!r.ok) return fallback;
        return r.json() as Promise<T>;
    } catch {
        return fallback;
    }
}

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
    onWindowMaximized: () => { warnOnce('onWindowMaximized'); },
    getAppScale: async () => 1,
    setAppScale: async (scale: number) => scale,

    // ---------- Bible reads ----------
    getAvailableBibles: async () => apiFetch('/bible/versions', [] as string[]),
    deleteBible: async () => { warnOnce('deleteBible'); return { success: false, error: 'Not available on web' }; },
    getVerses: async (args: string) => {
        const { bible_versions, book_number, selected_chapter } = JSON.parse(args);
        const params = new URLSearchParams();
        (bible_versions as string[]).forEach((v) => params.append('versions[]', v));
        params.set('book_number', String(book_number));
        params.set('chapter', String(selected_chapter));
        return apiFetch(`/bible/verses?${params}`, []);
    },
    getVersesCount: async (args: string) => {
        const { bible_versions, book_number, selected_chapter } = JSON.parse(args);
        const params = new URLSearchParams();
        (bible_versions as string[]).forEach((v) => params.append('versions[]', v));
        params.set('book_number', String(book_number));
        params.set('chapter', String(selected_chapter));
        const res = await apiFetch<{ count: number }>(`/bible/verses/count?${params}`, { count: 0 });
        return res.count;
    },
    searchBible: async (args: string) => {
        const { search, bible_versions, book_number, book_numbers, page, limit } = JSON.parse(args);
        const params = new URLSearchParams({ q: search, page: String(page), limit: String(limit) });
        (bible_versions as string[]).forEach((v) => params.append('versions[]', v));
        if (Array.isArray(book_numbers) && book_numbers.length) {
            (book_numbers as number[]).forEach((b) => params.append('book_numbers[]', String(b)));
        } else if (book_number) {
            params.set('book_number', String(book_number));
        }
        return apiFetch(`/bible/search?${params}`, []);
    },

    // ---------- Highlights ----------
    getChapterHighlights: async (args: string) => {
        const { book_number, chapter } = JSON.parse(args);
        const params = new URLSearchParams({ book_number: String(book_number), chapter: String(chapter) });
        return apiFetch(`/highlights/chapter?${params}`, []);
    },
    getHighlights: async (args: string) => {
        const { page, search, limit } = JSON.parse(args);
        const params = new URLSearchParams({ page: String(page), limit: String(limit) });
        if (search) params.set('search', search);
        return apiFetch(`/highlights?${params}`, []);
    },
    saveHighlight: async (args: string) => {
        const body = JSON.parse(args);
        return apiFetch('/highlights', 0, { method: 'POST', body: JSON.stringify(body) });
    },
    deleteHighlight: async (args: { key: string }) => {
        return apiFetch(`/highlights/${encodeURIComponent(args.key)}`, null, { method: 'DELETE' });
    },

    // ---------- Downloads ----------
    downloadModule: () => { warnOnce('downloadModule'); },

    // ---------- Bookmarks ----------
    getBookMarks: async () => apiFetch('/bookmarks', {}),
    saveBookMark: async (args: string) => {
        const body = JSON.parse(args);
        return apiFetch('/bookmarks', {}, { method: 'POST', body: JSON.stringify(body) });
    },
    deleteBookmark: async (args: string) => {
        const { book_number, chapter, verse } = JSON.parse(args);
        const key = `${book_number}_${chapter}_${verse}`;
        return apiFetch(`/bookmarks/${encodeURIComponent(key)}`, null, { method: 'DELETE' });
    },

    // ---------- Clip Notes ----------
    getClipNotes: async (args: string) => {
        const { page, search, limit } = JSON.parse(args);
        const params = new URLSearchParams({ page: String(page), limit: String(limit) });
        if (search) params.set('search', search);
        return apiFetch(`/clip-notes?${params}`, []);
    },
    getChapterClipNotes: async (args: string) => {
        const { book_number, chapter } = JSON.parse(args);
        const params = new URLSearchParams({ book_number: String(book_number), chapter: String(chapter) });
        return apiFetch(`/clip-notes/chapter?${params}`, {} as any);
    },
    storeClipNote: async (args: string) => {
        const body = JSON.parse(args);
        return apiFetch('/clip-notes', null, { method: 'POST', body: JSON.stringify(body) });
    },
    deleteChapterClipNotes: async (args: string) => {
        const { book_number, chapter, verse } = JSON.parse(args);
        const key = `${book_number}_${chapter}_${verse}`;
        return apiFetch(`/clip-notes/${encodeURIComponent(key)}`, null, { method: 'DELETE' });
    },

    // ---------- Prayer List ----------
    getPrayerLists: async () => apiFetch('/prayer-list', []),
    savePrayerItem: async (args: string) => {
        const body = JSON.parse(args);
        return apiFetch('/prayer-list', null, { method: 'POST', body: JSON.stringify(body) });
    },
    resetPrayerListItems: async (args: string) => {
        const body = JSON.parse(args);
        return apiFetch('/prayer-list/reset', null, { method: 'POST', body: JSON.stringify(body) });
    },
    reorderPrayerListItems: async (args: string) => {
        const body = JSON.parse(args);
        return apiFetch('/prayer-list/reorder', null, { method: 'POST', body: JSON.stringify(body) });
    },
    deletePrayerListItem: async (key: string | number) => {
        return apiFetch(`/prayer-list/${encodeURIComponent(String(key))}`, null, { method: 'DELETE' });
    },

    // ---------- Misc ----------
    updateDownloadProgress: () => { /* no-op listener */ },
    openDonateWindow: () => { warnOnce('openDonateWindow'); },

    // ---------- Notes ----------
    getNotes: async () => apiFetch('/notes', []),
    upsertNote: async (args: { note_id: string; title: string; content: string }) => {
        return apiFetch('/notes', null, { method: 'POST', body: JSON.stringify(args) });
    },
    deleteNote: async (args: { note_id: string }) => {
        return apiFetch(`/notes/${encodeURIComponent(args.note_id)}`, null, { method: 'DELETE' });
    },

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
    getVerseText: async (args) => {
        const { bible_versions, book_number, chapter, verse } = args;
        const params = new URLSearchParams();
        (bible_versions as string[]).forEach((v) => params.append('versions[]', v));
        params.set('book_number', String(book_number));
        params.set('chapter', String(chapter));
        params.set('verse', String(verse));
        return apiFetch(`/bible/verse-text?${params}`, []);
    },
};

export function installWebBridge() {
    if (window.isElectron) return;
    if (window.browserWindow) return;
    window.browserWindow = stub;
}
