import { ipcMain, BrowserWindow, dialog } from 'electron';
import { app } from 'electron';
import Log from 'electron-log';
import { setupPortableMode } from '../../util/portable';
import fs from 'fs';
import path from 'path';
import knex from 'knex';
import {
    SUPPORTED_BOOK_NUMBERS,
    validateEbibleSql,
    parseEbibleSql,
    createBibleModule,
    type ParsedVerse,
} from '../../util/ebibleConverter';

setupPortableMode();
const dataPath = app.getPath('userData');
const biblePath = path.join(dataPath, 'modules', 'bible');

type ValidationResult = {
    valid: boolean;
    error?: string;
    verseCount?: number;
    warning?: string;
};

/**
 * Validate a MyBible .sqlite3 file.
 * Checks for the required `verses` table schema and that book numbers are in the supported set.
 */
async function validateMyBibleSqlite(filePath: string): Promise<ValidationResult> {
    const db = knex({
        client: 'sqlite3',
        connection: { filename: filePath },
        useNullAsDefault: true,
    });
    try {
        const hasVerses = await db.schema.hasTable('verses');
        if (!hasVerses) {
            return { valid: false, error: 'No "verses" table found. This does not appear to be a valid MyBible module.' };
        }

        const cols = await db('verses').columnInfo() as Record<string, unknown>;
        for (const col of ['book_number', 'chapter', 'verse', 'text']) {
            if (!cols[col]) {
                return { valid: false, error: `Missing required column "${col}" in the verses table.` };
            }
        }

        const bookRows: { book_number: number }[] = await db('verses').distinct('book_number').select('book_number');
        const bookNumbers = bookRows.map(r => r.book_number);
        const unsupported = bookNumbers.filter(bn => !SUPPORTED_BOOK_NUMBERS.has(bn));

        if (bookNumbers.length > 0 && unsupported.length === bookNumbers.length) {
            return {
                valid: false,
                error: `No supported book numbers found (got: ${unsupported.slice(0, 5).join(', ')}${unsupported.length > 5 ? '…' : ''}). Expected MyBible 10-increment numbering (10=Genesis, 20=Exodus, …).`,
            };
        }

        const countRow = await db('verses')
            .whereIn('book_number', [...SUPPORTED_BOOK_NUMBERS])
            .count('* as cnt')
            .first() as { cnt: number };

        const warning = unsupported.length > 0
            ? `${unsupported.length} unrecognized book number(s) will be skipped: ${unsupported.slice(0, 8).join(', ')}${unsupported.length > 8 ? '…' : ''}.`
            : undefined;

        return { valid: true, verseCount: Number(countRow.cnt), warning };
    } catch (err: any) {
        return { valid: false, error: `Failed to open SQLite file: ${err.message}` };
    } finally {
        await db.destroy();
    }
}

/**
 * Read all supported verses from a MyBible .sqlite3 source file and create a new module.
 */
async function importMyBibleSqlite(filePath: string, fileName: string): Promise<number> {
    const src = knex({
        client: 'sqlite3',
        connection: { filename: filePath },
        useNullAsDefault: true,
    });
    try {
        const rows: { book_number: number; chapter: number; verse: number; text: string }[] =
            await src('verses')
                .whereIn('book_number', [...SUPPORTED_BOOK_NUMBERS])
                .select('book_number', 'chapter', 'verse', 'text');

        const verses: ParsedVerse[] = rows.map(r => ({
            book_number: r.book_number,
            chapter: r.chapter,
            verse: r.verse,
            text: r.text ?? '',
        }));

        if (verses.length === 0) {
            throw new Error('No verses with supported book numbers were found in this file.');
        }

        const dbPath = path.join(biblePath, fileName);
        await createBibleModule(dbPath, verses);
        return verses.length;
    } finally {
        await src.destroy();
    }
}

export default (mainWindow: BrowserWindow) => {
    // Open file dialog to pick a file (format-aware)
    ipcMain.handle('import-bible:select-file', async (_event, source: string) => {
        const isMyBible = source === 'mybible-sqlite3';
        const result = await dialog.showOpenDialog(mainWindow, {
            title: isMyBible ? 'Select MyBible SQLite3 file' : 'Select ebible.org SQL file',
            filters: isMyBible
                ? [
                    { name: 'MyBible SQLite3', extensions: ['sqlite3', 'db'] },
                    { name: 'All Files', extensions: ['*'] },
                ]
                : [
                    { name: 'SQL Files', extensions: ['sql'] },
                    { name: 'All Files', extensions: ['*'] },
                ],
            properties: ['openFile'],
        });

        if (result.canceled || result.filePaths.length === 0) {
            return { canceled: true };
        }

        return { canceled: false, filePath: result.filePaths[0] };
    });

    // Validate the selected file
    ipcMain.handle('import-bible:validate', async (_event, args: { filePath: string; source: string }) => {
        try {
            if (args.source === 'mybible-sqlite3') {
                return await validateMyBibleSqlite(args.filePath);
            }

            // ebible-sql
            const content = fs.readFileSync(args.filePath, 'utf-8');
            const error = validateEbibleSql(content);
            if (error) {
                return { valid: false, error };
            }
            const lines = content.split('\n').filter(l => l.trim().startsWith('INSERT INTO'));
            return { valid: true, verseCount: lines.length };
        } catch (err: any) {
            return { valid: false, error: `Failed to read file: ${err.message}` };
        }
    });

    // Check if a bible module with the given filename already exists
    ipcMain.handle('import-bible:check-duplicate', async (_event, title: string) => {
        const fileName = `${title}.SQLite3`;
        const fullPath = path.join(biblePath, fileName);
        return { exists: fs.existsSync(fullPath) };
    });

    // Import the file into a new SQLite module
    ipcMain.handle('import-bible:import', async (_event, args: { filePath: string; title: string; description: string; source: string }) => {
        const fileName = `${args.title}.SQLite3`;
        const fullPath = path.join(biblePath, fileName);
        try {
            // Final duplicate check
            if (fs.existsSync(fullPath)) {
                return { success: false, error: `A Bible module named "${args.title}" already exists.` };
            }

            let verseCount: number;

            if (args.source === 'mybible-sqlite3') {
                verseCount = await importMyBibleSqlite(args.filePath, fileName);
            } else {
                const content = fs.readFileSync(args.filePath, 'utf-8');
                const validationError = validateEbibleSql(content);
                if (validationError) {
                    return { success: false, error: validationError };
                }
                const verses = parseEbibleSql(content);
                if (verses.length === 0) {
                    return { success: false, error: 'No valid verses could be parsed from the file.' };
                }
                await createBibleModule(fullPath, verses);
                verseCount = verses.length;
            }

            Log.info(`Imported Bible module: ${fileName} (${verseCount} verses)`);
            return { success: true, verseCount, fileName };
        } catch (err: any) {
            Log.error('Import Bible error:', err);
            if (fs.existsSync(fullPath)) {
                fs.unlinkSync(fullPath);
            }
            return { success: false, error: `Import failed: ${err.message}` };
        }
    });
};
