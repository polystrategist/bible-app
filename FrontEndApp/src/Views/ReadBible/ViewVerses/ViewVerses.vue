<script lang="ts" setup>
import { onBeforeMount, onMounted, onUnmounted, ref, watch, h, computed, nextTick } from 'vue';
import { useBibleStore } from '../../../store/BibleStore';
import { NButton, NIcon, NPopover, NSelect, NSlider, useDialog, useMessage } from 'naive-ui';
import { Attachment, BookmarkFilled, Copy, Delete, Edit, Add, Close } from '@vicons/carbon';
import SESSION from '../../../util/session';
import { useMouse } from '@vueuse/core';
import ContextMenu from './ContextMenu/ContextMenu.vue';
import { useBookmarkStore } from '../../../store/bookmark';
import CreateClipNoteVue from '../../../components/ClipNotes/CreateClipNote.vue';
import { useClipNoteStore } from '../../../store/ClipNotes';
import { getSelectionParentElement } from '../../../util/ElementUtil';
import VerseSelector from '../../../components/VerseSelector.vue';
import { useI18n } from 'vue-i18n';
import { FastForward20Regular, SlideSearch28Regular } from '@vicons/fluent';
import { SlideSearch28Filled } from '@vicons/fluent';
import { Note24Regular, Note28Filled } from '@vicons/fluent';
import { useThemeStore } from '../../../store/theme';
import useNoteStore from '../../../store/useNoteStore';
import { useTTSStore } from '../../../store/ttsStore';
import { usePiperTTSStore } from '../../../store/piperTTSStore';
import { useSettingStore } from '../../../store/settingStore';
import { useMainStore } from '../../../store/main';
import { Icon } from '@iconify/vue';
import PiperModelsModal from '../../../components/Settings/VerseReader/PiperModelsModal.vue';
import FootnotePopover from '../../../components/FootnotePopover/FootnotePopover.vue';
import { useFlipbookStore } from '../../../store/flipbookStore';
import { useModuleStore } from '../../../store/moduleStore';
import { Splitpanes, Pane } from 'splitpanes';

const { t } = useI18n();
const showPiperModels = ref(false);

const voiceReaderLabel = computed(() => {
    return settingStore.verseReaderMode === 'piper-tts' ? 'Piper TTS' : 'Browser TTS';
});

const piperVoiceLabel = computed(() => {
    const id = settingStore.piperActiveModel;
    const parts = id.split('-');
    // parts: ['en_US', 'ryan', 'high'] → 'Ryan · High'
    const name = parts[1] ?? '';
    const quality = parts[2] ?? '';
    return `${name.charAt(0).toUpperCase() + name.slice(1)} · ${quality.charAt(0).toUpperCase() + quality.slice(1)}`;
});
const themeStore = useThemeStore();
const noteStore = useNoteStore();
const ttsStore = useTTSStore();
const piperStore = usePiperTTSStore();
const settingStore = useSettingStore();
const mainStore = useMainStore();
const flipbookStore = useFlipbookStore();

const moduleStore = useModuleStore();

// --- Split View ---
const storageSplitPaneSizesKey = 'verse-split-pane-sizes';
const storageScrollPositionKey = 'verse-scroll-position';
const splitPaneSizes = ref<number[]>([100]);
const scrollPaneRefs = ref<(HTMLElement | null)[]>([]);
const verseSkeletonRows = [0, 1, 2, 3, 4];
let activePaneIndex: number | null = null;
let saveScrollTimeout: ReturnType<typeof setTimeout> | null = null;

function versionOptionsForPane(paneIndex: number) {
    const usedByOtherPanes = bibleStore.selectedBibleVersions.filter(
        (_: string, i: number) => i !== paneIndex,
    );
    return moduleStore.bibleLists
        .filter(
            (b: any) =>
                !b.title.includes('commentaries') && !usedByOtherPanes.includes(b.file_name),
        )
        .map((b: any) => ({
            label: b.title,
            value: b.file_name,
        }));
}

function changeVersion(paneIndex: number, newVersion: string) {
    bibleStore.selectedBibleVersions[paneIndex] = newVersion;
    bibleStore.getVerses();
}

async function versionHasCurrentChapter(versionFile: string) {
    const verseCount = await window.browserWindow.getVersesCount(
        JSON.stringify({
            bible_versions: [versionFile],
            book_number: bibleStore.selectedBookNumber,
            selected_chapter: bibleStore.selectedChapter,
        }),
    );

    return verseCount > 0;
}

