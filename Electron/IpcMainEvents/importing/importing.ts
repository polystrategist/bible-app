import { ipcMain, BrowserWindow, dialog } from 'electron';
import { app } from 'electron';
import Log from 'electron-log';
import { setupPortableMode } from '../../util/portable';
import fs from 'fs';
import path from 'path';
import knex from 'knex';

setupPortableMode();
const dataPath = app.getPath('userData');
const biblePath = path.join(dataPath, 'modules', 'bible');

/**
 * Map ebible.org 3-letter book codes to MyBible book_number (10-increment system).
 */
const EBIBLE_BOOK_MAP: Record<string, number> = {
    // Old Testament
    GEN: 10, EXO: 20, LEV: 30, NUM: 40, DEU: 50,
    JOS: 60, JDG: 70, RUT: 80,
    '1SA': 90, '2SA': 100, '1KI': 110, '2KI': 120,
    '1CH': 130, '2CH': 140, EZR: 150, NEH: 160,
    // Deuterocanonical (between Nehemiah and Esther in some orderings)
    TOB: 170, JDT: 180,
    EST: 190,
    JOB: 220, PSA: 230, PRO: 240, ECC: 250, SNG: 260,
    // Deuterocanonical
    WIS: 270, SIR: 280,
    ISA: 290, JER: 300, LAM: 310,
    BAR: 320,
    EZK: 330, DAN: 340,
    HOS: 350, JOL: 360, AMO: 370, OBA: 380, JON: 390,
    MIC: 400, NAM: 410, HAB: 420, ZEP: 430, HAG: 440, ZEC: 450, MAL: 460,
    // Deuterocanonical
    '1MA': 462, '2MA': 464,
    // New Testament
    MAT: 470, MRK: 480, LUK: 490, JHN: 500, ACT: 510,
    ROM: 520, '1CO': 530, '2CO': 540, GAL: 550, EPH: 560,
    PHP: 570, COL: 580, '1TH': 590, '2TH': 600,
    '1TI': 610, '2TI': 620, TIT: 630, PHM: 640, HEB: 650,
    JAS: 660, '1PE': 670, '2PE': 680,
    '1JN': 690, '2JN': 700, '3JN': 710, JUD: 720, REV: 730,
};

/**
 * Book long names for the `books` table.
 */
const BOOK_LONG_NAMES: Record<number, string> = {
    10: 'Genesis', 20: 'Exodus', 30: 'Leviticus', 40: 'Numbers', 50: 'Deuteronomy',
    60: 'Joshua', 70: 'Judges', 80: 'Ruth',
    90: '1 Samuel', 100: '2 Samuel', 110: '1 Kings', 120: '2 Kings',
    130: '1 Chronicles', 140: '2 Chronicles', 150: 'Ezra', 160: 'Nehemiah',
    170: 'Tobit', 180: 'Judith',
    190: 'Esther',
    220: 'Job', 230: 'Psalms', 240: 'Proverbs', 250: 'Ecclesiastes', 260: 'Song of Solomon',
    270: 'Wisdom', 280: 'Sirach',
    290: 'Isaiah', 300: 'Jeremiah', 310: 'Lamentations',
    320: 'Baruch',
    330: 'Ezekiel', 340: 'Daniel',
    350: 'Hosea', 360: 'Joel', 370: 'Amos', 380: 'Obadiah', 390: 'Jonah',
    400: 'Micah', 410: 'Nahum', 420: 'Habakkuk', 430: 'Zephaniah', 440: 'Haggai', 450: 'Zechariah', 460: 'Malachi',
    462: '1 Maccabees', 464: '2 Maccabees',
    470: 'Matthew', 480: 'Mark', 490: 'Luke', 500: 'John', 510: 'Acts',
    520: 'Romans', 530: '1 Corinthians', 540: '2 Corinthians', 550: 'Galatians', 560: 'Ephesians',
    570: 'Philippians', 580: 'Colossians', 590: '1 Thessalonians', 600: '2 Thessalonians',
    610: '1 Timothy', 620: '2 Timothy', 630: 'Titus', 640: 'Philemon', 650: 'Hebrews',
    660: 'James', 670: '1 Peter', 680: '2 Peter',
    690: '1 John', 700: '2 John', 710: '3 John', 720: 'Jude', 730: 'Revelation',
};

type ParsedVerse = {
    book_number: number;
    chapter: number;
    verse: number;
    text: string;
};

/**
 * Validate that the SQL content looks like an ebible.org VPL SQL dump.
 * Returns null if valid, or an error message string.
 */
