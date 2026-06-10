import clip_noteMigration from './StoreDB/clip_note.migration';
import prayerListMigration from './StoreDB/prayerList.migration';
import bookmarksMigration from './StoreDB/bookmarks.migration';
import highlightsMigration from './StoreDB/highlights.migration';
import notesMigration from './StoreDB/notes.migration';
import syncLogsMigration from './StoreDB/sync_logs.migration';
import cachedSermonsMigration from './StoreDB/cached_sermons.migration';
import sermonFavoritesMigration from './StoreDB/sermon_favorites.migration';
import aiConversationsMigration from './StoreDB/ai_conversations.migration';
import aiInsightsMigration from './StoreDB/ai_insights.migration';
import prayerDaysMigration from './StoreDB/prayer_days.migration';
import devotionDaysMigration from './StoreDB/devotion_days.migration';
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

        // setup sermons offline cache + favorites
        await cachedSermonsMigration();
        await sermonFavoritesMigration();

        // setup AI Assistant conversation history
        await aiConversationsMigration();

        // setup AI insight/sermon local cache
        await aiInsightsMigration();

        // setup prayer-streak days
        await prayerDaysMigration();

        // setup devotion-streak days
        await devotionDaysMigration();
    } catch (e) {
        try {
            Log.error(e);
        } catch (e) {
            Log.error('SetStoreDatabase.ts');
        }
    }
};
