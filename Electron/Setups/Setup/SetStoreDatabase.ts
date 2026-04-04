import clip_noteMigration from './StoreDB/clip_note.migration';
import prayerListMigration from './StoreDB/prayerList.migration';
import bookmarksMigration from './StoreDB/bookmarks.migration';
import highlightsMigration from './StoreDB/highlights.migration';
import notesMigration from './StoreDB/notes.migration';
import syncLogsMigration from './StoreDB/sync_logs.migration';
import dailyDevotionalsMigration from './StoreDB/daily_devotionals.migration';
import Log from 'electron-log';

export default async () => {
    try {
        // setup clip_notes
        await clip_noteMigration();

        // setup prayer list
        await prayerListMigration();

        // setup bookmark
        await bookmarksMigration();

        // setup highlights
        await highlightsMigration();

        // set note migration
        await notesMigration();

        // setup sync_logs
        await syncLogsMigration();

        // setup daily devotionals
        await dailyDevotionalsMigration();
    } catch (e) {
        try {
            Log.error(e);
        } catch (e) {
            Log.error('SetStoreDatabase.ts');
        }
    }
};
