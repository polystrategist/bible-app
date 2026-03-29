import { ipcMain, BrowserWindow, app } from 'electron';
import { isDev, isNightly } from '../config';
import path from 'path';
import fs from 'fs';
import { getBibleVersionDb } from '../Modules/Bible/Common/BibleVersionCache';

export const CompareVerseIpcEvents = () => {
    ipcMain.handle(
        'compareVerse:open',
        async (
            _event,
            args: { book_number: number; chapter: number; verse: number; book_name: string }
        ) => {
            let iconPath = path.join(__dirname, 'assets', 'icon.ico');
            if (isDev || isNightly) iconPath = path.join('assets', 'icon.ico');

            const win = new BrowserWindow({
                width: 520,
                height: 680,
                minWidth: 350,
                minHeight: 420,
                frame: false,
                resizable: true,
                icon: iconPath,
                webPreferences: {
                    preload: path.join(__dirname, '../preload.js'),
                    devTools: isDev || isNightly,
                },
                show: false,
            });

            const query = [
                `book=${args.book_number}`,
                `chapter=${args.chapter}`,
                `verse=${args.verse}`,
                `bookName=${encodeURIComponent(args.book_name)}`,
            ].join('&');

            const url = isDev
                ? `http://localhost:3000/#/compare-verse?${query}`
                : `file://${path.join(__dirname, './index.html')}#/compare-verse?${query}`;

            await win.loadURL(url);
            win.show();
        }
    );

    ipcMain.handle(
        'compareVerse:getVerse',
        async (
            _event,
            args: { book_number: number; chapter: number; verse: number }
        ) => {
            const dataPath = app.getPath('userData');
            const modulesPath = dataPath + `\\modules\\bible\\`;

            let availableVersions: string[] = [];
            try {
                availableVersions = fs.readdirSync(modulesPath);
            } catch {
                return [];
            }

            const results: { version: string; text: string }[] = [];

            for (const fileName of availableVersions) {
                try {
                    const db = getBibleVersionDb(fileName);
                    const rows = await db
                        .select()
                        .from('verses')
                        .where('book_number', args.book_number)
                        .where('chapter', args.chapter)
                        .where('verse', args.verse);

                    if (rows.length > 0) {
                        results.push({
                            version: fileName.replace(/\.SQLite3$/i, '').replace(/\.db$/i, ''),
                            text: rows[0].text,
                        });
                    }
                } catch {
                    // skip broken/unavailable versions
                }
            }

            return results;
        }
    );

    ipcMain.handle('closeCurrentWindow', (event) => {
        BrowserWindow.fromWebContents(event.sender)?.close();
    });
};
