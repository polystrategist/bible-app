import { removeUniqueConstraint, StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

export default async () => {
    await StoreDB.schema.hasTable('highlights').then(async (exists) => {
        try {
            if (!exists) {
                await StoreDB.schema
                    .createTable('highlights', function (table) {
                        table.increments('id').primary();
                        table.string('key');
                        table.integer('book_number');
                        table.integer('chapter');
                        table.integer('verse');
                        table.string('content');
                        table.timestamps(true);
                    })
                    .then();
            } else {
                await removeUniqueConstraint('highlights', 'key');

                // Migrate old version-specific highlights to version-independent format
                await migrateOldHighlights();
            }
        } catch (e) {
            console.log(e);
        }
    });
};

/**
 * Migrates old highlights from version-specific keys and HTML content
 * to version-independent keys and hex color content.
 *
 * Old format:
 *   key: "King James Version - 1769_10_1_1"
 *   content: '<span class="HasHighlightSpan" style="background: #FFD26A">verse text</span>'
 *
 * New format:
 *   key: "10_1_1"
 *   content: "#FFD26A"
 */
async function migrateOldHighlights() {
    try {
        // Find rows with old HTML content (contains HasHighlightSpan)
        const oldHighlights = await StoreDB('highlights')
            .whereLike('content', '%HasHighlightSpan%');

        if (!oldHighlights.length) return;

        Log.info(`[Highlights Migration] Found ${oldHighlights.length} old-format highlights to migrate`);

        for (const hl of oldHighlights) {
            // Extract color from HTML content
            const colorMatch = hl.content.match(/background:\s*([^"';]+)/);
            const color = colorMatch ? colorMatch[1].trim() : '#FFD26A'; // default yellow

            // Build version-independent key
            const newKey = `${hl.book_number}_${hl.chapter}_${hl.verse}`;

            // Check if a new-format highlight already exists for this verse
            const existing = await StoreDB('highlights')
                .where('key', newKey)
                .first();

            if (existing) {
                // New format already exists, just delete the old row
                await StoreDB('highlights').where('id', hl.id).del();
            } else {
                // Update the old row to new format
                await StoreDB('highlights').where('id', hl.id).update({
                    key: newKey,
                    content: color,
                });
            }
        }

        Log.info(`[Highlights Migration] Migration complete`);
    } catch (e) {
        Log.error('[Highlights Migration] Error:', e);
    }
}