function validateEbibleSql(content: string): string | null {
    const lines = content.split('\n').filter(l => l.trim().startsWith('INSERT INTO'));
    if (lines.length === 0) {
        return 'No INSERT statements found. This does not appear to be a valid ebible.org SQL file.';
    }

    // Check first few lines match the expected pattern
    const pattern = /INSERT INTO \S+ VALUES \("([^"]+)","([^"]+)","([A-Z0-9]+)","(\d+)","(\d+)","(\d+)","(.*)"\s*\);/;
    const sampleLines = lines.slice(0, 5);
    for (const line of sampleLines) {
        if (!pattern.test(line.trim())) {
            return 'SQL format does not match ebible.org VPL format. Expected: INSERT INTO <table> VALUES ("id","sort","BOOK","chapter","verse","verse","text");';
        }
    }

    // Check that we can map at least one book code
    const firstMatch = sampleLines[0].trim().match(pattern);
    if (firstMatch) {
        const bookCode = firstMatch[3];
        if (!EBIBLE_BOOK_MAP[bookCode]) {
            return `Unrecognized book code "${bookCode}". This may not be a standard ebible.org SQL file.`;
        }
    }

    return null;
}

/**
 * Parse all INSERT statements from ebible.org SQL content into verse objects.
 */
function parseEbibleSql(content: string): ParsedVerse[] {
    const verses: ParsedVerse[] = [];
    const pattern = /INSERT INTO \S+ VALUES \("([^"]+)","([^"]+)","([A-Z0-9]+)","(\d+)","(\d+)","(\d+)","(.*)"\s*\);/;

    const lines = content.split('\n');
    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed.startsWith('INSERT INTO')) continue;

        const match = trimmed.match(pattern);
        if (!match) continue;

        const bookCode = match[3];
        const chapter = parseInt(match[4], 10);
        const verse = parseInt(match[5], 10);
        let text = match[7];

        const bookNumber = EBIBLE_BOOK_MAP[bookCode];
        if (!bookNumber) continue;

        // Clean up pilcrow paragraph markers — they are not needed in our format
        text = text.replace(/¶\s*/g, '').trim();

        verses.push({ book_number: bookNumber, chapter, verse, text });
    }

    return verses;
}

/**
 * Create a SQLite3 database file in MyBible format from parsed verses.
 */
async function createBibleModule(fileName: string, verses: ParsedVerse[]): Promise<void> {
    const dbPath = path.join(biblePath, fileName);

    // Ensure bible directory exists
    if (!fs.existsSync(biblePath)) {
        fs.mkdirSync(biblePath, { recursive: true });
    }

    const db = knex({
        client: 'sqlite3',
        connection: { filename: dbPath },
        useNullAsDefault: true,
    });

    try {
        // Create verses table
        await db.schema.createTable('verses', (table) => {
            table.integer('book_number');
            table.integer('chapter');
            table.integer('verse');
            table.text('text');
        });

        // Create books table
        await db.schema.createTable('books', (table) => {
            table.integer('book_number').primary();
            table.text('long_name');
        });

        // Collect unique book numbers from the verses
        const bookNumbers = [...new Set(verses.map(v => v.book_number))].sort((a, b) => a - b);

        // Insert books
        const bookRows = bookNumbers.map(bn => ({
            book_number: bn,
            long_name: BOOK_LONG_NAMES[bn] || `Book ${bn}`,
        }));
        await db.batchInsert('books', bookRows, 100);

        // Insert verses in batches
        await db.batchInsert('verses', verses, 500);

        // Create index for faster queries
        await db.schema.raw('CREATE INDEX IF NOT EXISTS idx_verses_book_chapter ON verses (book_number, chapter)');
    } finally {
        await db.destroy();
    }
}

export default (mainWindow: BrowserWindow) => {
    // Open file dialog to pick a SQL file
    ipcMain.handle('import-bible:select-file', async () => {
        const result = await dialog.showOpenDialog(mainWindow, {
            title: 'Select ebible.org SQL file',
            filters: [
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

    // Validate the selected SQL file
    ipcMain.handle('import-bible:validate', async (_event, filePath: string) => {
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            const error = validateEbibleSql(content);
            if (error) {
                return { valid: false, error };
            }

            // Count verses for preview
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

    // Import the SQL file into a new SQLite module
    ipcMain.handle('import-bible:import', async (_event, args: { filePath: string; title: string; description: string }) => {
        try {
            const fileName = `${args.title}.SQLite3`;
            const fullPath = path.join(biblePath, fileName);

            // Final duplicate check
            if (fs.existsSync(fullPath)) {
                return { success: false, error: `A Bible module named "${args.title}" already exists.` };
            }

            const content = fs.readFileSync(args.filePath, 'utf-8');

            // Validate
            const validationError = validateEbibleSql(content);
            if (validationError) {
                return { success: false, error: validationError };
            }

            // Parse
            const verses = parseEbibleSql(content);
            if (verses.length === 0) {
                return { success: false, error: 'No valid verses could be parsed from the file.' };
            }

            // Create module
            await createBibleModule(fileName, verses);

            Log.info(`Imported Bible module: ${fileName} (${verses.length} verses)`);
            return { success: true, verseCount: verses.length, fileName };
        } catch (err: any) {
            Log.error('Import Bible error:', err);
            // Clean up partial file on failure
            const fileName = `${args.title}.SQLite3`;
            const fullPath = path.join(biblePath, fileName);
            if (fs.existsSync(fullPath)) {
                fs.unlinkSync(fullPath);
            }
            return { success: false, error: `Import failed: ${err.message}` };
        }
    });
};
