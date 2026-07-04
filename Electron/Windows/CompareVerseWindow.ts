import { ipcMain, BrowserWindow, app, screen } from 'electron';
import { isDev, isBeta } from '../config';
import path from 'path';
import fs from 'fs';
import { getBibleVersionDb } from '../Modules/Bible/Common/BibleVersionCache';
import { appIconPath } from '../util/appIcon';

const COMPARE_WIN_WIDTH = 520;
const COMPARE_WIN_HEIGHT = 680;

/**
 * Position the Compare Verse window centered over the window that opened it, so
 * it appears on the same monitor as the main window. Clamped to that display's
 * work area so it never lands partially off-screen.
 */
const positionOverParent = (
    parent: BrowserWindow | null
): { x: number; y: number } | undefined => {
    if (!parent || parent.isDestroyed()) return undefined;
    const pb = parent.getBounds();
    const { workArea } = screen.getDisplayMatching(pb);

    const centeredX = Math.round(pb.x + (pb.width - COMPARE_WIN_WIDTH) / 2);
    const centeredY = Math.round(pb.y + (pb.height - COMPARE_WIN_HEIGHT) / 2);

    return {
        x: Math.max(
            workArea.x,
            Math.min(centeredX, workArea.x + workArea.width - COMPARE_WIN_WIDTH)
        ),
        y: Math.max(
            workArea.y,
            Math.min(centeredY, workArea.y + workArea.height - COMPARE_WIN_HEIGHT)
        ),
    };
};

export const CompareVerseIpcEvents = () => {
    ipcMain.handle(
        'compareVerse:open',
        async (
            event,
            args: { book_number: number; chapter: number; verse: number; book_name: string }
        ) => {
            const iconPath = appIconPath();

            const position = positionOverParent(
                BrowserWindow.fromWebContents(event.sender)
            );

            const win = new BrowserWindow({
                width: COMPARE_WIN_WIDTH,
                height: COMPARE_WIN_HEIGHT,
                x: position?.x,
                y: position?.y,
                minWidth: 350,
                minHeight: 420,
                frame: false,
                resizable: true,
                icon: iconPath,
                webPreferences: {
                    preload: path.join(__dirname, '../preload.js'),
                    devTools: isDev || isBeta,
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
                // Compiled to dist/Windows/; index.html sits at the dist root (matching
                // the `../preload.js` above), so go up one level.
                : `file://${path.join(__dirname, '..', 'index.html')}#/compare-verse?${query}`;

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
                availableVersions = fs
                    .readdirSync(modulesPath)
                    .filter((f) => /\.(SQLite3|db)$/i.test(f));
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