async function addSplit() {
    if (bibleStore.selectedBibleVersions.length >= 6) return;
    const available = moduleStore.bibleLists.filter(
        (b: any) =>
            !b.title.includes('commentaries') &&
            !bibleStore.selectedBibleVersions.includes(b.file_name),
    );

    let newVersion = available[0]?.file_name ?? bibleStore.DefaultSelectedVersion;
    for (const candidate of available) {
        if (await versionHasCurrentChapter(candidate.file_name)) {
            newVersion = candidate.file_name;
            break;
        }
    }

    bibleStore.selectedBibleVersions.push(newVersion);
    // Distribute pane sizes evenly
    const count = bibleStore.selectedBibleVersions.length;
    splitPaneSizes.value = Array(count).fill(100 / count);
    SESSION.set(storageSplitPaneSizesKey, splitPaneSizes.value);
    bibleStore.getVerses();
}

function paneHasVisibleVerses(paneIndex: number) {
    return bibleStore.renderVerses.some((verse) => verse.version[paneIndex]?.text);
}

const showVerseSkeletons = computed(() => !window.isElectron && bibleStore.isLoadingVerses);

function removeSplit(paneIndex: number) {
    if (bibleStore.selectedBibleVersions.length <= 1) return;
    bibleStore.selectedBibleVersions.splice(paneIndex, 1);
    // Redistribute sizes evenly
    const count = bibleStore.selectedBibleVersions.length;
    splitPaneSizes.value = Array(count).fill(100 / count);
    SESSION.set(storageSplitPaneSizesKey, splitPaneSizes.value);
    bibleStore.getVerses();
}

function onSplitResized(sizes: Array<{ size: number }>) {
    splitPaneSizes.value = sizes.map((s) => s.size);
    SESSION.set(storageSplitPaneSizesKey, splitPaneSizes.value);
}

