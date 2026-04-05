import { StoreDB } from '../../../DataBase/DataBase';

export default async () => {
    // Create table if it doesn't exist
    const exists = await StoreDB.schema.hasTable('notes');
    if (!exists) {
        await StoreDB.schema.createTable('notes', function (table) {
            table.increments('id').primary();
            table.string('note_id').notNullable().defaultTo('');
            table.string('title').notNullable().defaultTo('');
            table.text('content').defaultTo('');
            table.timestamps(true);
        });
        return;
    }

    // Add note_id column if missing (schema upgrade from single-row to per-row)
    const hasNoteId = await StoreDB.schema.hasColumn('notes', 'note_id');
    if (!hasNoteId) {
        await StoreDB.schema.table('notes', function (table) {
            table.string('note_id').defaultTo('');
            table.string('title').defaultTo('');
        });

        // Migrate existing single-row blob to individual rows
        const existingRow = await StoreDB('notes').first();
        if (existingRow) {
            const raw: string = existingRow.content ?? '';
            let parsed: any = null;
            try { parsed = JSON.parse(raw); } catch (_) { /* not JSON */ }

            if (parsed?.type === 'multi-note-v1' && Array.isArray(parsed.notes)) {
                // Delete the old blob row
                await StoreDB('notes').where('id', existingRow.id).delete();
                // Insert one row per note
                for (const note of parsed.notes) {
                    const noteId = note.id || `note-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
                    await StoreDB('notes').insert({
                        note_id: noteId,
                        title: note.title ?? 'Note',
                        content: note.content ?? '',
                        created_at: note.created_at ? new Date(note.created_at) : new Date(),
                        updated_at: note.updated_at ? new Date(note.updated_at) : new Date(),
                    });
                }
            } else {
                // Plain HTML or empty — promote the existing row
                const noteId = `note-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
                await StoreDB('notes').where('id', existingRow.id).update({
                    note_id: noteId,
                    title: 'Note 1',
                });
            }
        }
    }
};
