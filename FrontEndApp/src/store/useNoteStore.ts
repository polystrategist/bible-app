import { defineStore } from 'pinia';
import { computed, ref, watch } from 'vue';
import SpaceStudyStore from './SpaceStudyStore';
import { runSync } from '../util/Sync/sync';

type NoteItem = {
    id: string;
    title: string;
    content: string;
    created_at: string;
    updated_at: string;
};

type StoredMultiNotePayload = {
    type: 'multi-note-v1';
    selected_note_id: string;
    notes: Array<NoteItem>;
};

export default defineStore('useNotesStore', () => {
    const notes = ref<Array<NoteItem>>([]);
    const selectedNoteId = ref<string>('');
    const showNote = ref<boolean>(true);
    const spaceStudyStore = SpaceStudyStore();
    const isHydrating = ref(false);

    function createDefaultNote(content = ''): NoteItem {
        const now = new Date().toISOString();
        return {
            id: `note-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
            title: 'Note 1',
            content,
            created_at: now,
            updated_at: now,
        };
    }

    function normalizeTitle(content: string, fallback: string) {
        const plainText = content
            .replace(/<[^>]+>/g, ' ')
            .replace(/&nbsp;/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();

        if (!plainText) {
            return fallback;
        }

        return plainText.slice(0, 28);
    }

    function ensureSelectedNote() {
        if (!notes.value.length) {
            const first = createDefaultNote('');
            notes.value = [first];
            selectedNoteId.value = first.id;
            return;
        }

        const selectedExists = notes.value.some((noteItem) => noteItem.id === selectedNoteId.value);
        if (!selectedExists) {
            selectedNoteId.value = notes.value[0].id;
        }
    }

    const selectedNote = computed(() => {
        ensureSelectedNote();
        return notes.value.find((noteItem) => noteItem.id === selectedNoteId.value) || notes.value[0];
    });

    const currentNoteContent = computed({
        get() {
            return selectedNote.value?.content || '';
        },
        set(value: string) {
            const selected = selectedNote.value;
            if (!selected) {
                return;
            }

            selected.content = value;
            selected.updated_at = new Date().toISOString();
        },
    });

    function renameNote(noteId: string, title: string) {
        const noteToRename = notes.value.find((noteItem) => noteItem.id === noteId);
        if (!noteToRename) {
            return;
        }

        const cleaned = (title || '').trim();
        noteToRename.title = cleaned.slice(0, 60) || 'Untitled Note';
        noteToRename.updated_at = new Date().toISOString();
    }

    function serializePayload(): string {
        const payload: StoredMultiNotePayload = {
            type: 'multi-note-v1',
            selected_note_id: selectedNoteId.value,
            notes: notes.value,
        };

        return JSON.stringify(payload);
    }

    function hydrateFromStoredContent(content?: string | null) {
        isHydrating.value = true;

        if (!content) {
            const defaultNote = createDefaultNote('');
            notes.value = [defaultNote];
            selectedNoteId.value = defaultNote.id;
            isHydrating.value = false;
            return;
        }

        try {
            const parsed = JSON.parse(content) as StoredMultiNotePayload;
            if (parsed?.type === 'multi-note-v1' && Array.isArray(parsed.notes)) {
                const normalized = parsed.notes.map((noteItem, index) => ({
                    id: noteItem.id || `note-${Date.now()}-${index}`,
                    title: noteItem.title || `Note ${index + 1}`,
                    content: noteItem.content || '',
                    created_at: noteItem.created_at || new Date().toISOString(),
                    updated_at: noteItem.updated_at || new Date().toISOString(),
                }));

                notes.value = normalized.length ? normalized : [createDefaultNote('')];
                selectedNoteId.value = parsed.selected_note_id || notes.value[0].id;
                ensureSelectedNote();
                isHydrating.value = false;
                return;
            }
        } catch (error) {
            // Old content is plain HTML/string, so we treat it as a single existing note.
        }

        const singleNote = createDefaultNote(content);
        singleNote.title = normalizeTitle(content, 'Note 1');
        notes.value = [singleNote];
        selectedNoteId.value = singleNote.id;
        isHydrating.value = false;
    }

    async function loadNoteForSelectedSpace(spaceStudyId?: number | string | null) {
        const targetSpaceId = (spaceStudyId || spaceStudyStore.selectedSpaceStudy?.id) as number | string;
        if (!targetSpaceId) {
            hydrateFromStoredContent('');
            return;
        }

        try {
            const storedNote = await window.browserWindow.getNote(Number(targetSpaceId));
            hydrateFromStoredContent(storedNote?.content || '');
        } catch (error) {
            hydrateFromStoredContent('');
        }
    }

    function selectNote(noteId: string) {
        selectedNoteId.value = noteId;
    }

    function addNote(title?: string) {
        const nextNumber = notes.value.length + 1;
        const newNote = createDefaultNote('');
        const cleanedTitle = (title || '').trim();
        newNote.title = cleanedTitle ? cleanedTitle.slice(0, 60) : `Note ${nextNumber}`;
        notes.value = [...notes.value, newNote];
        selectedNoteId.value = newNote.id;
    }

    function deleteNote(noteId: string) {
        if (notes.value.length <= 1) {
            notes.value = [createDefaultNote('')];
            selectedNoteId.value = notes.value[0].id;
            return;
        }

        notes.value = notes.value.filter((noteItem) => noteItem.id !== noteId);
        ensureSelectedNote();
    }

    function storeNote() {
        const selectedSpaceId = spaceStudyStore.selectedSpaceStudy?.id as number | string;
        if (!selectedSpaceId) {
            return;
        }

        // NOTE: save note to database table
        window.browserWindow.saveNote({
            note: serializePayload(),
            space_study_id: selectedSpaceId,
        });
        runSync();
    }

    watch(
        () => [notes.value, selectedNoteId.value],
        () => {
            if (isHydrating.value) {
                return;
            }
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
        loadNoteForSelectedSpace,
        storeNote,
        showNote,
    };
});
