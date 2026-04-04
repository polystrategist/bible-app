import { StoreDB } from '../../DataBase/DataBase';
import Log from 'electron-log';

/**
 * Create indexes on frequently queried columns for better performance
 */
export async function createDatabaseIndexes() {
    try {
        // Check if indexes already exist
        const indexes = await StoreDB.raw('PRAGMA index_list(bookmarks)');
        const indexNames = indexes.map((idx: any) => idx.name);

        if (!indexNames.includes('bookmarks_key')) {
            await StoreDB.schema.alterTable('bookmarks', (table: any) => {
                table.index('key', 'bookmarks_key');
            });
            Log.info('Created index: bookmarks_key');
        }

        // Highlights indexes
        const highlightsIndexes = await StoreDB.raw('PRAGMA index_list(highlights)');
        const highlightsIndexNames = highlightsIndexes.map((idx: any) => idx.name);

        if (!highlightsIndexNames.includes('highlights_book_chapter')) {
            await StoreDB.schema.alterTable('highlights', (table: any) => {
                table.index(['book_number', 'chapter'], 'highlights_book_chapter');
            });
            Log.info('Created index: highlights_book_chapter');
        }

        // Clip notes indexes
        const clipNotesIndexes = await StoreDB.raw('PRAGMA index_list(clip_notes)');
        const clipNotesIndexNames = clipNotesIndexes.map((idx: any) => idx.name);

        if (!clipNotesIndexNames.includes('clip_notes_key')) {
            await StoreDB.schema.alterTable('clip_notes', (table: any) => {
                table.index('key', 'clip_notes_key');
            });
            Log.info('Created index: clip_notes_key');
        }

        // Prayer list indexes
        const prayerListIndexes = await StoreDB.raw('PRAGMA index_list(prayer_lists)');
        const prayerListIndexNames = prayerListIndexes.map((idx: any) => idx.name);

        if (!prayerListIndexNames.includes('prayer_lists_status')) {
            await StoreDB.schema.alterTable('prayer_lists', (table: any) => {
                table.index('status', 'prayer_lists_status');
            });
            Log.info('Created index: prayer_lists_status');
        }

        if (!prayerListIndexNames.includes('prayer_lists_key')) {
            await StoreDB.schema.alterTable('prayer_lists', (table: any) => {
                table.index('key', 'prayer_lists_key');
            });
            Log.info('Created index: prayer_lists_key');
        }

        Log.info('Database indexes created successfully');
    } catch (error) {
        Log.error('Error creating database indexes:', error);
    }
}