function getTopVisibleVerse(scrollEl: HTMLElement): { verse: number; proportion: number } | null {
    const scrollTop = scrollEl.scrollTop;
    const paneTop = scrollEl.offsetTop;
    const children = scrollEl.children;
    // Binary search for the first verse element whose bottom is below scrollTop
    let lo = 0;
    let hi = children.length - 1;
    while (lo < hi) {
        const mid = (lo + hi) >>> 1;
        const el = children[mid] as HTMLElement;
        if (el.offsetTop - paneTop + el.offsetHeight <= scrollTop) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    const el = children[lo] as HTMLElement | undefined;
    if (!el) return null;
    const verseEl = el.querySelector<HTMLElement>('[data-verse]');
    if (!verseEl) return null;
    const elTop = verseEl.offsetTop - paneTop;
    return {
        verse: Number(verseEl.dataset.verse),
        proportion: (scrollTop - elTop) / (verseEl.offsetHeight || 1),
    };
}

function scrollPaneToVerse(scrollEl: HTMLElement, verse: number, proportion: number) {
    const targetVerseEl = scrollEl.querySelector<HTMLElement>(`[data-verse="${verse}"]`);
    if (!targetVerseEl) return;
    scrollEl.scrollTop = targetVerseEl.offsetTop - scrollEl.offsetTop + proportion * targetVerseEl.offsetHeight;
}

function saveScrollPosition(scrollEl: HTMLElement) {
    if (saveScrollTimeout) clearTimeout(saveScrollTimeout);
    saveScrollTimeout = setTimeout(() => {
        const pos = getTopVisibleVerse(scrollEl);
        if (pos) SESSION.set(storageScrollPositionKey, pos);
    }, 200);
}

let isRestoringScroll = false;

function restoreScrollPosition() {
    const saved = SESSION.get(storageScrollPositionKey);
    if (!saved) return;
    isRestoringScroll = true;
    // Wait for DOM to render verses
    nextTick(() => {
        setTimeout(() => {
            scrollPaneRefs.value.forEach((el) => {
                if (el) scrollPaneToVerse(el as HTMLElement, saved.verse, saved.proportion);
            });
            // Keep the flag on briefly so the renderVerses watcher doesn't override
            setTimeout(() => {
                isRestoringScroll = false;
            }, 300);
        }, 100);
    });
}

function onPaneMouseEnter(paneIndex: number) {
    activePaneIndex = paneIndex;
}

function syncScroll(sourcePaneIndex: number) {
    if (activePaneIndex !== sourcePaneIndex) return;
    const source = scrollPaneRefs.value[sourcePaneIndex];
    if (!source) return;

    const pos = getTopVisibleVerse(source as HTMLElement);
    if (!pos) return;

    const panes = scrollPaneRefs.value;
    for (let i = 0; i < panes.length; i++) {
        if (i === sourcePaneIndex || !panes[i]) continue;
        scrollPaneToVerse(panes[i] as HTMLElement, pos.verse, pos.proportion);
    }

    saveScrollPosition(source as HTMLElement);
}

function setScrollPaneRef(index: number, el: any) {
    scrollPaneRefs.value[index] = el as HTMLElement | null;
}

// Initialize split sizes from storage
function initSplitSizes() {
    const saved = SESSION.get(storageSplitPaneSizesKey);
    const count = bibleStore.selectedBibleVersions.length;
    if (saved && saved.length === count) {
        splitPaneSizes.value = saved;
    } else {
        splitPaneSizes.value = Array(count).fill(100 / count);
    }
}

function scrollAllPanesToVerse(verseNumber: number) {
    if (isRestoringScroll) return;

    function doScroll() {
        scrollPaneRefs.value.forEach((el) => {
            if (!el) return;
            const pane = el as HTMLElement;
            const verseEl = pane.querySelector<HTMLElement>(`[data-verse="${verseNumber}"]`);
            if (!verseEl) return;
            const paneRect = pane.getBoundingClientRect();
            const verseRect = verseEl.getBoundingClientRect();
            pane.scrollTop += verseRect.top - paneRect.top - 10;
        });
        const firstPane = scrollPaneRefs.value[0] as HTMLElement | null;
        if (firstPane) {
            const pos = getTopVisibleVerse(firstPane);
            if (pos) SESSION.set(storageScrollPositionKey, pos);
        }
    }

    // Always wait for DOM to settle after verse data changes
    nextTick(() => {
        requestAnimationFrame(doScroll);
    });
}

// Watcher for verse/chapter scroll sync — registered in onMounted to avoid setup errors

function activeStore() {
    return settingStore.verseReaderMode === 'piper-tts' ? piperStore : ttsStore;
}

function playVerse(verseIndex: number, versionIndex: number) {
    // Stop both engines before playing to avoid overlap
    ttsStore.stop();
    piperStore.stop();

    switch (settingStore.verseReaderMode) {
        case 'piper-tts':
            if (!piperStore.isInstalled) {
                dialog.warning({
                    title: 'Piper Not Installed',
                    content:
                        'Piper Neural TTS needs to be downloaded before use. Go to Settings → Verse Reader to install it.',
                    positiveText: 'Open Settings',
                    negativeText: 'Cancel',
                    onPositiveClick: () => {
                        mainStore.settingsTab = 'VerseReader';
                        mainStore.showSettings = true;
                    },
                });
                return;
            }
            piperStore.playFromVerse(verseIndex, versionIndex);
            break;
        case 'browser-tts':
        default:
            ttsStore.playFromVerse(verseIndex, versionIndex);
            break;
    }
}
const dialog = useDialog();
const clipNoteStore = useClipNoteStore();
const fontSizeOfShowChapter = 'font-size-of-show-chapter';
const bibleStore = useBibleStore();
const fontSize = ref(15);
const showContextMenu = ref(false);
const contextMenuPositionX = ref<number>(0);
const contextMenuPositionY = ref<number>(0);
const contextMenuData = ref({});
const contextMenuVerseKey = ref<string>('');
const bookmarkStore = useBookmarkStore();
const showPopOver = ref(false);
const selectedPassageTextForCopy = ref<string | null>(null);
const { x, y } = useMouse();
let verseCopyListener: ((event: ClipboardEvent) => void) | null = null;
let forcedPassageCopyText: string | null = null;

const footnotePopover = ref({
    show: false,
    x: 0,
    y: 0,
    marker: '',
    text: '',
});

async function handleFootnoteHover(event: MouseEvent, version: any, verse: any) {
    const target = event.target as HTMLElement;
    const footnoteEl =
        target.tagName.toLowerCase() === 'f'
            ? target
            : (target.closest?.('f') as HTMLElement | null);

    if (!footnoteEl) {
        footnotePopover.value.show = false;
        return;
    }

    const marker = footnoteEl.textContent?.trim() ?? '';
    if (!marker) return;

    const footnotes: Array<{ marker: string; text: string }> = await (
        window as any
    ).browserWindow.getCommentaryForVerse(
        JSON.stringify({
            version: version.version,
            book_number: verse.book_number,
            chapter: verse.chapter,
            verse: verse.verse,
        }),
    );

    const match = footnotes.find((f) => f.marker === marker);
    if (!match) return;

    const rect = footnoteEl.getBoundingClientRect();
    footnotePopover.value = {
        show: true,
        x: rect.left + rect.width / 2,
        y: rect.top - 8,
        marker,
        text: match.text,
    };
}
const message = useMessage();
const createClipNoteRef = ref<null | { toggleClipNoteModal: Function }>(null);
const clipNoteRender: any = (key: any) => {
    return (clipNoteStore.chapterClipNotes as any)[key]
        ? (clipNoteStore.chapterClipNotes as any)[key]
        : false;
};
const fontSelected = ref('Poppins');
const bundledFonts = [
    { label: 'Poppins', value: 'Poppins' },
    { label: 'Inter', value: 'Inter' },
    { label: 'Zodiac', value: 'Zodiac' },
];
const fontOptions = ref<any[]>([...bundledFonts]);

async function loadSystemFonts() {
    try {
        const fonts: any[] = await (window as any).queryLocalFonts();
        const families = [...new Set(fonts.map((f) => f.family as string))].sort();
        const systemFonts = families
            .filter((f) => !bundledFonts.some((b) => b.value === f))
            .map((f) => ({ label: f, value: f }));
        fontOptions.value = [
            { type: 'group', label: 'Bundled', key: 'bundled', children: bundledFonts },
            { type: 'group', label: 'System Fonts', key: 'system', children: systemFonts },
        ];
    } catch {
        // queryLocalFonts not available or permission denied — keep bundled fonts only
    }
}

watch(
    () => fontSelected.value,
    (FSelected: string) => {
        SESSION.set('font-family-of-show-chapter', FSelected);
        document.documentElement.style.setProperty('--bible-font-family', FSelected);
    },
);

watch(
    () => fontSize.value,
    (FSize: number) => {
        SESSION.set(fontSizeOfShowChapter, FSize);
    },
);

// Keep split sizes in sync with selected versions count
watch(
    () => bibleStore.selectedBibleVersions.length,
    (count) => {
        if (splitPaneSizes.value.length !== count) {
            splitPaneSizes.value = Array(count).fill(100 / count);
            SESSION.set(storageSplitPaneSizesKey, splitPaneSizes.value);
        }
    },
);

// Stop TTS when the chapter or book changes — unless TTS itself triggered the chapter advance
watch(
    () => [bibleStore.selectedChapter, bibleStore.selectedBookNumber],
    () => {
        const s = activeStore();
        if (s.isActive && !s.autoAdvancing) s.stop();
    },
);

async function navigateChapter(action: 'next' | 'before') {
    if (action == 'before' && bibleStore.selectedChapter == 1) return;
    if (action == 'next' && bibleStore.selectedChapter == bibleStore.selectedBook.chapter_count)
        return;

    await bibleStore.selectChapter(
        action == 'next' ? bibleStore.selectedChapter + 1 : bibleStore.selectedChapter - 1,
    );
    bibleStore.AutoScrollSavedPosition();
}

function clickContextMenu(verse: Object) {
    contextMenuData.value = verse;
    contextMenuVerseKey.value = (verse as any).key;

    if (showContextMenu.value) {
        showContextMenu.value = false;
        contextMenuVerseKey.value = '';
    } else {
        showContextMenu.value = true;
        contextMenuPositionX.value = x.value;
        contextMenuPositionY.value = y.value;
    }
}

watch(showContextMenu, (val) => {
    if (!val) contextMenuVerseKey.value = '';
});

function getCleanVerseTextForCopy(element: HTMLElement) {
    const clone = element.cloneNode(true) as HTMLElement;
    clone.querySelectorAll('a, s, f').forEach((hiddenElement) => hiddenElement.remove());

    return (clone.textContent ?? '').replace(/\s+/g, ' ').trim();
}

function getSelectedVerseElements(selection: Selection) {
    if (!selection.rangeCount || !selection.toString().trim()) return [];

    const container = document.getElementById('view-verses-container');
    if (!container) return [];

    const range = selection.getRangeAt(0);

    return Array.from(container.querySelectorAll<HTMLElement>('.verse-select-text')).filter(
        (element) => {
            try {
                return range.intersectsNode(element);
            } catch {
                return false;
            }
        },
    );
}

function getSelectedPassageTextForCopy(includeRawFallback = true) {
    const selected = window.getSelection();
    if (!selected) return null;

    const selectedVerseElements = getSelectedVerseElements(selected);
    if (!selectedVerseElements.length) {
        return includeRawFallback ? selected.toString().trim() || null : null;
    }

    const selectedVerses = selectedVerseElements
        .map((element) => ({
            bookNumber: Number(element.dataset.book),
            chapter: Number(element.dataset.chapter),
            verse: Number(element.dataset.verse),
            text: getCleanVerseTextForCopy(element),
        }))
        .filter((verse) => verse.bookNumber && verse.chapter && verse.verse && verse.text);

    if (!selectedVerses.length) {
        return includeRawFallback ? selected.toString().trim() || null : null;
    }

    const firstVerse = selectedVerses[0];
    const lastVerse = selectedVerses[selectedVerses.length - 1];
    const bookName = bibleStore.getBook(firstVerse.bookNumber).title;
    const reference =
        firstVerse.verse === lastVerse.verse
            ? `${bookName} ${firstVerse.chapter}:${firstVerse.verse}`
            : `${bookName} ${firstVerse.chapter}:${firstVerse.verse}-${lastVerse.verse}`;

    return `"${selectedVerses.map((verse) => verse.text).join('\n')}"\n${reference}`;
}

function copyTextThroughCopyEvent(text: string) {
    forcedPassageCopyText = text;

    const copyTarget = document.createElement('textarea');
    copyTarget.value = text;
    copyTarget.setAttribute('readonly', 'true');
    copyTarget.style.position = 'fixed';
    copyTarget.style.opacity = '0';
    copyTarget.style.pointerEvents = 'none';
    copyTarget.style.top = '-9999px';

    document.body.appendChild(copyTarget);
    copyTarget.focus();
    copyTarget.select();

    let copied = false;
    try {
        copied = document.execCommand('copy');
    } finally {
        document.body.removeChild(copyTarget);
        forcedPassageCopyText = null;
    }

    return copied;
}

const copyText = () => {
    const text = selectedPassageTextForCopy.value ?? getSelectedPassageTextForCopy();
    if (!text) return;

    if (copyTextThroughCopyEvent(text)) {
        message.success('Copied to clipboard');
        showPopOver.value = false;
        return;
    }

    message.error('Unable to copy selected verses');
};

function copySelectedPassageWithReference(event: ClipboardEvent) {
    const text = forcedPassageCopyText ?? getSelectedPassageTextForCopy(false);
    if (!text || !event.clipboardData) return;

    event.clipboardData.setData('text/plain', text);
    event.preventDefault();
}

function setActiveVerseFromElement(event: Event): void {
    const el = (event.currentTarget as HTMLElement | null)?.closest<HTMLElement>('[data-verse]');
    if (!el) return;

    const verse = parseInt(el.dataset.verse || '0');
    if (verse) {
        bibleStore.setActiveVerse(verse);
    }
}

function deleteClipNote(args: { book_number: number; chapter: number; verse: number }) {
    dialog.warning({
        title: t('Confirm'),
        content: t(
            'Are You Sure You want to remove? If you delete this clip note, you will not be able to undo it!',
        ),
        positiveText: t('Yes'),
        negativeText: t('No'),
        onPositiveClick: async () => {
            await clipNoteStore.deleteClipNote(args);
            await clipNoteStore.getChapterClipNotes(args.book_number, args.chapter);
        },
    });
}

onBeforeMount(() => {
    const savedFontSize = SESSION.get(fontSizeOfShowChapter);
    if (savedFontSize) fontSize.value = savedFontSize;
    initSplitSizes();
});

onMounted(() => {
    piperStore.checkInstalled();
    loadSystemFonts();
    restoreScrollPosition();

    // Scroll all panes when verse data changes (new chapter/book loaded)
    watch(
        () => bibleStore.verses,
        () => {
            scrollAllPanesToVerse(bibleStore.selectedVerse);
        },
    );

    // set initial font family
    const savedFontFamily = SESSION.get('font-family-of-show-chapter');
    if (savedFontFamily) {
        fontSelected.value = savedFontFamily;
        document.documentElement.style.setProperty('--bible-font-family', savedFontFamily);
    }

    const container = document.getElementById('view-verses-container');

    // click outside to close popover
    document.addEventListener('click', function (e) {
        if (!container?.contains(e.target as any)) {
            showPopOver.value = false;
        }
    });

    // text selection popover (delegated on the container)
    container?.addEventListener('mouseup', (e) => {
        let selection = document.getSelection();
        let selectedText = selection?.toString();

        const parentElement = getSelectionParentElement('view-verse-rendered-clip-note');
        if (parentElement) {
            showPopOver.value = false;
            return;
        }

        if (!selectedText) {
            selectedPassageTextForCopy.value = null;
            showPopOver.value = false;
        } else {
            selectedPassageTextForCopy.value = getSelectedPassageTextForCopy(false);
            contextMenuPositionX.value = e.pageX;
            contextMenuPositionY.value = e.pageY - 20;
            showPopOver.value = true;
        }
    });

    container?.addEventListener('dragstart', (event) => {
        event.preventDefault();
    });

    verseCopyListener = copySelectedPassageWithReference;
    document.addEventListener('copy', verseCopyListener);

    // Ctrl+scroll to change font size (works across all panes)
    container?.addEventListener('wheel', (event) => {
        if (event.ctrlKey) {
            if (event.deltaY > 0) {
                if (fontSize.value <= 10) return;
                fontSize.value--;
            } else if (event.deltaY < 0) {
                fontSize.value++;
            }
            event.preventDefault();
        }
    });
});

onUnmounted(() => {
    if (verseCopyListener) {
        document.removeEventListener('copy', verseCopyListener);
    }
});
</script>
<template>
    <div class="w-full h-full show-chapter-verses flex flex-col read-bible-verses-panel">
        <div
            class="dark:bg-dark-400 flex items-center py-6px select-none px-10px read-bible-verses-toolbar overflow-x-auto overflow-y-hidden scrollbar-thin"
        >
            <div class="flex-shrink-0">
                <div
                    class="flex items-center hover:text-[var(--primary-color)] cursor-pointer whitespace-nowrap"
                    @click="navigateChapter('before')"
                >
                    <NIcon :component="FastForward20Regular" size="20" class="rotate-180" />
                    <span>{{ $t('Before') }}</span>
                </div>
            </div>
            <div class="flex items-center gap-5px flex-1 min-w-0 mx-8px justify-center">
                <div
                    class="flex items-center gap-5px flex-shrink-0"
                    style="width: clamp(100px, 20%, 200px)"
                >
                    <NSlider v-model:value="fontSize" :max="35" :min="10" class="flex-1" />
                    <span class="text-xs flex-shrink-0">{{ fontSize }}</span>
                </div>
                <div class="flex-shrink-0" style="width: clamp(100px, 25%, 250px)">
                    <NSelect
                        v-model:value="fontSelected"
                        :options="fontOptions"
                        size="small"
                        filterable
                        :virtual-scroll="false"
                        :render-label="
                            (option: any) =>
                                h(
                                    'span',
                                    { style: `font-family: '${option.value}'` },
                                    option.label as string,
                                )
                        "
                    />
                </div>
                <VerseSelector circle>
                    <NIcon
                        size="25"
                        :component="themeStore.isDark ? SlideSearch28Filled : SlideSearch28Regular"
                    />
                </VerseSelector>
                <NButton
                    size="small"
                    quaternary
                    circle
                    class="flex-shrink-0"
                    :title="
                        noteStore.showNote
                            ? 'Hide Notes (Ctrl+Shift+N)'
                            : 'Open Notes (Ctrl+Shift+N)'
                    "
                    @click="noteStore.showNote = !noteStore.showNote"
                >
                    <template #icon>
                        <NIcon
                            :component="noteStore.showNote ? Note28Filled : Note24Regular"
                            size="20"
                        />
                    </template>
                </NButton>
                <NButton
                    size="small"
                    quaternary
                    class="flex-shrink-0 mr-4px"
                    title="Open as Flipbook"
                    @click="flipbookStore.openVersionSelect()"
                >
                    <template #icon>
                        <Icon icon="mdi:book-open-page-variant" style="font-size: 24px" />
                    </template>
                </NButton>
                <NButton
                    size="small"
                    quaternary
                    class="flex-shrink-0"
                    :title="voiceReaderLabel + ' — Click to change'"
                    @click="
                        mainStore.settingsTab = 'VerseReader';
                        mainStore.showSettings = true;
                    "
                >
                    <template #icon>
                        <Icon icon="mdi:account-voice" style="font-size: 24px" />
                    </template>
                    <span class="text-xs whitespace-nowrap">{{ voiceReaderLabel }}</span>
                </NButton>
                <NButton
                    v-if="settingStore.verseReaderMode === 'piper-tts' && piperStore.isInstalled"
                    size="small"
                    quaternary
                    class="flex-shrink-0"
                    title="Voice Models"
                    @click="showPiperModels = true"
                >
                    <template #icon>
                        <Icon icon="mdi:account-voice" style="font-size: 18px" />
                    </template>
                    <span class="text-xs whitespace-nowrap">{{ piperVoiceLabel }}</span>
                </NButton>
                <NButton
                    v-if="bibleStore.selectedBibleVersions.length < 6"
                    size="small"
                    quaternary
                    class="flex-shrink-0"
                    title="Add Split View"
                    @click="addSplit"
                >
                    <template #icon>
                        <Icon icon="mdi:book-plus" style="font-size: 22px" />
                    </template>
                </NButton>
            </div>
            <div class="flex-shrink-0">
                <div
                    class="flex items-center hover:text-[var(--primary-color)] cursor-pointer whitespace-nowrap"
                    @click="navigateChapter('next')"
                >
                    <span>{{ $t('Next') }}</span>
                    <NIcon :component="FastForward20Regular" size="20" />
                </div>
            </div>
        </div>
        <div
            id="view-verses-container"
            class="w-full flex-1 min-h-0"
        >
            <Splitpanes
                class="h-full split-view-panes"
                :dbl-click-splitter="false"
                @resized="onSplitResized"
            >
                <Pane
                    v-for="(versionFile, paneIndex) in bibleStore.selectedBibleVersions.slice(0, 6)"
                    :key="versionFile"
                    :size="splitPaneSizes[paneIndex] ?? (100 / bibleStore.selectedBibleVersions.length)"
                >
                    <div class="h-full flex flex-col">
                        <!-- Pane header: version selector -->
                        <div class="flex items-center gap-4px px-6px py-4px dark:bg-dark-400 bg-gray-100 border-b border-gray-200 dark:border-dark-200 select-none split-pane-header">
                            <NSelect
                                :value="versionFile"
                                :options="versionOptionsForPane(paneIndex)"
                                size="small"
                                filterable
                                :virtual-scroll="false"
                                to="body"
                                @update:value="(v: string) => changeVersion(paneIndex, v)"
                            />
                            <NButton
                                v-if="bibleStore.selectedBibleVersions.length > 1"
                                size="tiny"
                                quaternary
                                circle
                                title="Remove split"
                                @click="removeSplit(paneIndex)"
                            >
                                <template #icon>
                                    <NIcon size="14"><Close /></NIcon>
                                </template>
                            </NButton>
                        </div>
                        <!-- Scrollable verse list for this pane -->
                        <div
                            :ref="(el) => setScrollPaneRef(paneIndex, el)"
                            class="flex-1 min-h-0 scroll-bar-md flex flex-col gap-5px overflow-y-auto overflowing-div pb-20px"
                            @mouseenter="onPaneMouseEnter(paneIndex)"
                            @scroll="syncScroll(paneIndex)"
                        >
                            <template v-if="showVerseSkeletons">
                                <div
                                    v-for="row in verseSkeletonRows"
                                    :key="`verse-skeleton-${paneIndex}-${row}`"
                                    class="mx-10px verse-loading-skeleton"
                                    aria-hidden="true"
                                >
                                    <div class="verse-loading-number"></div>
                                    <div class="verse-loading-content">
                                        <div class="verse-loading-line w-92"></div>
                                        <div class="verse-loading-line w-76"></div>
                                        <div class="verse-loading-line w-58"></div>
                                    </div>
                                </div>
                            </template>
                            <template v-else-if="!paneHasVisibleVerses(paneIndex)">
                                <div
                                    class="mx-10px mt-16px rounded border px-12px py-10px text-size-13px"
                                    style="border-color: rgba(245, 158, 11, 0.35); background: rgba(245, 158, 11, 0.12); color: #f59e0b;"
                                >
                                    This Bible version does not contain
                                    {{ bibleStore.selectedBook.title }} {{ bibleStore.selectedChapter }}.
                                </div>
                            </template>
                            <template v-else>
                                <div
                                    v-for="(verse, verseIndex) in bibleStore.renderVerses"
                                    :key="verse.verse"
                                    class="flex flex-col w-full mx-auto"
                                >
                                <div class="mx-10px">
                                    <div
                                        :class="{
                                            'rounded-t-md': clipNoteRender(
                                                `${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                            ),
                                            'dark:bg-light-50 dark:bg-opacity-10 bg-gray-600 bg-opacity-10':
                                                bibleStore.selectedVerse === verse.verse,
                                            'the-selected-verse':
                                                bibleStore.selectedVerse === verse.verse,
                                        }"
                                        :data-book="verse.book_number"
                                        :data-chapter="verse.chapter"
                                        :data-verse="verse.verse"
                                        :id="
                                            paneIndex === 0 && bibleStore.selectedVerse === verse.verse
                                                ? 'the-selected-verse'
                                                : undefined
                                        "
                                        :style="[
                                            `border: 1px solid ${clipNoteRender(`${verse.book_number}_${verse.chapter}_${verse.verse}`).color}`,
                                            bibleStore.selectedVerse === verse.verse ? 'border-left: 1px solid var(--primary-color)' : '',
                                        ]"
                                        class="group flex items-start dark:hover:bg-light-50 dark:hover:bg-opacity-10 hover:bg-gray-600 hover:bg-opacity-10 px-8px py-2 relative transition-colors duration-150"
                                    >
                                        <div
                                            v-if="!verse.version[paneIndex].missing"
                                            class="w-full"
                                            :class="{
                                                'context-menu-active-verse':
                                                    contextMenuVerseKey === verse.version[paneIndex].key,
                                            }"
                                            @contextmenu="clickContextMenu({ ...verse, key: verse.version[paneIndex].key })"
                                        >
                                            <div :style="`font-size:${fontSize}px`">
                                                <span
                                                    class="font-bold select-none italic the-verse-number"
                                                >
                                                    {{ verse.verse }}.
                                                </span>
                                                <!-- TTS play/indicator -->
                                                <Icon
                                                    v-if="
                                                        activeStore().activeVerseNumber === verse.verse &&
                                                        paneIndex === activeStore().selectedVersionIndex
                                                    "
                                                    icon="mdi:account-voice"
                                                    :style="`font-size: ${fontSize}px; vertical-align: middle;`"
                                                    class="text-[var(--primary-color)] animate-pulse mx-5px"
                                                    title="Reading this verse"
                                                />
                                                <NButton
                                                    v-else-if="
                                                        activeStore().activeVerseNumber !== verse.verse
                                                    "
                                                    size="tiny"
                                                    quaternary
                                                    circle
                                                    class="opacity-0 group-hover:opacity-100 transition-opacity"
                                                    style="vertical-align: middle; margin: 0 1px"
                                                    title="Read from this verse"
                                                    @click.stop="
                                                        playVerse(verseIndex, paneIndex)
                                                    "
                                                >
                                                    <Icon
                                                        icon="mdi:play"
                                                        :style="`font-size: ${fontSize - 3}px;`"
                                                    />
                                                </NButton>
                                                <span
                                                    :data-bible-version="verse.version[paneIndex].version"
                                                    :data-book="verse.book_number"
                                                    :data-chapter="verse.chapter"
                                                    :data-key="verse.version[paneIndex].key"
                                                    :data-verse="verse.verse"
                                                    class="verse-select-text input-text-search"
                                                    v-html="verse.version[paneIndex].text"
                                                    @mousedown="setActiveVerseFromElement"
                                                    @mouseover="handleFootnoteHover($event, verse.version[paneIndex], verse)"
                                                    @mouseleave="footnotePopover.show = false"
                                                ></span>
                                                <NIcon
                                                    v-if="bookmarkStore.isBookmarkExists(`${verse.book_number}_${verse.chapter}_${verse.verse}`)"
                                                    size="16"
                                                    class="text-[var(--primary-color)] ml-4px"
                                                    style="vertical-align: middle; display: inline-flex;"
                                                    title="Bookmarked"
                                                >
                                                    <BookmarkFilled />
                                                </NIcon>
                                            </div>
                                        </div>
                                    </div>
                                    <!-- Clip notes -->
                                    <div
                                        v-if="
                                            clipNoteRender(
                                                `${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                            )
                                        "
                                        :style="`background: ${
                                            clipNoteRender(
                                                `${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                            ).color
                                        }`"
                                        class="prose-mirror-render-html relative text-dark-900 rounded-b-md mb-3"
                                    >
                                        <NIcon
                                            class="absolute -top-16px left-1 transform rotate-45 dark:text-gray-600"
                                            size="30"
                                        >
                                            <Attachment />
                                        </NIcon>
                                        <div class="absolute flex gap-2 -top-5 right-3">
                                            <NButton
                                                class="shadow-md"
                                                :style="`background: ${
                                                    clipNoteRender(
                                                        `${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                                    ).color
                                                }`"
                                                size="small"
                                                @click="
                                                    createClipNoteRef &&
                                                    createClipNoteRef.toggleClipNoteModal(
                                                        clipNoteRender(
                                                            `${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                                        ),
                                                    )
                                                "
                                                title="Edit"
                                            >
                                                <NIcon class="text-dark-9">
                                                    <Edit />
                                                </NIcon>
                                            </NButton>
                                            <NButton
                                                class="shadow-md"
                                                :style="`background: ${
                                                    clipNoteRender(
                                                        `${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                                    ).color
                                                }`"
                                                size="small"
                                                @click="
                                                    deleteClipNote({
                                                        book_number: verse.book_number,
                                                        chapter: verse.chapter,
                                                        verse: verse.verse,
                                                    })
                                                "
                                                title="Delete"
                                            >
                                                <NIcon class="text-dark-9">
                                                    <Delete />
                                                </NIcon>
                                            </NButton>
                                        </div>
                                        <div
                                            :style="`font-size:${fontSize - 1}px`"
                                            class="px-10px pb-1 view-verse-rendered-clip-note"
                                            v-html="
                                                clipNoteRender(
                                                    `${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                                ).content
                                            "
                                        ></div>
                                    </div>
                                </div>
                                </div>
                            </template>
                        </div>
                    </div>
                </Pane>
            </Splitpanes>
        </div>
        <ContextMenu
            :data="contextMenuData"
            :show-context-menu="showContextMenu"
            :x="contextMenuPositionX"
            :y="contextMenuPositionY"
            @close="showContextMenu = false"
            @create-clip-note="
                (data) => (createClipNoteRef ? createClipNoteRef.toggleClipNoteModal(data) : false)
            "
        />
        <NPopover
            :show="showPopOver"
            :x="contextMenuPositionX"
            :y="contextMenuPositionY"
            trigger="click"
        >
            <div id="buttons" class="flex items-center gap-10px">
                <NButton
                    round
                    size="small"
                    secondary
                    title="Copy"
                    @mousedown.prevent
                    @click="copyText"
                >
                    <template #icon>
                        <NIcon>
                            <Copy />
                        </NIcon>
                    </template>
                    {{ $t('copy') }}
                </NButton>
            </div>
        </NPopover>
        <CreateClipNoteVue ref="createClipNoteRef" />
        <PiperModelsModal v-model:show="showPiperModels" />
        <FootnotePopover
            :show="footnotePopover.show"
            :x="footnotePopover.x"
            :y="footnotePopover.y"
            :marker="footnotePopover.marker"
            :text="footnotePopover.text"
            :font-size="fontSize"
        />
    </div>
</template>
<style lang="scss" src="./ViewVersesStyle.scss"></style>
