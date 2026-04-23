import { ipcMain } from 'electron';
import Log from 'electron-log';
import { CrossReferencesDB } from '../../DataBase/DataBase';
import { getBibleVersionDb } from '../../Modules/Bible/Common/BibleVersionCache';

export default () => {
    ipcMain.handle(
        'getCrossReferences',
        async (_event, args: { book_number: number; chapter: number; verse: number }) => {
            return CrossReferencesDB('cross_references')
                .where({
                    from_book: args.book_number,
                    from_chapter: args.chapter,
                    from_verse: args.verse,
                })
                .orderBy('votes', 'desc')
                .select('to_book', 'to_chapter', 'to_verse_start', 'to_verse_end', 'votes');
        }
    );

    ipcMain.handle(
        'getVerseText',
        async (
            _event,
            args: { bible_versions: string[]; book_number: number; chapter: number; verse: number }
        ) => {
            const results: { version: string; text: string }[] = [];
            Log.info('getVerseText args:', JSON.stringify(args));
            for (const version of args.bible_versions) {
                try {
                    const db = getBibleVersionDb(version);
                    const row = await db('verses')
                        .where('book_number', args.book_number)
                        .where('chapter', args.chapter)
                        .where('verse', args.verse)
                        .first();
                    if (row) results.push({ version, text: row.text });
                } catch (e) {
                    Log.error('getVerseText error for version', version, e);
                }
            }
            Log.info('getVerseText results count:', results.length);
            return results;
        }
    );
};
