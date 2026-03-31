import { ipcMain } from 'electron';
import { getCommentaryDb, hasCommentaryFile } from './CommentaryVersionCache';

export type GetCommentaryArgs = {
    version: string;
    book_number: number;
    chapter: number;
    verse: number;
};

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
            text: row.text.replace(/<a\s[^>]*>/gi, '<span>').replace(/<\/a>/gi, '</span>'),
        }));
    });

    ipcMain.handle('hasCommentary', (_event, version: string) => {
        return hasCommentaryFile(version);
    });
};
