import { BrowserWindow } from 'electron';
import { BookmarkEvents } from './bookmark/bookmark';
import ClipNotes from './ClipNotes/ClipNotes';
import downloading from './downloading/downloading';
import highlighting from './highlights/highlighting';
import PrayerList from './PrayerList/PrayerList';
import { ipcVersionEvents } from './Versions/Versions';
import { windowBrowserEvents } from './WindowEvents/BrowserWindowEvents';

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
};
