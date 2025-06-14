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
            getAvailableBibles: () => Promise<Array<any>>;
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
                done: () => void;
            }) => void;

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
                study_space_id: number | string;
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

            /**
             * Space Studies Events
             */
            getSpaceStudyList: (search: string | null | undefined) => Promise<any>;
            storeSpaceStudy: (args: string) => Promise<{
                data: null | {
                    id: number;
                    title: string;
                    is_selected: boolean | number;
                    description: string;
                    created_at: string;
                    updated_at: string;
                };
                error: null | { errno?: number; code?: string; message: string };
            }>;
            deleteSpaceStudy: (
                id: number
            ) => Promise<{ data: any; error: { message: string;[key: string]: any } }>;
            selectStudySpace: (
                id: number | string
            ) => Promise<{ data: any; error: { message: string;[key: string]: any } }>;
            getSelectedSpaceStudy: () => Promise<{
                data: null | {
                    id: number;
                    title: string;
                    is_selected: boolean | number;
                    description: string;
                    created_at: string;
                    updated_at: string;
                };
                error: null | { errno?: number; code?: string; message: string };
            }>;

            // Note
            getNote: (space_study_id: number) => Promise<{
                content: string;
                created_at: null | number | string;
                id: number;
                study_space_id: number;
                updated_at: number | string | null;
            }>;
            saveNote: (args: { space_study_id: number | string; note: string }) => Promise<any>;

            // Dictionary
            searchDictionary: (search: string) => Promise<any>;
            getDefinitions: (word: string) => Promise<any>;

        };
    }
}
export { };
