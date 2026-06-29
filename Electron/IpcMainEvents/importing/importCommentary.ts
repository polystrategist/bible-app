import { ipcMain, BrowserWindow, dialog } from 'electron';
import { app } from 'electron';
import Log from 'electron-log';
import { setupPortableMode } from '../../util/portable';
import fs from 'fs';
import path from 'path';
import knex from 'knex';
import { clearCommentaryCache } from '../../Modules/Commentaries/Common/CommentaryVersionCache';

setupPortableMode();
const dataPath = app.getPath('userData');
const commentariesPath = path.join(dataPath, 'modules', 'commentaries');

// Columns a MyBible-style `commentaries` table must have for the reader to
// query verse ranges and render markers. Validation rejects any file missing
// the table or one of these columns.
const REQUIRED_COLUMNS = [
    'book_number',
    'chapter_number_from',
    'verse_number_from',
    'chapter_number_to',
    'verse_number_to',
    'marker',
    'text',
];

type ValidationResult = {
    valid: boolean;
    error?: string;
    entryCount?: number;
};

/** Strip characters that aren't valid in a file name. */
function sanitizeName(name: string): string {
    return name.replace(/[\\/:*?"<>|]/g, '').trim();
}

/** Destination commentary file name for a user-provided display name. */
function commentaryFileName(name: string): string {
    return `${sanitizeName(name)}.commentaries.SQLite3`;
}

/**
 * Validate a commentary SQLite file: it must contain a `commentaries` table
 * with the required MyBible columns and at least one entry.
 */
async function validateCommentarySqlite(filePath: string): Promise<ValidationResult> {
    const db = knex({
        client: 'sqlite3',
        connection: { filename: filePath },
        useNullAsDefault: true,
    });
    try {
        const hasTable = await db.schema.hasTable('commentaries');
        if (!hasTable) {
            return {
                valid: false,
                error: 'No "commentaries" table found. This does not appear to be a valid commentary module.',
            };
        }

        const cols = (await db('commentaries').columnInfo()) as Record<string, unknown>;
        const missing = REQUIRED_COLUMNS.filter((col) => !cols[col]);
        if (missing.length > 0) {
            return {
                valid: false,
                error: `Missing required column(s) in the commentaries table: ${missing.join(', ')}.`,
            };
        }

        const countRow = (await db('commentaries').count('* as cnt').first()) as { cnt: number };
        const entryCount = Number(countRow?.cnt ?? 0);
        if (entryCount === 0) {
            return { valid: false, error: 'The commentaries table is empty — nothing to import.' };
        }

        return { valid: true, entryCount };
    } catch (err: any) {
        return { valid: false, error: `Failed to open SQLite file: ${err.message}` };
    } finally {
        await db.destroy();
    }
}

export default (mainWindow: BrowserWindow) => {
    // Open a file dialog to pick a commentary SQLite file.
    ipcMain.handle('import-commentary:select-file', async () => {
        const result = await dialog.showOpenDialog(mainWindow, {
            title: 'Select commentary SQLite file',
            filters: [
                { name: 'Commentary module', extensions: ['SQLite3', 'sqlite3', 'db'] },
                { name: 'All Files', extensions: ['*'] },
            ],
            properties: ['openFile'],
        });

        if (result.canceled || result.filePaths.length === 0) {
            return { canceled: true };
        }
        return { canceled: false, filePath: result.filePaths[0] };
    });

    // Validate the selected file's table + columns.
    ipcMain.handle('import-commentary:validate', async (_event, args: { filePath: string }) => {
        try {
            return await validateCommentarySqlite(args.filePath);
        } catch (err: any) {
            return { valid: false, error: `Failed to read file: ${err.message}` };
        }
    });

    // Check whether a commentary with the chosen name is already installed.
    ipcMain.handle('import-commentary:check-duplicate', async (_event, name: string) => {
        const fullPath = path.join(commentariesPath, commentaryFileName(name));
        return { exists: fs.existsSync(fullPath) };
    });

    // Copy the validated commentary file into the commentaries folder under the
    // user-provided name; the Commentaries tab then lists it independently of
    // whichever translation is open.
    ipcMain.handle(
        'import-commentary:import',
        async (_event, args: { filePath: string; name: string; overwrite?: boolean }) => {
            const cleanName = sanitizeName(args.name);
            if (!cleanName) {
                return { success: false, error: 'Please enter a valid commentary name.' };
            }

            const fileName = commentaryFileName(cleanName);
            const fullPath = path.join(commentariesPath, fileName);
            try {
                if (fs.existsSync(fullPath) && !args.overwrite) {
                    return {
                        success: false,
                        error: `A commentary named "${cleanName}" is already installed.`,
                    };
                }

                // Re-validate before committing the copy.
                const validation = await validateCommentarySqlite(args.filePath);
                if (!validation.valid) {
                    return { success: false, error: validation.error };
                }

                fs.mkdirSync(commentariesPath, { recursive: true });
                fs.copyFileSync(args.filePath, fullPath);

                // Drop cached connections so the freshly imported file is picked up.
                clearCommentaryCache();

                Log.info(`Imported commentary module: ${fileName} (${validation.entryCount} entries)`);
                return { success: true, entryCount: validation.entryCount, fileName };
            } catch (err: any) {
                Log.error('Import commentary error:', err);
                if (fs.existsSync(fullPath)) {
                    try {
                        fs.unlinkSync(fullPath);
                    } catch {
                        /* best-effort cleanup */
                    }
                }
                return { success: false, error: `Import failed: ${err.message}` };
            }
        },
    );
};
