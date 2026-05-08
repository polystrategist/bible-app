import { ipcMain } from 'electron';
import { DevotionalsDB } from '../../DataBase/DataBase';

const bookNames: Record<number, string> = {
    10: 'Genesis', 20: 'Exodus', 30: 'Leviticus', 40: 'Numbers', 50: 'Deuteronomy',
    60: 'Joshua', 70: 'Judges', 80: 'Ruth', 90: '1 Samuel', 100: '2 Samuel',
    110: '1 Kings', 120: '2 Kings', 130: '1 Chronicles', 140: '2 Chronicles',
    150: 'Ezra', 160: 'Nehemiah', 170: 'Tobit', 180: 'Judith', 190: 'Esther',
    220: 'Job', 230: 'Psalms', 240: 'Proverbs', 250: 'Ecclesiastes',
    260: 'Song of Solomon', 270: 'Wisdom', 280: 'Sirach', 290: 'Isaiah',
    300: 'Jeremiah', 310: 'Lamentations', 320: 'Baruch', 330: 'Ezekiel',
    340: 'Daniel', 350: 'Hosea', 360: 'Joel', 370: 'Amos', 380: 'Obadiah',
    390: 'Jonah', 400: 'Micah', 410: 'Nahum', 420: 'Habakkuk', 430: 'Zephaniah',
    440: 'Haggai', 450: 'Zechariah', 460: 'Malachi', 462: '1 Maccabees',
    464: '2 Maccabees', 470: 'Matthew', 480: 'Mark', 490: 'Luke', 500: 'John',
    510: 'Acts', 520: 'Romans', 530: '1 Corinthians', 540: '2 Corinthians',
    550: 'Galatians', 560: 'Ephesians', 570: 'Philippians', 580: 'Colossians',
    590: '1 Thessalonians', 600: '2 Thessalonians', 610: '1 Timothy',
    620: '2 Timothy', 630: 'Titus', 640: 'Philemon', 650: 'Hebrews',
    660: 'James', 670: '1 Peter', 680: '2 Peter', 690: '1 John',
    700: '2 John', 710: '3 John', 720: 'Jude', 730: 'Revelation',
};

function currentTime(): string {
    const now = new Date();
    return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
}

function dayOfYear(): number {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 1);
    return Math.floor((now.getTime() - start.getTime()) / 86400000) + 1;
}

async function queryDevotional(dayNumber: number, isToday: boolean, languageCode: string) {
    const rows = await DevotionalsDB.raw<any[]>(
        `SELECT
            d.day_number,
            c.id          AS content_id,
            c.start_at,
            COALESCE(tl.title,     te.title)     AS title,
            COALESCE(tl.pause,     te.pause)     AS pause,
            COALESCE(tl.listen,    te.listen)    AS listen,
            COALESCE(tl.think,     te.think)     AS think,
            COALESCE(tl.pray,      te.pray)      AS pray,
            COALESCE(tl.go_action, te.go_action) AS go_action
        FROM devotional_days d
        JOIN devotional_contents c ON c.devotional_day_id = d.id
        LEFT JOIN devotional_content_translations tl
               ON tl.devotional_content_id = c.id
              AND tl.language_code = ?
        LEFT JOIN devotional_content_translations te
               ON te.devotional_content_id = c.id
              AND te.language_code = 'en'
        WHERE d.day_number = ?
        ORDER BY c.id ASC`,
        [languageCode, dayNumber]
    );

    if (!rows.length) return null;

    // For today pick the latest block whose start_at is <= current time.
    // For other days just use the first block.
    let chosen = rows[0];
    if (isToday) {
        const now = currentTime();
        for (const row of rows) {
            const startAt: string = row.start_at ?? '00:01';
            if (
                startAt.localeCompare(now) <= 0 &&
                startAt.localeCompare(chosen.start_at ?? '00:01') > 0
            ) {
                chosen = row;
            }
        }
    }

    const verseRows = await DevotionalsDB.raw<any[]>(
        `SELECT book_number, chapter, verse_start, verse_end
         FROM devotional_content_verses
         WHERE devotional_content_id = ?
         ORDER BY id ASC`,
        [chosen.content_id]
    );

    const verses: string[] = verseRows.map((v: any) => {
        const bookName = bookNames[v.book_number] ?? String(v.book_number);
        const end = v.verse_end != null ? `-${v.verse_end}` : '';
        return `${bookName}:${v.chapter}:${v.verse_start}${end}`;
    });

    return {
        id: chosen.content_id,
        day_number: chosen.day_number,
        title: chosen.title ?? '',
        pause: chosen.pause ?? '',
        listen: chosen.listen ?? '',
        think: chosen.think ?? '',
        pray: chosen.pray ?? '',
        go_action: chosen.go_action ?? '',
        verses,
    };
}

export default () => {
    ipcMain.handle('getTodayDevotional', async (_event, languageCode: string = 'en') => {
        const day = Math.min(Math.max(dayOfYear(), 1), 365);
        return queryDevotional(day, true, languageCode);
    });

    ipcMain.handle('getDevotionalByDay', async (_event, day: number, languageCode: string = 'en') => {
        return queryDevotional(day, false, languageCode);
    });
};
