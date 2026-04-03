import { BrowserWindow, dialog, ipcMain } from 'electron';
import * as fs from 'fs';
import * as path from 'path';

export default (mainWindow: BrowserWindow) => {
    ipcMain.handle(
        'exportToPdf',
        async (
            event,
            args: { html: string; filename: string }
        ) => {
            try {
                const result = await dialog.showSaveDialog(mainWindow, {
                    defaultPath: args.filename,
                    filters: [{ name: 'PDF', extensions: ['pdf'] }],
                });

                if (result.canceled || !result.filePath) return { success: false };

                // Create a hidden window to render the HTML and print to PDF
                const printWin = new BrowserWindow({
                    show: false,
                    width: 800,
                    height: 600,
                    webPreferences: { offscreen: true },
                });

                await printWin.loadURL(
                    `data:text/html;charset=utf-8,${encodeURIComponent(args.html)}`
                );

                const pdfBuffer = await printWin.webContents.printToPDF({
                    printBackground: true,
                    margins: { top: 0.5, bottom: 0.5, left: 0.5, right: 0.5 },
                });

                fs.writeFileSync(result.filePath, pdfBuffer);
                printWin.close();

                return { success: true, filePath: result.filePath };
            } catch (e) {
                console.error('PDF export error:', e);
                return { success: false, error: String(e) };
            }
        }
    );

    ipcMain.handle(
        'exportToDocx',
        async (
            event,
            args: { html: string; filename: string }
        ) => {
            try {
                const result = await dialog.showSaveDialog(mainWindow, {
                    defaultPath: args.filename,
                    filters: [{ name: 'Word Document', extensions: ['doc'] }],
                });

                if (result.canceled || !result.filePath) return { success: false };

                // Word-compatible HTML with proper encoding
                const wordHtml = `
                    <html xmlns:o="urn:schemas-microsoft-com:office:office"
                          xmlns:w="urn:schemas-microsoft-com:office:word"
                          xmlns="http://www.w3.org/TR/REC-html40">
                    <head><meta charset="utf-8"><title>Export</title>
                    <style>
                        body { font-family: Georgia, 'Times New Roman', serif; font-size: 12pt; color: #222; max-width: 600pt; margin: 0 auto; }
                        h1 { text-align: center; font-size: 18pt; margin-bottom: 12pt; }
                        p { margin: 4pt 0; line-height: 1.6; }
                    </style>
                    </head>
                    <body>${args.html}</body></html>`;

                fs.writeFileSync(result.filePath, wordHtml, 'utf-8');

                return { success: true, filePath: result.filePath };
            } catch (e) {
                console.error('DOCX export error:', e);
                return { success: false, error: String(e) };
            }
        }
    );
};
