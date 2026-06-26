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
const bibleVersesCache = new Map<string, Promise<any[]>>();

async function apiFetch<T>(path: string, fallback: T, options: RequestInit = {}): Promise<T> {
    try {
        const token = localStorage.getItem('auth_token');
        const isPublic = path.startsWith('/bible/') || path.startsWith('/devotional/');
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

/**
 * Largest `limit` the REST API accepts on paginated list endpoints
 * (clip-notes, highlights). Requests above this 422 with a validation error.
 */
const API_MAX_LIMIT = 200;

/**
 * Fetch a paginated list endpoint, honoring the caller's requested `limit`.
 *
 * Callers (e.g. the sidebar lists) pass a large `limit` to mean "give me the
 * whole dataset for virtual scrolling", but the API caps `limit` at
 * {@link API_MAX_LIMIT}. When more is requested we page through the endpoint in
 * API-legal chunks and concatenate, stopping once a short page signals the end.
 */
async function fetchPagedList(
    path: string,
    opts: { page?: number; search?: string | null; limit?: number },
): Promise<any[]> {
    const requested = Number(opts.limit) || API_MAX_LIMIT;
    const search = opts.search ?? null;

    // Small request — a single page honoring the caller's page/limit verbatim.
    if (requested <= API_MAX_LIMIT) {
        const params = new URLSearchParams({ page: String(opts.page ?? 1), limit: String(requested) });
        if (search) params.set('search', String(search));
        return apiFetch(`${path}?${params}`, []);
    }

    // Large request — walk every page until the dataset is exhausted. The page
    // cap is a safety net against an unbounded loop, set well above any realistic
    // per-user record count.
    const all: any[] = [];
    const MAX_PAGES = 500;
    for (let page = 1; page <= MAX_PAGES; page++) {
        const params = new URLSearchParams({ page: String(page), limit: String(API_MAX_LIMIT) });
        if (search) params.set('search', String(search));
        const rows = await apiFetch<any[]>(`${path}?${params}`, []);
        if (!Array.isArray(rows) || rows.length === 0) break;
        all.push(...rows);
        if (rows.length < API_MAX_LIMIT) break;
    }
    return all;
}

function buildBibleVersesPath(version: string, bookNumber: number, chapter: number) {
    const params = new URLSearchParams();
    params.append('versions[]', version);
    params.set('book_number', String(bookNumber));
    params.set('chapter', String(chapter));

    return `/bible/verses?${params}`;
}

function getBibleVersesRows(version: string, bookNumber: number, chapter: number) {
    const path = buildBibleVersesPath(version, bookNumber, chapter);
    const cached = bibleVersesCache.get(path);
    if (cached) return cached;

    const request = apiFetch<any[]>(path, []);
    bibleVersesCache.set(path, request);
    return request;
}

function mergeVerseRows(target: any[], rows: any[], fallbackVersion: string) {
    rows.forEach((row: any) => {
        if (!row) return;

        const verseNumber = Number(row.verse);
        if (!verseNumber) return;

        if (!target[verseNumber - 1]) {
            target[verseNumber - 1] = {
                book_number: row.book_number,
                chapter: row.chapter,
                verse: verseNumber,
                version: [],
            };
        }

        const versionRows = Array.isArray(row.version)
            ? row.version
            : [{ version: row.version ?? fallbackVersion, text: row.text }];

        versionRows.forEach((versionRow: any) => {
            const version = versionRow?.version ?? fallbackVersion;
            const text = versionRow?.text ?? '';

            if (!version || target[verseNumber - 1].version.some((item: any) => item.version === version)) {
                return;
            }

            target[verseNumber - 1].version.push({ version, text });
        });
    });
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
    appReady: () => { /* no-op on web — no splash window */ },
    setSplashTheme: async () => { /* no-op on web — no splash window */ },

    // ---------- Bible reads ----------
    getAvailableBibles: async () => apiFetch('/bible/version-details', [] as string[]),
    deleteBible: async () => { warnOnce('deleteBible'); return { success: false, error: 'Not available on web' }; },
    getVerses: async (args: string) => {
        const { bible_versions, book_number, selected_chapter } = JSON.parse(args);
        const selectedVersions = bible_versions as string[];
        const responses = await Promise.all(
            selectedVersions.map((version) =>
                getBibleVersesRows(version, book_number, selected_chapter),
            ),
        );

        const mergedRows: any[] = [];
        responses.forEach((rows, index) => {
            mergeVerseRows(mergedRows, rows, selectedVersions[index]);
        });

        return mergedRows.filter(Boolean);
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
        return fetchPagedList('/highlights', { page, search, limit });
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
        return fetchPagedList('/clip-notes', { page, search, limit });
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

    // ---------- Prayer-streak days ----------
    // The web build has no dedicated prayer-days REST route, so the streak is
    // kept in localStorage (per-browser). Electron + mobile persist + sync it.
    getPrayerDays: async () => {
        try {
            const raw = localStorage.getItem('prayer_days');
            const days: string[] = raw ? JSON.parse(raw) : [];
            const durRaw = localStorage.getItem('prayer_days_duration');
            const dur: Record<string, number> = durRaw ? JSON.parse(durRaw) : {};
            return days.map((day) => ({ day, duration: dur[day] ?? 0 }));
        } catch {
            return [];
        }
    },
    markPrayedToday: async (durationSeconds = 0) => {
        const d = new Date();
        const day = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
        try {
            const raw = localStorage.getItem('prayer_days');
            const days: string[] = raw ? JSON.parse(raw) : [];
            if (!days.includes(day)) {
                days.push(day);
                localStorage.setItem('prayer_days', JSON.stringify(days));
            }
            const add = Math.max(0, Math.floor(durationSeconds || 0));
            if (add > 0) {
                const durRaw = localStorage.getItem('prayer_days_duration');
                const dur: Record<string, number> = durRaw ? JSON.parse(durRaw) : {};
                dur[day] = (dur[day] ?? 0) + add;
                localStorage.setItem('prayer_days_duration', JSON.stringify(dur));
            }
        } catch { /* ignore */ }
        return day;
    },
    getDevotionDays: async () => {
        try {
            const raw = localStorage.getItem('devotion_days');
            const days: string[] = raw ? JSON.parse(raw) : [];
            return days.map((day) => ({ day }));
        } catch {
            return [];
        }
    },
    markDevotionToday: async () => {
        const d = new Date();
        const day = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
        try {
            const raw = localStorage.getItem('devotion_days');
            const days: string[] = raw ? JSON.parse(raw) : [];
            if (!days.includes(day)) {
                days.push(day);
                localStorage.setItem('devotion_days', JSON.stringify(days));
            }
        } catch { /* ignore */ }
        return day;
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

    // ---------- AI Assistant conversation history (backend; paid feature) ----------
    getAiConversations: async () => apiFetch('/ai-conversations', [] as any[]),
    getAiConversation: async (id: string) =>
        apiFetch(`/ai-conversations/${encodeURIComponent(id)}`, null),
    saveAiConversation: async (payload) =>
        apiFetch('/ai-conversations', null, { method: 'POST', body: JSON.stringify(payload) }),
    deleteAiConversation: async (id: string) => {
        const res = await apiFetch<boolean | null>(
            `/ai-conversations/${encodeURIComponent(id)}`, null, { method: 'DELETE' },
        );
        return res === true;
    },

    // ---------- AI insight/sermon cache (local-only convenience; skipped on web — always online) ----------
    getAiInsight: async () => null,
    saveAiInsight: async () => false,
    pruneAiInsights: async () => false,

    // ---------- Sermons offline cache + favorites (no-op on web — backend is source of truth) ----------
    replaceCachedSermons: async () => ({ success: false, error: 'Not available on web' }),
    getCachedSermons: async () => [],
    getSermonFavorites: async () => [],
    getSermonFavoriteIds: async () => [],
    addSermonFavorite: async () => ({ success: false, error: 'Not available on web' }),
    removeSermonFavorite: async () => ({ success: false, error: 'Not available on web' }),

    // ---------- Export (TODO: replace with client-side jsPDF/docx libs) ----------
    exportToPdf: async () => { warnOnce('exportToPdf'); return { success: false, error: 'Not yet on web' }; },
    exportToDocx: async () => { warnOnce('exportToDocx'); return { success: false, error: 'Not yet on web' }; },

    // ---------- Shell ----------
    openExternal: async (url: string) => { window.open(url, '_blank', 'noopener,noreferrer'); },

    // ---------- Clipboard ----------
    writeClipboard: async (text: string) => { await navigator.clipboard.writeText(text); },

    // ---------- Cross References ----------
    // ---------- Devotional ----------
    getTodayDevotional: async (languageCode: string = 'en') => {
        const params = new URLSearchParams({ lang: languageCode });
        return apiFetch(`/devotional/today?${params}`, null);
    },
    getDevotionalByDay: async (day: number, languageCode: string = 'en') => {
        const params = new URLSearchParams({ lang: languageCode });
        return apiFetch(`/devotional/${day}?${params}`, null);
    },

    getCrossReferences: async (args) => {
        const params = new URLSearchParams({
            book_number: String(args.book_number),
            chapter: String(args.chapter),
            verse: String(args.verse),
        });
        return apiFetch(`/cross-references?${params}`, []);
    },
    getVerseText: async (args) => {
        const { bible_versions, book_number, chapter, verse } = args;
        const params = new URLSearchParams();
        (bible_versions as string[]).forEach((v) => params.append('versions[]', v));
        params.set('book_number', String(book_number));
        params.set('chapter', String(chapter));
        params.set('verse', String(verse));
        return apiFetch(`/bible/verse-text?${params}`, []);
    },

    // ---------- Games (Electron-only — the /games route redirects web users) ----------
    gameGetLives: async () => 7,
    gameLoseLife: async () => 7,
    gameNextRecoveryAt: async () => null,
    gameRefillLives: async () => { /* no-op */ },
    gameResetProgress: async () => { /* no-op */ },
    qaGetGroups: async () => [],
    qaGetQuestionsForGroup: async () => [],
    qaGetAllGroupProgress: async () => [],
    qaSaveGroupProgress: async () => ({ newlyPassed: false }),
    tfGetGroups: async () => [],
    tfGetStatementsForGroup: async () => [],
    tfGetAllGroupProgress: async () => [],
    tfSaveGroupProgress: async () => ({ newlyPassed: false }),
    fpGetLevels: async () => [],
    fpGetSolvedLevelIds: async () => [],
    fpMarkLevelSolved: async () => { /* no-op */ },
    fpGetImagesBasePath: async () => '',

    // ---------- Encouragement reminders (desktop-only; no-op on web) ----------
    getReminderEnabled: async () => false,
    setReminderEnabled: async (value: boolean) => { warnOnce('setReminderEnabled'); return value; },
    getReminderAutoStart: async () => false,
    setReminderAutoStart: async (value: boolean) => { warnOnce('setReminderAutoStart'); return value; },
    reminderRecordActivity: async () => { /* no-op on web — no tray/scheduler */ },
};

export function installWebBridge() {
    if (window.isElectron) return;
    if (window.browserWindow) return;
    window.browserWindow = stub;
}
