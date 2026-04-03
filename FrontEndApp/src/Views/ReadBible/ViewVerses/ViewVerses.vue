<script lang="ts" setup>
import { onBeforeMount, onMounted, ref, watch, h, computed, nextTick } from 'vue';
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

function addSplit() {
    if (bibleStore.selectedBibleVersions.length >= 6) return;
    // Pick first version not already selected
    const available = moduleStore.bibleLists
        .filter((b: any) => !b.title.includes('commentaries'))
        .find((b: any) => !bibleStore.selectedBibleVersions.includes(b.file_name));
    const newVersion = available ? available.file_name : bibleStore.DefaultSelectedVersion;
    bibleStore.selectedBibleVersions.push(newVersion);
    // Distribute pane sizes evenly
    const count = bibleStore.selectedBibleVersions.length;
    splitPaneSizes.value = Array(count).fill(100 / count);
    SESSION.set(storageSplitPaneSizesKey, splitPaneSizes.value);
    bibleStore.getVerses();
}

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
const { x, y } = useMouse();

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

const copyText = () => {
    const selected = window.getSelection();
    const text: string | undefined = selected?.toString();
    if (text) {
        navigator.clipboard.writeText(text);
        message.success('Copied to clipboard');
    }
};

function checkHere(this: HTMLElement): void {
    const el = this;
    el.addEventListener('keydown', function (event: KeyboardEvent) {
        const key = event.key;
        const ctrl = event.ctrlKey;
        if (key.toUpperCase() == 'C' && ctrl) {
            const selected = window.getSelection();
            const text: string | undefined = selected?.toString();
            if (text) {
                message.info('Copied to Clipboard!');
            }
        } else {
            event.preventDefault();
        }
    });
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
            showPopOver.value = false;
        } else {
            contextMenuPositionX.value = e.pageX;
            contextMenuPositionY.value = e.pageY - 20;
            showPopOver.value = true;
        }
    });

    container?.addEventListener('dragstart', (event) => {
        event.preventDefault();
    });

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
                            <div
                                v-for="(verse, verseIndex) in bibleStore.renderVerses"
                                :key="verse.verse"
                                class="flex flex-col w-full mx-auto"
                            >
                                <div class="mx-10px">
                                    <div
                                        :class="{
                                            'rounded-t-md': clipNoteRender(
                                                `key_${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                            ),
                                        }"
                                        :data-book="verse.book_number"
                                        :data-chapter="verse.chapter"
                                        :data-verse="verse.verse"
                                        :style="`border: 1px solid ${
                                            clipNoteRender(
                                                `key_${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                            ).color
                                        }`"
                                        class="group flex items-start dark:hover:bg-light-50 dark:hover:bg-opacity-10 hover:bg-gray-600 hover:bg-opacity-10 px-8px py-2 relative"
                                    >
                                        <div
                                            v-if="verse.version[paneIndex]"
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
                                                    :onfocus="checkHere"
                                                    class="verse-select-text input-text-search"
                                                    contenteditable="true"
                                                    spellcheck="false"
                                                    v-html="verse.version[paneIndex].text"
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
                                                `key_${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                            )
                                        "
                                        :style="`background: ${
                                            clipNoteRender(
                                                `key_${verse.book_number}_${verse.chapter}_${verse.verse}`,
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
                                                        `key_${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                                    ).color
                                                }`"
                                                size="small"
                                                @click="
                                                    createClipNoteRef &&
                                                    createClipNoteRef.toggleClipNoteModal(
                                                        clipNoteRender(
                                                            `key_${verse.book_number}_${verse.chapter}_${verse.verse}`,
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
                                                        `key_${verse.book_number}_${verse.chapter}_${verse.verse}`,
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
                                                    `key_${verse.book_number}_${verse.chapter}_${verse.verse}`,
                                                ).content
                                            "
                                        ></div>
                                    </div>
                                </div>
                            </div>
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
                <NButton round size="small" secondary title="Copy" @click="copyText">
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
