import { BrowserWindow } from "electron";
import { ipcVersionEvents } from "./Versions/Versions";
import { windowBrowserEvents } from "./WindowEvents/BrowserWindowEvents";

export default (BrowserWindow: BrowserWindow) => {
    // Version Events
    ipcVersionEvents();

    // browser window events
    windowBrowserEvents(BrowserWindow);
};
