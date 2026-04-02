import { defineStore } from 'pinia';
import { computed, ref, watch } from 'vue';
import { useBibleStore } from './BibleStore';
import { getBibleService } from '../services/BibleService';
import { useTTSStore } from './ttsStore';
import { usePiperTTSStore } from './piperTTSStore';
import { useSettingStore } from './settingStore';
import { bibleBooks } from '../util/books';
import SESSION from '../util/session';

const STORAGE_KEY_VERSION = 'flipbook-selected-version';
const STORAGE_KEY_FONT_SIZE = 'flipbook-font-size';
const STORAGE_KEY_PAGES = 'flipbook-page-positions';

export const useFlipbookStore = defineStore('useFlipbookStore', () => {
    const bibleStore = useBibleStore();

    const isOpen = ref(false);
    const showVersionSelect = ref(false);
    const selectedVersion = ref<string>(SESSION.get(STORAGE_KEY_VERSION) || '');
    const currentPage = ref(0);
    const versesPerPage = ref(12);
    const fontSize = ref(SESSION.get(STORAGE_KEY_FONT_SIZE) || 18);
    const verses = ref<any[]>([]);
    const isLoading = ref(false);

    // Flipbook's own book/chapter tracking (independent of main reader)
    const activeBookNumber = ref<number>(0);
    const activeChapter = ref<number>(1);

    // Persist font size
    watch(fontSize, (val) => SESSION.set(STORAGE_KEY_FONT_SIZE, val));

    // Persist selected version
    watch(selectedVersion, (val) => { if (val) SESSION.set(STORAGE_KEY_VERSION, val); });

    // Save page position keyed by version + book + chapter
    function pagePositionKey(): string {
        return `${selectedVersion.value}_${activeBookNumber.value}_${activeChapter.value}`;
    }

    function savePagePosition() {
        const positions = SESSION.get(STORAGE_KEY_PAGES) || {};
        positions[pagePositionKey()] = currentPage.value;
        SESSION.set(STORAGE_KEY_PAGES, positions);
    }

    function restorePagePosition() {
        const positions = SESSION.get(STORAGE_KEY_PAGES) || {};
        const saved = positions[pagePositionKey()];
        currentPage.value = typeof saved === 'number' ? saved : 0;
    }

    // Persist page when it changes
    watch(currentPage, () => { if (isOpen.value) savePagePosition(); });

    const bookTitle = computed(() => {
        const book = bibleBooks.find(b => b.book_number === activeBookNumber.value);
        return book ? book.title : '';
    });

    const activeBook = computed(() => {
        return bibleBooks.find(b => b.book_number === activeBookNumber.value) || null;
    });

    const chapterNumber = computed(() => activeChapter.value);

    const totalPages = computed(() => {
        return Math.ceil(verses.value.length / versesPerPage.value);
    });

    const currentPageVerses = computed(() => {
        const start = currentPage.value * versesPerPage.value;
        return verses.value.slice(start, start + versesPerPage.value);
    });

    const versionDisplayName = computed(() => {
        return selectedVersion.value.replace('.SQLite3', '');
    });

    function openVersionSelect() {
        // If a version was previously saved, open directly with it
        if (selectedVersion.value) {
            openFlipbook(selectedVersion.value);
        } else {
            showVersionSelect.value = true;
        }
    }

    function changeVersion() {
        showVersionSelect.value = true;
    }

    async function openFlipbook(version: string) {
        selectedVersion.value = version;
        showVersionSelect.value = false;

        // Initialize from the main reader's current position
        activeBookNumber.value = bibleStore.selectedBookNumber;
        activeChapter.value = bibleStore.selectedChapter;

        await loadVerses();
        isOpen.value = true;
    }

    async function loadVerses() {
        isLoading.value = true;

        try {
            const arg = {
                bible_versions: [selectedVersion.value],
                book_number: activeBookNumber.value,
                selected_chapter: activeChapter.value,
            };
            const bibleService = getBibleService();
            const result = await bibleService.getVerses(arg);
            verses.value = result.map((v: any) => ({
                book_number: v.book_number,
                chapter: v.chapter,
                verse: v.verse,
                text: v.version?.[0]?.text ?? '',
            }));
        } catch (e) {
            console.error('Failed to load flipbook verses:', e);
            verses.value = [];
        }

        // Restore saved page position for this version+book+chapter
        restorePagePosition();
        if (currentPage.value >= totalPages.value) {
            currentPage.value = Math.max(0, totalPages.value - 1);
        }

        isLoading.value = false;
    }

    async function navigateToBook(bookNumber: number, chapter: number) {
        activeBookNumber.value = bookNumber;
        activeChapter.value = chapter;
        currentPage.value = 0;
        await loadVerses();
    }

    async function navigateChapter(direction: 'next' | 'prev') {
        const book = activeBook.value;
        if (!book) return;

        if (direction === 'next' && activeChapter.value < book.chapter_count) {
            activeChapter.value++;
        } else if (direction === 'prev' && activeChapter.value > 1) {
            activeChapter.value--;
        } else {
            return;
        }
        currentPage.value = 0;
        await loadVerses();
    }

    function close() {
        isOpen.value = false;
        verses.value = [];
        currentPage.value = 0;
    }

    function nextPage() {
        if (currentPage.value < totalPages.value - 1) {
            currentPage.value++;
        }
    }

    function prevPage() {
        if (currentPage.value > 0) {
            currentPage.value--;
        }
    }

    function goToVerse(verseNumber: number) {
        const index = verses.value.findIndex(v => v.verse === verseNumber);
        if (index >= 0) {
            currentPage.value = Math.floor(index / versesPerPage.value);
        }
    }

    function getPlainText(): string {
        const title = `${bookTitle.value} ${chapterNumber.value} (${versionDisplayName.value})`;
        const lines = verses.value.map(v => `${v.verse}. ${stripHtml(v.text)}`);
        return `${title}\n\n${lines.join('\n\n')}`;
    }

    function stripHtml(html: string): string {
        const div = document.createElement('div');
        div.innerHTML = html;
        return div.textContent || div.innerText || '';
    }

    function downloadAsTxt() {
        const text = getPlainText();
        const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
        triggerDownload(blob, `${bookTitle.value}_${chapterNumber.value}.txt`);
    }

    function downloadAsWord() {
        const title = `${bookTitle.value} ${chapterNumber.value} (${versionDisplayName.value})`;
        const versesHtml = verses.value
            .map(v => `<p><b>${v.verse}.</b> ${v.text}</p>`)
            .join('');
        const html = `
            <html xmlns:o="urn:schemas-microsoft-com:office:office"
                  xmlns:w="urn:schemas-microsoft-com:office:word"
                  xmlns="http://www.w3.org/TR/REC-html40">
            <head><meta charset="utf-8"><title>${title}</title></head>
            <body>
                <h1>${title}</h1>
                ${versesHtml}
            </body></html>`;
        const blob = new Blob([html], { type: 'application/msword' });
        triggerDownload(blob, `${bookTitle.value}_${chapterNumber.value}.doc`);
    }

    function downloadAsPdf() {
        const title = `${bookTitle.value} ${chapterNumber.value} (${versionDisplayName.value})`;
        const versesHtml = verses.value
            .map(v => `<p style="margin:4px 0;line-height:1.6"><b>${v.verse}.</b> ${v.text}</p>`)
            .join('');
        const printWindow = window.open('', '_blank');
        if (!printWindow) return;
        printWindow.document.write(`
            <!DOCTYPE html>
            <html><head><meta charset="utf-8">
            <title>${title}</title>
            <style>
                body { font-family: Georgia, serif; max-width: 700px; margin: 40px auto; padding: 20px; color: #222; }
                h1 { text-align: center; font-size: 24px; margin-bottom: 20px; }
                p { font-size: 14px; }
            </style></head>
            <body>
                <h1>${title}</h1>
                ${versesHtml}
            </body></html>
        `);
        printWindow.document.close();
        printWindow.onload = () => {
            printWindow.print();
            printWindow.close();
        };
    }

    function triggerDownload(blob: Blob, filename: string) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    return {
        isOpen,
        showVersionSelect,
        selectedVersion,
        currentPage,
        versesPerPage,
        fontSize,
        verses,
        isLoading,
        activeBookNumber,
        activeChapter,
        activeBook,
        bookTitle,
        chapterNumber,
        totalPages,
        currentPageVerses,
        versionDisplayName,
        openVersionSelect,
        changeVersion,
        openFlipbook,
        navigateToBook,
        navigateChapter,
        close,
        nextPage,
        prevPage,
        goToVerse,
        getPlainText,
        stripHtml,
        downloadAsTxt,
        downloadAsWord,
        downloadAsPdf,
    };
});
