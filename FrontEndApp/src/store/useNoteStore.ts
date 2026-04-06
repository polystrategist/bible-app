import { defineStore } from 'pinia';
import { computed, onMounted, ref, watch } from 'vue';
import { debouncedRunSync } from '../util/Sync/sync';
import SESSION from '../util/session';

export type NoteItem = {
    id: string;        // = note_id in DB
    title: string;
    content: string;
    created_at: string;
    updated_at: string;
};

export default defineStore('useNotesStore', () => {
    const notes = ref<Array<NoteItem>>([]);
    const selectedNoteId = ref<string>('');
    const showNote = ref<boolean>(true);
    const isHydrating = ref(false);

    const showNoteKey = 'show-note-panel';

    onMounted(() => {
        const saved = SESSION.get(showNoteKey);
        if (saved !== null && saved !== undefined)
            showNote.value = saved !== false && saved !== 'false';
    });

    watch(() => showNote.value, (val) => SESSION.set(showNoteKey, val));

    function createDefaultNote(): NoteItem {
        const now = new Date().toISOString();
        return {
            id: `note-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
            title: 'Note 1',
            content: '',
            created_at: now,
            updated_at: now,
        };
    }

    function normalizeTitle(content: string, fallback: string): string {
        const plainText = content
            .replace(/<[^>]+>/g, ' ')
            .replace(/&nbsp;/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
        return plainText ? plainText.slice(0, 28) : fallback;
    }

    function ensureSelectedNote() {
        if (!notes.value.length) {
            selectedNoteId.value = '';
            return;
        }
        const exists = notes.value.some((n) => n.id === selectedNoteId.value);
        if (!exists) selectedNoteId.value = notes.value[0].id;
    }

    const selectedNote = computed(() => {
        if (!notes.value.length) return undefined;
        ensureSelectedNote();
        return notes.value.find((n) => n.id === selectedNoteId.value) ?? notes.value[0];
    });

    const currentNoteContent = computed({
        get() { return selectedNote.value?.content ?? ''; },
        set(value: string) {
            const selected = selectedNote.value;
            if (!selected) return;
            selected.content = value;
            selected.updated_at = new Date().toISOString();
        },
    });

    // ─── Load ───────────────────────────────────────────────────

    async function loadNote() {
        isHydrating.value = true;
        try {
            const rows: any[] = await window.browserWindow.getNotes();
            if (rows && rows.length > 0) {
                notes.value = rows.map((r) => ({
                    id: r.note_id,
                    title: r.title ?? '',
                    content: r.content ?? '',
                    created_at: r.created_at ? new Date(r.created_at).toISOString() : new Date().toISOString(),
                    updated_at: r.updated_at ? new Date(r.updated_at).toISOString() : new Date().toISOString(),
                }));
                ensureSelectedNote();
            } else {
                notes.value = [];
                selectedNoteId.value = '';
            }
        } catch (error) {
            notes.value = [];
            selectedNoteId.value = '';
        } finally {
            isHydrating.value = false;
        }
    }

    // ─── CRUD ────────────────────────────────────────────────────

    function selectNote(noteId: string) {
        selectedNoteId.value = noteId;
    }

    function addNote(title?: string) {
        const note = createDefaultNote();
        const nextNumber = notes.value.length + 1;
        const cleaned = (title ?? '').trim();
        note.title = cleaned ? cleaned.slice(0, 60) : `Note ${nextNumber}`;
        notes.value = [...notes.value, note];
        selectedNoteId.value = note.id;
    }

    function renameNote(noteId: string, title: string) {
        const note = notes.value.find((n) => n.id === noteId);
        if (!note) return;
        const cleaned = (title ?? '').trim();
        note.title = cleaned.slice(0, 60) || 'Untitled Note';
        note.updated_at = new Date().toISOString();
    }

    function deleteNote(noteId: string) {
        notes.value = notes.value.filter((n) => n.id !== noteId);
        ensureSelectedNote();
        window.browserWindow.deleteNote({ note_id: noteId });
        debouncedRunSync();
    }

    // ─── Persistence ─────────────────────────────────────────────

    async function _persistNote(note: NoteItem) {
        await window.browserWindow.upsertNote({
            note_id: note.id,
            title: note.title,
            content: note.content,
        });
    }

    function storeNote() {
        for (const note of notes.value) {
            window.browserWindow.upsertNote({
                note_id: note.id,
                title: note.title,
                content: note.content,
            });
        }
        debouncedRunSync();
    }

    watch(
        () => [notes.value, selectedNoteId.value],
        () => {
            if (isHydrating.value) return;
            clearTimeout(window.takingNoteTimeOut);
            window.takingNoteTimeOut = setTimeout(() => {
                storeNote();
            }, 700);
        },
        { deep: true }
    );

    return {
        notes,
        selectedNote,
        selectedNoteId,
        currentNoteContent,
        addNote,
        renameNote,
        deleteNote,
        selectNote,
        loadNote,
        storeNote,
        showNote,
        normalizeTitle,
    };
});
