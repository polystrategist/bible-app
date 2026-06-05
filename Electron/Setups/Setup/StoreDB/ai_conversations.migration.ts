import { StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

/**
 * `ai_conversations` stores the user's AI Assistant chat history so saved
 * conversations survive app restarts (ChatGPT/Gemini-style). Messages are kept
 * as a JSON array (`[{ role, content }]`) in a single text column — the whole
 * conversation is read/written at once, so a child message table isn't needed.
 *
 * `deleted` is a soft-delete tombstone (0/1) so a removed conversation can be
 * propagated to the backend when conversation sync is enabled (table_name =
 * 'ai_conversations', record_key = id). The id is a client-generated string
 * (uuid) so it stays stable across devices.
 */
export default async () => {
    await StoreDB.schema.hasTable('ai_conversations').then(async (exists) => {
        if (exists) return;
        try {
            await StoreDB.schema.createTable('ai_conversations', (table) => {
                table.string('id').primary();
                table.string('title').notNullable();
                table.text('messages').notNullable();
                table.integer('deleted').notNullable().defaultTo(0);
                table.string('created_at').notNullable();
                table.string('updated_at').notNullable();
            });
        } catch (e) {
            Log.error(e);
        }
    });
};
