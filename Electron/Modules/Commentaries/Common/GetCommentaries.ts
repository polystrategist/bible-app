import { ipcMain } from 'electron';
import { getCommentaryDb, getCommentaryDbByFile, hasCommentaryFile } from './CommentaryVersionCache';

export type GetCommentaryArgs = {
    version: string;
    book_number: number;
    chapter: number;
    verse: number;
};

export type GetChapterCommentaryArgs = {
    version: string;
    book_number: number;
    chapter: number;
};

export type GetFileCommentaryArgs = {
    file: string;
    book_number: number;
    chapter: number;
};

// Normalize the MyBible markup in a commentary entry:
//  - Deep-link refs `<a href="B:500 3:11">3:11</a>` become click-navigable
//    `<span class="commentary-ref" data-book data-chapter data-verse>` that the
//    renderer wires to verse navigation.
//  - Any other <a> tag is flattened to a plain <span> (no broken links).
function sanitizeCommentaryText(text: string): string {
    return (text ?? '')
        .replace(
            /<a\s+[^>]*href=['"]B:(\d+)\s+(\d+):(\d+)[^'"]*['"][^>]*>([\s\S]*?)<\/a>/gi,
            (_m, book, chapter, verse, label) =>
                `<span class="commentary-ref" data-book="${book}" data-chapter="${chapter}" data-verse="${verse}">${label}</span>`,
        )
        .replace(/<a\s[^>]*>/gi, '<span>')
        .replace(/<\/a>/gi, '</span>');
}

// Range-aware fetch of every entry in a chapter from an already-opened
// commentary DB. `*_to` of 0/NULL marks a single-verse entry.
async function fetchChapterEntries(db: any, book_number: number, chapter: number) {
    const rows = await db
        .select(
            'marker',
            'text',
            'chapter_number_from',
            'verse_number_from',
            'chapter_number_to',
            'verse_number_to',
        )
        .from('commentaries')
        .where('book_number', book_number)
        .where('chapter_number_from', chapter)
        .orderBy('verse_number_from', 'asc')
        .orderBy('marker', 'asc');

    return rows.map((row: any) => ({
        marker: row.marker ?? '',
        text: sanitizeCommentaryText(row.text),
        chapter_number_from: Number(row.chapter_number_from) || 0,
        verse_number_from: Number(row.verse_number_from) || 0,
        chapter_number_to: Number(row.chapter_number_to) || 0,
        verse_number_to: Number(row.verse_number_to) || 0,
    }));
}

export default () => {
    ipcMain.handle('getCommentaryForVerse', async (_event, args: GetCommentaryArgs) => {
        const db = getCommentaryDb(args.version);
        if (!db) return [];

        const rows = await db
            .select('marker', 'text')
            .from('commentaries')
            .where('book_number', args.book_number)
            .where('chapter_number_from', args.chapter)
            .where('verse_number_from', args.verse);

        // Replace deep-link <a> tags (e.g. href="B:500 6:39") with plain spans
        return rows.map((row: { marker: string; text: string }) => ({
            marker: row.marker,
            text: sanitizeCommentaryText(row.text),
        }));
    });

    // Whole-chapter fetch matched to a Bible version (used where commentary
    // should follow the open translation, e.g. version-specific footnotes).
    ipcMain.handle('getCommentariesForChapter', async (_event, args: GetChapterCommentaryArgs) => {
        const db = getCommentaryDb(args.version);
        if (!db) return [];
        return fetchChapterEntries(db, args.book_number, args.chapter);
    });

    // Whole-chapter fetch from a specific commentary file, independent of the
    // open translation. Powers the Commentaries tab's user-selected modules.
    ipcMain.handle('getCommentariesByFile', async (_event, args: GetFileCommentaryArgs) => {
        const db = getCommentaryDbByFile(args.file);
        if (!db) return [];
        return fetchChapterEntries(db, args.book_number, args.chapter);
    });

    ipcMain.handle('hasCommentary', (_event, version: string) => {
        return hasCommentaryFile(version);
    });
};
