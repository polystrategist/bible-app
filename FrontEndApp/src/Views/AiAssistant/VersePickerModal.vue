<script lang="ts" setup>
import { ref, computed } from 'vue';
import { NModal, NSpin } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { bibleBooks, type BookInfo } from '../../util/books';
import { useBibleStore } from '../../store/BibleStore';
import { useSettingStore } from '../../store/settingStore';
import { getBibleService } from '../../services/BibleService';

defineProps<{ show: boolean }>();
const emit = defineEmits<{
    (e: 'update:show', v: boolean): void;
    (e: 'select', payload: { reference: string; verseText: string }): void;
}>();

const bibleStore = useBibleStore();
const settingStore = useSettingStore();

type Step = 'book' | 'chapter' | 'verse';
const step = ref<Step>('book');
const book = ref<BookInfo | null>(null);
const chapter = ref<number | null>(null);
const verses = ref<Array<{ verse: number; text: string }>>([]);
const loading = ref(false);

const version = computed(
    () => bibleStore.selectedBibleVersions[0] ?? 'bs_KJV - 1769.SQLite3',
);

const booksFiltered = computed(() =>
    bibleBooks.filter((b) => settingStore.showDeuterocanonical || !b.deuterocanonical),
);

function chapterCount(b: BookInfo): number {
    if (settingStore.showDeuterocanonical && b.deuterocanonical_chapter_count)
        return b.deuterocanonical_chapter_count;
    return b.chapter_count;
}

function sectionOf(bookNumber: number): string {
    if (bookNumber < 470) return 'Old Testament';
    if (bookNumber >= 740) return 'Apocrypha';
    return 'New Testament';
}

// Flatten books into section headers + book rows for the list.
const groupedBooks = computed(() => {
    const rows: Array<
        { type: 'header'; label: string } | { type: 'book'; book: BookInfo }
    > = [];
    let last = '';
    for (const b of booksFiltered.value) {
        const s = sectionOf(b.book_number);
        if (s !== last) {
            rows.push({ type: 'header', label: s });
            last = s;
        }
        rows.push({ type: 'book', book: b });
    }
    return rows;
});

