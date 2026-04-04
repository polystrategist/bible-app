import { BrowserWindow } from 'electron';
import { BookmarkEvents } from './bookmark/bookmark';
import ClipNotes from './ClipNotes/ClipNotes';
import downloading from './downloading/downloading';
import highlighting from './highlights/highlighting';
import PrayerList from './PrayerList/PrayerList';
import { ipcVersionEvents } from './Versions/Versions';
import { windowBrowserEvents } from './WindowEvents/BrowserWindowEvents';
import { WindowOpenerIpcEvents } from '../Windows/WindowOpenerIpcEvents';
import { CompareVerseIpcEvents } from '../Windows/CompareVerseWindow';
import notesEvents from './notes/notesEvents';
import dictionaries from './dictionaries/dictionaries';
import { SyncHandlers } from './Sync/SyncHandlers';
import { PiperTTSHandlers } from './Piper/PiperTTS';
import Commentaries from '../Modules/Commentaries/Commentaries';
import DailyDevotional from './DailyDevotional/DailyDevotional';
import importing from './importing/importing';
import exporting from './exporting/exporting';

export default (BrowserWindow: BrowserWindow) => {
    // Version Events
    ipcVersionEvents();

    // browser window events
    windowBrowserEvents(BrowserWindow);

    // download events
    downloading(BrowserWindow);

    // bookmarks events
    BookmarkEvents(BrowserWindow);

    // Highlighting
    highlighting();

    // ClipNotes
    ClipNotes();

    // Prayer List
    PrayerList();

    // window opener events
    WindowOpenerIpcEvents(BrowserWindow);

    // compare verse window
    CompareVerseIpcEvents();

    // notes events
    notesEvents();

    // dictionary events
    dictionaries();

    // sync handlers
    SyncHandlers(BrowserWindow);

    // piper tts handlers
    PiperTTSHandlers(BrowserWindow);

    // commentary handlers
    Commentaries();

    // daily devotional handlers
    DailyDevotional();

    // bible import handlers
    importing(BrowserWindow);

    // export handlers (PDF, DOCX)
    exporting(BrowserWindow);
};
