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
            appReady: () => void;
            setSplashTheme: (payload: { bg: string; text: string; accent: string }) => Promise<void>;
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
            /** Prayer-streak days (YYYY-MM-DD per row, with total prayer seconds). */
            getPrayerDays: () => Promise<Array<{ day: string; duration?: number; created_at?: string; updated_at?: string }>>;
            /** Mark today as prayed and add `durationSeconds` to today's total; resolves to the day key. */
            markPrayedToday: (durationSeconds?: number) => Promise<string | null>;
            /** Devotion-streak days (YYYY-MM-DD per row). */
            getDevotionDays: () => Promise<Array<{ day: string; created_at?: string; updated_at?: string }>>;
            /** Mark today as a completed devotion (idempotent); resolves to the day key. */
            markDevotionToday: () => Promise<string | null>;

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

            // Strong's lexicon
            getStrongsDefinition: (strongNumber: string) => Promise<{
                strong_number: string;
                language: string;
                lemma: string | null;
                translit: string | null;
                pronunciation: string | null;
                derivation: string | null;
                strongs_def: string | null;
                kjv_def: string | null;
            } | null>;

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
                prayer_days?: any[];
                devotion_days?: any[];
                notes?: any[];
                sermon_favorites?: any[];
                ai_conversations?: any[];
                settings?: any;
                game_lives?: any[];
                qa_group_progress?: any[];
                tf_group_progress?: any[];
            }) => Promise<{ success: boolean; error?: string }>;
            onSyncBeforeQuit: (cb: () => void) => void;
            notifySyncBeforeQuitDone: () => void;

            // Sermons offline cache + favorites
            replaceCachedSermons: (sermons: any[]) => Promise<{ success: boolean; error?: string }>;
            getCachedSermons: () => Promise<any[]>;
            getSermonFavorites: () => Promise<any[]>;
            getSermonFavoriteIds: () => Promise<number[]>;
            addSermonFavorite: (sermon: any) => Promise<{ success: boolean; error?: string }>;
            removeSermonFavorite: (sermonId: number) => Promise<{ success: boolean; error?: string }>;

            // Export
            exportToPdf: (args: { html: string; filename: string }) => Promise<any>;
            exportToDocx: (args: { html: string; filename: string }) => Promise<any>;

            // Shell
            openExternal: (url: string) => Promise<void>;

            // Clipboard
            writeClipboard: (text: string) => Promise<void>;

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

            // Devotional
            getTodayDevotional: (languageCode?: string) => Promise<{
                id: number;
                day_number: number;
                title: string;
                pause: string;
                listen: string;
                think: string;
                pray: string;
                go_action: string;
                verses: string[];
            } | null>;
            getDevotionalByDay: (day: number, languageCode?: string) => Promise<{
                id: number;
                day_number: number;
                title: string;
                pause: string;
                listen: string;
                think: string;
                pray: string;
                go_action: string;
                verses: string[];
            } | null>;

            // AI Assistant conversation history
            getAiConversations: () => Promise<Array<{
                id: string;
                title: string;
                messages: Array<{ role: string; content: string }>;
                created_at: string;
                updated_at: string;
            }>>;
            getAiConversation: (id: string) => Promise<{
                id: string;
                title: string;
                messages: Array<{ role: string; content: string }>;
                created_at: string;
                updated_at: string;
            } | null>;
            saveAiConversation: (payload: {
                id: string;
                title: string;
                messages: Array<{ role: string; content: string }>;
                created_at?: string;
            }) => Promise<{
                id: string;
                title: string;
                messages: Array<{ role: string; content: string }>;
                created_at: string;
                updated_at: string;
            } | null>;
            deleteAiConversation: (id: string) => Promise<boolean>;

            // AI insight/sermon local cache (device-local, pruned after 3 days)
            getAiInsight: (key: string) => Promise<{
                key: string;
                mode: string;
                reference: string;
                version: string | null;
                content: string;
                created_at: string;
            } | null>;
            saveAiInsight: (payload: {
                key: string;
                mode: string;
                reference: string;
                version?: string | null;
                content: string;
            }) => Promise<boolean>;
            pruneAiInsights: () => Promise<boolean>;

            // Games — lives (shared 7-life pool)
            gameGetLives: () => Promise<number>;
            gameLoseLife: () => Promise<number>;
            gameNextRecoveryAt: () => Promise<string | null>;
            gameRefillLives: () => Promise<void>;
            gameResetProgress: () => Promise<void>;

            // Games — Q&A
            qaGetGroups: () => Promise<Array<{ id: number; name: string; display_order: number; required_completed: number; passing_score: number }>>;
            qaGetQuestionsForGroup: (groupId: number) => Promise<Array<{ id: number; group_id: number; question: string; options: string[]; answer: number; proof: string; explanation: string | null }>>;
            qaGetAllGroupProgress: () => Promise<Array<{ group_id: number; is_completed: number; high_score_percentage: number; times_played: number; completed_at: string | null; updated_at: string }>>;
            qaSaveGroupProgress: (args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }) => Promise<{ newlyPassed: boolean }>;

            // Games — True/False
            tfGetGroups: () => Promise<Array<{ id: number; name: string; display_order: number; required_completed: number; passing_score: number }>>;
            tfGetStatementsForGroup: (groupId: number) => Promise<Array<{ id: number; group_id: number; statement: string; answer: number; proof: string; explanation: string | null }>>;
            tfGetAllGroupProgress: () => Promise<Array<{ group_id: number; is_completed: number; high_score_percentage: number; times_played: number; completed_at: string | null; updated_at: string }>>;
            tfSaveGroupProgress: (args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }) => Promise<{ newlyPassed: boolean }>;

            // Games — Four Pictures (device-local only)
            fpGetLevels: () => Promise<Array<{ id: number; level_order: number; word: string; image1: string; image2: string; image3: string; image4: string }>>;
            fpGetSolvedLevelIds: () => Promise<number[]>;
            fpMarkLevelSolved: (levelId: number) => Promise<void>;
            fpGetImagesBasePath: () => Promise<string>;

            // Encouragement reminders
            getReminderEnabled: () => Promise<boolean>;
            setReminderEnabled: (value: boolean) => Promise<boolean>;
            getReminderAutoStart: () => Promise<boolean>;
            setReminderAutoStart: (value: boolean) => Promise<boolean>;
            reminderRecordActivity: () => Promise<void>;
        };
    }
}
export { };