// Strip MyBible markup (<S>, <J>, <f>…) to plain text for the AI — mirrors the
// reader's right-click "AI Insight" flow.
function stripVerseMarkup(text: string): string {
    return (text ?? '')
        .replace(/<[^>]*>/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
}

const title = computed(() => {
    if (step.value === 'verse') return `${book.value?.title} ${chapter.value}`;
    if (step.value === 'chapter') return book.value?.title ?? '';
    return 'Select a verse';
});

function selectBook(b: BookInfo) {
    book.value = b;
    chapter.value = null;
    step.value = 'chapter';
}

async function selectChapter(c: number) {
    chapter.value = c;
    step.value = 'verse';
    loading.value = true;
    verses.value = [];
    try {
        const raw: any[] = await getBibleService().getVerses({
            bible_versions: [version.value],
            book_number: book.value!.book_number,
            selected_chapter: c,
        });
        verses.value = raw.map((v) => ({
            verse: v.verse,
            text: stripVerseMarkup(v.version?.[0]?.text ?? ''),
        }));
    } finally {
        loading.value = false;
    }
}

function selectVerse(v: { verse: number; text: string }) {
    emit('select', {
        reference: `${book.value!.title} ${chapter.value}:${v.verse}`,
        verseText: v.text,
    });
    close();
}

function back() {
    if (step.value === 'verse') step.value = 'chapter';
    else if (step.value === 'chapter') {
        step.value = 'book';
        book.value = null;
    } else close();
}

function close() {
    emit('update:show', false);
    // Reset so the next open starts at the book list.
    step.value = 'book';
    book.value = null;
    chapter.value = null;
    verses.value = [];
}
</script>

<template>
    <NModal
        :show="show"
        @update:show="(v: boolean) => (v ? null : close())"
        :mask-closable="true"
        :auto-focus="false"
    >
        <div class="vp">
            <div class="vp__head">
                <button class="vp__back" @click="back">
                    <Icon :icon="step === 'book' ? 'lucide:x' : 'lucide:chevron-left'" />
                </button>
                <span class="vp__title">{{ title }}</span>
                <span class="vp__spacer" />
            </div>

            <!-- Step 1: book -->
            <div v-if="step === 'book'" class="vp__body">
                <template v-for="(row, i) in groupedBooks" :key="i">
                    <div v-if="row.type === 'header'" class="vp__section">
                        {{ row.label.toUpperCase() }}
                    </div>
                    <button v-else class="vp__row" @click="selectBook(row.book)">
                        <span>{{ row.book.title }}</span>
                        <Icon icon="lucide:chevron-right" class="vp__row-caret" />
                    </button>
                </template>
            </div>

            <!-- Step 2: chapter -->
            <div v-else-if="step === 'chapter'" class="vp__body vp__grid">
                <button
                    v-for="c in chapterCount(book!)"
                    :key="c"
                    class="vp__chip"
                    @click="selectChapter(c)"
                >
                    {{ c }}
                </button>
            </div>

            <!-- Step 3: verse -->
            <div v-else class="vp__body">
                <div v-if="loading" class="vp__loading"><NSpin size="small" /></div>
                <p v-else-if="verses.length === 0" class="vp__empty">No verses found.</p>
                <button
                    v-else
                    v-for="v in verses"
                    :key="v.verse"
                    class="vp__verse"
                    @click="selectVerse(v)"
                >
                    <span class="vp__verse-num">{{ v.verse }}</span>
                    <span class="vp__verse-text">{{ v.text }}</span>
                </button>
            </div>
        </div>
    </NModal>
</template>

<style scoped>
.vp {
    width: min(560px, 92vw);
    max-height: 80vh;
    display: flex;
    flex-direction: column;
    background: var(--theme-bg-elevated);
    border: 1px solid var(--theme-border);
    border-radius: 16px;
    overflow: hidden;
}
.vp__head {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 12px 8px;
    border-bottom: 1px solid var(--theme-border);
}
.vp__back {
    width: 32px;
    height: 32px;
    display: grid;
    place-items: center;
    border: none;
    background: transparent;
    color: var(--theme-text);
    cursor: pointer;
    border-radius: 8px;
    font-size: 18px;
}
.vp__back:hover { background: var(--theme-bg-soft); }
.vp__title { flex: 1; font-weight: 700; }
.vp__spacer { width: 32px; }

.vp__body { overflow-y: auto; padding: 8px; }

.vp__section {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    opacity: 0.55;
    padding: 12px 12px 6px;
}
.vp__row {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 12px;
    border: none;
    background: transparent;
    color: var(--theme-text);
    cursor: pointer;
    border-radius: 8px;
    font-size: 14px;
}
.vp__row:hover { background: var(--theme-bg-soft); }
.vp__row-caret { opacity: 0.5; }

.vp__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(52px, 1fr));
    gap: 10px;
    padding: 12px;
}
.vp__chip {
    aspect-ratio: 1;
    display: grid;
    place-items: center;
    border: 1px solid var(--theme-border);
    background: var(--theme-bg-soft);
    color: var(--theme-text);
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
}
.vp__chip:hover { border-color: var(--primary-color); }

.vp__verse {
    width: 100%;
    display: flex;
    gap: 10px;
    text-align: left;
    padding: 12px;
    margin-bottom: 6px;
    border: 1px solid var(--theme-border);
    background: var(--theme-bg-soft);
    color: var(--theme-text);
    border-radius: 12px;
    cursor: pointer;
    line-height: 1.5;
}
.vp__verse:hover { border-color: var(--primary-color); }
.vp__verse-num { color: var(--primary-color); font-weight: 700; min-width: 22px; }
.vp__verse-text { flex: 1; }

.vp__loading, .vp__empty {
    display: grid;
    place-items: center;
    padding: 28px;
    opacity: 0.7;
}
</style>
