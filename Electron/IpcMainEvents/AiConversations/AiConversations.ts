import { ipcMain } from 'electron';
import Log from 'electron-log';
import { StoreDB, updateOrCreate } from '../../DataBase/DataBase';
import { logSyncChange, getSyncSetting } from '../../DataBase/SyncDB';

/**
 * IPC handlers for AI Assistant conversation history (`ai_conversations`).
 *
 * Conversations are stored locally and only enter the sync queue when the user
 * has turned on conversation sync (`ai_conversations_sync` sync setting) — that
 * keeps the chat history device-local by default and opt-in to cross-device.
 */

interface ConversationPayload {
    id: string;
    title: string;
    messages: Array<{ role: string; content: string }>;
    created_at?: string;
}

async function conversationSyncEnabled(): Promise<boolean> {
    try {
        return Boolean(await getSyncSetting('ai_conversations_sync'));
    } catch {
        return false;
    }
}

function rowToConversation(row: any) {
    return {
        id: row.id,
        title: row.title,
        messages: safeParseMessages(row.messages),
        created_at: row.created_at,
        updated_at: row.updated_at,
    };
}

function safeParseMessages(raw: unknown): Array<{ role: string; content: string }> {
    if (typeof raw !== 'string') return [];
    try {
        const parsed = JSON.parse(raw);
        return Array.isArray(parsed) ? parsed : [];
    } catch {
        return [];
    }
}

export default () => {
    // List conversations (most-recent first), excluding soft-deleted ones.
    ipcMain.handle('getAiConversations', async () => {
        try {
            const rows = await StoreDB('ai_conversations')
                .select()
                .where('deleted', 0)
                .orderBy('updated_at', 'desc');
            return rows.map(rowToConversation);
        } catch (e) {
            Log.error('getAiConversations failed:', e);
            return [];
        }
    });

    // Fetch a single conversation by id.
    ipcMain.handle('getAiConversation', async (_event, id: string) => {
        try {
            const row = await StoreDB('ai_conversations').where({ id }).first();
            return row && !row.deleted ? rowToConversation(row) : null;
        } catch (e) {
            Log.error('getAiConversation failed:', e);
            return null;
        }
    });

    // Create or update a conversation (whole-record upsert keyed by id).
    ipcMain.handle('saveAiConversation', async (_event, payload: ConversationPayload) => {
        try {
            const existing = await StoreDB('ai_conversations').where({ id: payload.id }).first();
            const now = new Date().toISOString();
            const messagesJson = JSON.stringify(payload.messages ?? []);

            await updateOrCreate(
                'ai_conversations',
                { id: payload.id },
                {
                    title: payload.title,
                    messages: messagesJson,
                    deleted: 0,
                    updated_at: now,
                    created_at: existing?.created_at ?? payload.created_at ?? now,
                }
            );

            if (await conversationSyncEnabled()) {
                try {
                    await logSyncChange({
                        table_name: 'ai_conversations',
                        record_key: payload.id,
                        action: existing ? 'updated' : 'created',
                        payload: {
                            id: payload.id,
                            title: payload.title,
                            messages: messagesJson,
                            deleted: 0,
                        },
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('Failed to log sync change for ai conversation:', e);
                }
            }

            const row = await StoreDB('ai_conversations').where({ id: payload.id }).first();
            return row ? rowToConversation(row) : null;
        } catch (e) {
            Log.error('saveAiConversation failed:', e);
            return null;
        }
    });

    // Soft-delete a conversation (tombstone), so the delete can sync if enabled.
    ipcMain.handle('deleteAiConversation', async (_event, id: string) => {
        try {
            const existing = await StoreDB('ai_conversations').where({ id }).first();
            if (!existing) return false;

            const now = new Date().toISOString();
            await StoreDB('ai_conversations')
                .where({ id })
                .update({ deleted: 1, updated_at: now });

            if (await conversationSyncEnabled()) {
                try {
                    await logSyncChange({
                        table_name: 'ai_conversations',
                        record_key: id,
                        action: 'deleted',
                        payload: { id, deleted: 1 },
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('Failed to log sync change for ai conversation deletion:', e);
                }
            }
            return true;
        } catch (e) {
            Log.error('deleteAiConversation failed:', e);
            return false;
        }
    });
};
