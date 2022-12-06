import { BrowserWindow } from 'electron';
import { BookmarkEvents } from './bookmark/bookmark';
import downloading from './downloading/downloading';
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
};
