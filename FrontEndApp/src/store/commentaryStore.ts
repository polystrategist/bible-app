import { defineStore } from 'pinia';
import { ref } from 'vue';
import SESSION from '../util/session';

export type CommentaryEntry = {
    marker: string;
    text: string;
    chapter_number_from: number;
    verse_number_from: number;
    chapter_number_to: number;
    verse_number_to: number;
};

export type CommentaryModule = {
    file: string;
    title: string;
};

export type CommentaryGroup = {
    file: string;
    title: string;
    entries: CommentaryEntry[];
};

export type CommentaryScope = 'verse' | 'chapter';

const SELECTED_FILES_KEY = 'commentary-selected-files';

/**
 * Commentaries for the Bible reader's bottom panel.
 *
 * Commentaries are decoupled from the open translation: every installed
 * commentary file is a selectable module, and the user toggles which ones to
 * show via the tab's selector. The whole chapter is fetched per selected module,
 * then narrowed to a single verse client-side via {@link matchesVerse} so the
 * Verse/Chapter toggle is instant with no refetch.
 */
export const useCommentaryStore = defineStore('commentary', () => {
    const modules = ref<CommentaryModule[]>([]);
    const selectedFiles = ref<string[]>([]);
    const groups = ref<CommentaryGroup[]>([]);
    const isLoading = ref(false);
    const scope = ref<CommentaryScope>('chapter');
    const currentKey = ref('');

    // Load the installed commentary modules and reconcile the saved selection
    // (drop removed files; default to all when nothing is saved yet).
    async function loadModules() {
        modules.value = await window.browserWindow.getCommentaryModules();
        const installed = modules.value.map((m) => m.file);
        const saved = (SESSION.get(SELECTED_FILES_KEY) as string[] | null) ?? null;
        selectedFiles.value = saved
            ? saved.filter((f) => installed.includes(f))
            : [...installed];
    }

    function setSelectedFiles(files: string[]) {
        selectedFiles.value = files;
        SESSION.set(SELECTED_FILES_KEY, files);
        currentKey.value = ''; // force the next fetch to re-run
    }

    async function fetchForChapter(book_number: number, chapter: number) {
        const key = `${selectedFiles.value.join(',')}_${book_number}_${chapter}`;
        if (currentKey.value === key) return;
        currentKey.value = key;
        isLoading.value = true;
        try {
            const titleOf = (file: string) =>
                modules.value.find((m) => m.file === file)?.title ?? file;

            const results = await Promise.all(
                selectedFiles.value.map(async (file) => ({
                    file,
                    title: titleOf(file),
                    entries: await window.browserWindow.getCommentariesByFile({
                        file,
                        book_number,
                        chapter,
                    }),
                })),
            );
            groups.value = results;
        } finally {
            isLoading.value = false;
        }
    }

    // Re-read installed modules + re-fetch (e.g. after importing a new file).
    async function reload(book_number: number, chapter: number) {
        await loadModules();
        currentKey.value = '';
        await fetchForChapter(book_number, chapter);
    }

    function clear() {
        groups.value = [];
        currentKey.value = '';
    }

    return {
        modules,
        selectedFiles,
        groups,
        isLoading,
        scope,
        loadModules,
        setSelectedFiles,
        fetchForChapter,
        reload,
        clear,
    };
});

/**
 * Does a commentary entry cover `verse`? A `*_to` of 0 means a single-verse
 * entry, so the range collapses to `verse_number_from`.
 */
export function matchesVerse(entry: CommentaryEntry, verse: number): boolean {
    const to = entry.verse_number_to > 0 ? entry.verse_number_to : entry.verse_number_from;
    return verse >= entry.verse_number_from && verse <= to;
}

/** Short "v.3" / "v.3–5" range label for an entry. */
export function formatEntryRange(entry: CommentaryEntry): string {
    const to = entry.verse_number_to > 0 ? entry.verse_number_to : entry.verse_number_from;
    return to !== entry.verse_number_from
        ? `v.${entry.verse_number_from}–${to}`
        : `v.${entry.verse_number_from}`;
}
