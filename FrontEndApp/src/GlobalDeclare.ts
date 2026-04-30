import { MessageApiInjection } from 'naive-ui/es/message/src/MessageProvider';
import { SAVED_CLIP_NOTE_TYPE, searchBibleType } from './GlobalTypes';
import { DialogApiInjection } from 'naive-ui/es/dialog/src/DialogProvider';

declare global {
    interface Window {
        syncDataOnline: any;
        searchTheBibleTimeOut: any;
        isElectron: Boolean;
        message: MessageApiInjection;
        takingNoteTimeOut: any;
        $message: MessageApiInjection;
        $dialog: DialogApiInjection;
        browserWindow: {
            versions: () => Promise<{
                chrome: string | number;
                node: string | number;
                electron: string | number;
                version: string | number;
                name: string;
            }>;
            isWindowBrowserMaximized: () => Promise<boolean>;
            closeWindow: () => Promise<void>;
            maximizeWindow: () => Promise<void>;
            minimizeWindow: () => Promise<void>;
            getAppScale: () => Promise<number>;
            setAppScale: (scale: number) => Promise<number>;
            getAvailableBibles: () => Promise<Array<any>>;
            deleteBible: (fileName: string) => Promise<{ success: boolean; error?: string }>;
            getVerses: (args: string) => Promise<Array<any>>;
            getVersesCount: (args: string) => Promise<number>;
            getChapterHighlights: (args: string) => Promise<Array<any>>;
            getHighlights: (args: string) => Promise<Array<any>>;
            searchBible: (args: string) => Promise<searchBibleType>;
            /**
             * Downloads Modules
             */
            downloadModule: (args: {
                url?: string;
                urls?: Array<string>;
                percentage: Function;
                done: () => void;
                cancel: () => void;
            }, moduleData?: { title: string; description: string; is_zipped: boolean; file_name: string; module_type?: string }) => void;

            /**
             * Save A Bookmark
             */
            saveBookMark: (args: string) => Promise<any>;
            /**
             * Get Bookmarks
             */
            getBookMarks: () => Promise<{
                [key: string]: {
                    book_number: number;
                    chapter: number;
                    verse: number;
                };
            }>;
            /**
             * Delete The Bookmark
             */
            deleteBookmark: (args: string) => Promise<any>;
            /**
             * Save a Highlight
             */
            saveHighlight: (args: string) => Promise<any>;
            deleteHighlight: (args: {
                key: string;
            }) => Promise<any>;

            /**
             * Get ClipNotes
             */
            getClipNotes: (args: string) => Promise<any>;

            /**
             * Get Chapter Clip Notes
             */
            getChapterClipNotes: (args: string) => Promise<SAVED_CLIP_NOTE_TYPE>;

            /**
             * get Clip Notes
             */
            storeClipNote: (args: string) => Promise<any>;

            /**
             * Reset Prayer List Items
             */
            resetPrayerListItems: (args: string) => Promise<any>;

            /**
             * Reorder Prayer List Items within a status group
             */
            reorderPrayerListItems: (args: string) => Promise<any>;

            /**
             * Delete Prayer List Item
             */
            deletePrayerListItem: (key: string | number) => Promise<any>;

            /**
             * Delete Chapter Notes
             */
            deleteChapterClipNotes: Function;

            /**
             * Get Prayer List
             */
            getPrayerLists: () => Promise<
                Array<{
                    content: string;
                    created_at: any;
                    group: any;
                    key: string;
                    id: number;
                    status: string;
                    title: any;
                    updated_at: any;
                }>
            >;

            /**
             * Save Prayer List Item
             */
            savePrayerItem: (args: string) => Promise<any>;

            updateDownloadProgress: (progress: { percentage: Function; done: Function }) => void;

            openDonateWindow: () => void;

            // Notes
            getNotes: () => Promise<Array<{
                note_id: string;
                title: string;
                content: string;
                created_at: null | number | string;
                updated_at: number | string | null;
            }>>;
            upsertNote: (args: { note_id: string; title: string; content: string }) => Promise<any>;
            deleteNote: (args: { note_id: string }) => Promise<any>;

            // Dictionary
            searchDictionary: (search: string) => Promise<any>;
            getDefinitions: (word: string) => Promise<any>;

            // Piper TTS
            piperStatus: () => Promise<{ binaryReady: boolean; modelReady: boolean; modelName: string }>;
            piperInstall: () => Promise<{ success: boolean; modelName?: string; error?: string }>;
            piperUninstall: () => Promise<{ success: boolean; error?: string }>;
            piperSpeak: (text: string, modelId?: string) => Promise<{ success: boolean; wav?: string; error?: string }>;
            piperVoices: () => Promise<Array<{ id: string; name: string; language: string; gender: string; quality: string; sizeMB: number; onnxUrl: string; configUrl: string; isDownloaded: boolean }>>;
            piperInstallModel: (voiceId: string) => Promise<{ success: boolean; error?: string }>;
            piperDeleteModel: (voiceId: string) => Promise<{ success: boolean; error?: string }>;
            piperOnInstallProgress: (cb: (data: { step: string; percent: number }) => void) => void;
            piperOnModelProgress: (cb: (data: { voiceId: string; percent: number }) => void) => void;

            // Updates
            getUpdateConfig: () => Promise<{
                provider: 'electron-updater' | 'microsoft-store' | 'unavailable';
                canCheckForUpdates: boolean;
                message: string;
            }>;
            checkForUpdates: () => Promise<{
                success: boolean;
                updateAvailable?: boolean;
                error?: string;
                provider?: 'electron-updater' | 'microsoft-store' | 'unavailable';
                message?: string;
            }>;
            installUpdate: () => Promise<void>;
            downloadUpdate: () => Promise<void>;
            openStoreUpdates: () => Promise<{ success: boolean; error?: string }>;
            onWindowMaximized: (cb: (isMaximized: boolean) => void) => void;
            onUpdateAvailable: (cb: (version: string) => void) => void;
            onUpdateProgress: (cb: (percent: number) => void) => void;
            onUpdateDownloaded: (cb: () => void) => void;

            // Bible Import
            importBibleSelectFile: (source: string) => Promise<{ canceled: boolean; filePath?: string }>;
            importBibleValidate: (args: { filePath: string; source: string }) => Promise<{ valid: boolean; error?: string; verseCount?: number; warning?: string }>;
            importBibleCheckDuplicate: (title: string) => Promise<{ exists: boolean }>;
            importBible: (args: { filePath: string; title: string; description: string; source: string }) => Promise<{ success: boolean; error?: string; verseCount?: number; fileName?: string }>;

            // Sync
            logSyncChange: (entry: any) => Promise<any>;
            getUnsyncedChanges: () => Promise<any[]>;
            markAsSynced: (ids: number[]) => Promise<any>;
            getLastSyncTimestamp: () => Promise<string>;
            updateLastSyncTimestamp: (timestamp: string) => Promise<any>;
            getSyncSetting: (key: string) => Promise<any>;
            setSyncSetting: (key: string, value: any) => Promise<any>;
            applyPullData: (data: {
                sync_logs?: any[];
                bookmarks?: any[];
                highlights?: any[];
                clip_notes?: any[];
                prayer_lists?: any[];
                notes?: any[];
                settings?: any;
            }) => Promise<{ success: boolean; error?: string }>;
            onSyncBeforeQuit: (cb: () => void) => void;
            notifySyncBeforeQuitDone: () => void;

            // Export
            exportToPdf: (args: { html: string; filename: string }) => Promise<any>;
            exportToDocx: (args: { html: string; filename: string }) => Promise<any>;

            // Shell
            openExternal: (url: string) => Promise<void>;

            // Cross References
            getCrossReferences: (args: {
                book_number: number;
                chapter: number;
                verse: number;
            }) => Promise<Array<{
                to_book: number;
                to_chapter: number;
                to_verse_start: number;
                to_verse_end: number;
                votes: number;
            }>>;
            getVerseText: (args: {
                bible_versions: string[];
                book_number: number;
                chapter: number;
                verse: number;
            }) => Promise<Array<{ version: string; text: string }>>;
        };
    }
}
export { };
