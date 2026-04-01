<script lang="ts" setup>
import { onBeforeMount, onMounted, ref, watch, h, computed } from 'vue';
import { useBibleStore } from '../../../store/BibleStore';
import { NButton, NIcon, NPopover, NSelect, NSlider, useDialog, useMessage } from 'naive-ui';
import { Attachment, BookmarkFilled, Copy, Delete, Edit } from '@vicons/carbon';
import SESSION from '../../../util/session';
import { useMouse } from '@vueuse/core';
import ContextMenu from './ContextMenu/ContextMenu.vue';
import { useBookmarkStore } from '../../../store/bookmark';
import HighlightOptions from './../../../components/HighlightOptions/HighlightOptions.vue';
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

const { t } = useI18n();
const showPiperModels = ref(false);

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

function activeStore() {
    return settingStore.verseReaderMode === 'piper-tts' ? piperStore : ttsStore;
}

function playVerse(verseIndex: number, versionIndex: number) {
    switch (settingStore.verseReaderMode) {
        case 'piper-tts':
            if (!piperStore.isInstalled) {
                dialog.warning({
                    title: 'Piper Not Installed',
                    content: 'Piper Neural TTS needs to be downloaded before use. Go to Settings → Verse Reader to install it.',
                    positiveText: 'Open Settings',
                    negativeText: 'Cancel',
                    onPositiveClick: () => { mainStore.settingsTab = 'VerseReader'; mainStore.showSettings = true; },
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
    const footnoteEl = target.tagName.toLowerCase() === 'f'
        ? target
        : (target.closest?.('f') as HTMLElement | null);

    if (!footnoteEl) {
        footnotePopover.value.show = false;
        return;
    }

    const marker = footnoteEl.textContent?.trim() ?? '';
    if (!marker) return;

    const footnotes: Array<{ marker: string; text: string }> = await (window as any).browserWindow.getCommentaryForVerse(
        JSON.stringify({
            version: version.version,
            book_number: verse.book_number,
            chapter: verse.chapter,
            verse: verse.verse,
        })
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
    }
);

watch(
    () => fontSize.value,
    (FSize: number) => {
        SESSION.set(fontSizeOfShowChapter, FSize);
    }
);

// Stop TTS when the chapter or book changes — unless TTS itself triggered the chapter advance
watch(
    () => [bibleStore.selectedChapter, bibleStore.selectedBookNumber],
    () => { const s = activeStore(); if (s.isActive && !s.autoAdvancing) s.stop(); }
);

async function navigateChapter(action: 'next' | 'before') {
    if (action == 'before' && bibleStore.selectedChapter == 1) return;
    if (action == 'next' && bibleStore.selectedChapter == bibleStore.selectedBook.chapter_count)
        return;

    await bibleStore.selectChapter(
        action == 'next' ? bibleStore.selectedChapter + 1 : bibleStore.selectedChapter - 1
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
            'Are You Sure You want to remove? If you delete this clip note, you will not be able to undo it!'
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
});

onMounted(() => {
    piperStore.checkInstalled();
    loadSystemFonts();

    // set initial font family
    const savedFontFamily = SESSION.get('font-family-of-show-chapter');
    if (savedFontFamily) {
        fontSelected.value = savedFontFamily;
        document.documentElement.style.setProperty('--bible-font-family', savedFontFamily);
    }

    // click outside to close popover
    document.addEventListener('click', function (e) {
        let verseView = document.getElementById('view-verses-container');
        if (!verseView?.contains(e.target as any)) {
            showPopOver.value = false;
        }
    });
    document.getElementById('view-verses-container')?.addEventListener('mouseup', (e) => {
        let selection = document.getSelection();
        let selectedText = selection?.toString();

        // check if this selected is highlightable
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

    document.getElementById('view-verses-container')?.addEventListener('dragstart', (event) => {
        event.preventDefault();
    });
    const scrollArea = document.getElementById('view-verses-container');

    scrollArea?.addEventListener('wheel', (event) => {
        if (event.ctrlKey) {
            if (event.deltaY > 0) {
                // Ctrl + Scroll Down
                if (fontSize.value <= 10) return;

                fontSize.value--;
                // Do something else you want
            } else if (event.deltaY < 0) {
                // Ctrl + Scroll Up
                fontSize.value++;
                // Do something else you want
            }
            // Prevent the default scroll behavior when Ctrl is pressed
            event.preventDefault();
        }
    });
});
</script>
<template>
    <div class="w-full h-full show-chapter-verses flex flex-col read-bible-verses-panel">
        <div class="h-30px dark:bg-dark-400 flex items-center pb-10px pt-10px select-none px-10px read-bible-verses-toolbar">
            <div>
                <div
                    class="flex items-center hover:text-[var(--primary-color)] cursor-pointer"
                    @click="navigateChapter('before')"
                >
                    <NIcon :component="FastForward20Regular" size="20" class="rotate-180" />
                    <span>{{ $t('Before') }}</span>
                </div>
            </div>
            <div class="flex justify-center items-center gap-5px w-full">
                <div class="flex justify-center items-center gap-5px w-full max-w-200px">
                    <NSlider v-model:value="fontSize" :max="35" :min="10" class="max-w-150px" />
                    {{ fontSize }}
                </div>
                <div class="w-100% max-w-250px">
                    <NSelect
                        v-model:value="fontSelected"
                        :options="fontOptions"
                        size="small"
                        filterable
                        :virtual-scroll="false"
                        :render-label="(option: any) => h('span', { style: `font-family: '${option.value}'` }, option.label as string)"
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
                    :title="noteStore.showNote ? 'Hide Notes (Ctrl+Shift+N)' : 'Open Notes (Ctrl+Shift+N)'"
                    @click="noteStore.showNote = !noteStore.showNote"
                >
                    <template #icon>
                        <NIcon :component="noteStore.showNote ? Note28Filled : Note24Regular" size="20" />
                    </template>
                </NButton>
                <NButton
                    v-if="settingStore.verseReaderMode === 'piper-tts' && piperStore.isInstalled"
                    size="small"
                    quaternary
                    title="Voice Models"
                    @click="showPiperModels = true"
                >
                    <template #icon>
                        <Icon icon="mdi:account-voice" style="font-size: 18px;" />
                    </template>
                    <span class="text-xs">{{ piperVoiceLabel }}</span>
                </NButton>
            </div>
            <div>
                <div
                    class="flex items-center hover:text-[var(--primary-color)] cursor-pointer"
                    @click="navigateChapter('next')"
                >
                    <span>{{ $t('Next') }}</span>
                    <NIcon :component="FastForward20Regular" size="20" />
                </div>
            </div>
        </div>
        <div
            id="view-verses-container"
            class="w-full flex-1 min-h-0 scroll-bar-md flex flex-col gap-5px overflow-y-auto overflowing-div pb-20px"
        >
            <div
                v-if="
                    bibleStore.renderVerses[0] &&
                    bibleStore.renderVerses[0].version &&
                    bibleStore.renderVerses[0].version.length <= 3
                "
                class="sticky top-0 flex w-full mx-auto gap-20 dark:bg-dark-400 bg-white z-9 py-2 read-bible-version-sticky"
            >
                <div
                    v-for="version in bibleStore.renderVerses[0].version"
                    :key="version.key"
                    class="w-full text-center"
                >
                    <div
                        class="opacity-80 dark:opacity-80 text-[var(--primary-color)] select-none font-700"
                    >
                        {{ version.version.replace('.SQLite3', '') }}
                    </div>
                </div>
            </div>
            <div
                v-for="(verse, verseIndex) in bibleStore.renderVerses"
                :key="verse.verse"
                class="flex flex-col w-full max-w-1200px mx-auto"
            >
                <div class="mx-10px">
                    <div
                        :id="verse.verse == bibleStore.selectedVerse ? 'the-selected-verse' : ''"
                        :class="{
                            'dark:bg-opacity-5 dark:bg-light-100':
                                verse.verse == bibleStore.selectedVerse,
                            'rounded-t-md': clipNoteRender(
                                `key_${verse.book_number}_${verse.chapter}_${verse.verse}`
                            ),
                        }"
                        :data-book="verse.book_number"
                        :data-chapter="verse.chapter"
                        :data-verse="verse.verse"
                        :style="`border: 1px solid ${
                            clipNoteRender(
                                `key_${verse.book_number}_${verse.chapter}_${verse.verse}`
                            ).color
                        }`"
                        class="group flex items-center gap-3 dark:hover:bg-light-50 dark:hover:bg-opacity-10 hover:bg-gray-600 hover:bg-opacity-10 px-10px py-2 relative"
                        @click="
                            bibleStore.selectVerse(verse.book_number, verse.chapter, verse.verse)
                        "
                    >
                        <div
                            :class="{ '!h-full': verse.verse == bibleStore.selectedVerse }"
                            class="h-0 w-5px bg-[var(--primary-color)] absolute left-[-5px] top-0 opacity-60 transition-all"
                            title="Selected Verse"
                        ></div>
                        <div class="flex flex-col items-center gap-2 min-w-8">
                            <div v-show="verse.version.length > 3" class="flex flex-col items-center gap-1">
                                <span
                                    class="font-700 select-none text-size-30px opacity-60 dark:opacity-70"
                                >
                                    {{ verse.verse }}
                                </span>
                                <!-- TTS: speaking indicator (>3 versions, beside large verse number) -->
                                <Icon
                                    v-if="activeStore().activeVerseNumber === verse.verse"
                                    icon="mdi:account-voice"
                                    style="font-size: 20px;"
                                    class="text-[var(--primary-color)] animate-pulse"
                                    title="Reading this verse"
                                />
                                <NButton
                                    v-else
                                    size="tiny"
                                    quaternary
                                    circle
                                    class="opacity-0 group-hover:opacity-100 transition-opacity"
                                    title="Read from this verse"
                                    @click.stop="playVerse(verseIndex, 0)"
                                >
                                    <Icon icon="mdi:play" style="font-size: 14px;" />
                                </NButton>
                            </div>
                            <div
                                v-show="
                                    bookmarkStore.isBookmarkExists(
                                        `${verse.book_number}_${verse.chapter}_${verse.verse}`
                                    )
                                "
                                title="This is Bookmarked"
                            >
                                <NIcon size="20">
                                    <BookmarkFilled />
                                </NIcon>
                            </div>
                        </div>
                        <div
                            class="flex flex-row gap-3 w-full"
                            :class="{ '!flex-col': bibleStore.selectedBibleVersions.length > 3 }"
                        >
                            <div
                                v-for="(version, versionIndex) in verse.version"
                                :key="version.key"
                                :style="`width: calc(100%/${
                                    bibleStore.selectedBibleVersions.length > 3
                                        ? 1
                                        : bibleStore.selectedBibleVersions.length
                                });`"
                                :class="{ 'context-menu-active-verse': contextMenuVerseKey === version.key }"
                                @contextmenu="clickContextMenu({ ...verse, key: version.key })"
                            >
                                <div
                                    v-if="bibleStore.selectedBibleVersions.length > 3"
                                    class="font-700 opacity-80 dark:opacity-80 mr-10px text-[var(--primary-color)] select-none"
                                    :style="`font-size: ${fontSize - 2}px`"
                                >
                                    {{ version.version.replace('.SQLite3', '') }}
                                </div>
                                <div :style="`font-size:${fontSize}px`">
                                    <span
                                        v-show="verse.version.length <= 3"
                                        class="font-bold select-none italic the-verse-number"
                                    >
                                        {{ verse.verse }}.
                                    </span>
                                    <!-- TTS: inline beside verse number (≤3 versions) -->
                                    <template v-if="verse.version.length <= 3">
                                        <!-- Speaking icon: only in the column that is being played -->
                                        <Icon
                                            v-if="activeStore().activeVerseNumber === verse.verse && versionIndex === activeStore().selectedVersionIndex"
                                            icon="mdi:account-voice"
                                            :style="`font-size: ${fontSize}px; vertical-align: middle;`"
                                            class="text-[var(--primary-color)] animate-pulse mx-5px"
                                            title="Reading this verse"
                                        />
                                        <!-- Play button: in every column on hover, but hidden when speaking -->
                                        <NButton
                                            v-else-if="activeStore().activeVerseNumber !== verse.verse"
                                            size="tiny"
                                            quaternary
                                            circle
                                            class="opacity-0 group-hover:opacity-100 transition-opacity"
                                            style="vertical-align: middle; margin: 0 1px;"
                                            title="Read from this verse"
                                            @click.stop="playVerse(verseIndex, versionIndex as number)"
                                        >
                                            <Icon icon="mdi:play" :style="`font-size: ${fontSize - 3}px;`" />
                                        </NButton>
                                    </template>
                                    <span
                                        :data-bible-version="version.version"
                                        :data-book="verse.book_number"
                                        :data-chapter="verse.chapter"
                                        :data-key="version.key"
                                        :data-verse="verse.verse"
                                        :onfocus="checkHere"
                                        class="verse-select-text input-text-search"
                                        contenteditable="true"
                                        spellcheck="false"
                                        v-html="version.text"
                                        @mouseover="handleFootnoteHover($event, version, verse)"
                                        @mouseleave="footnotePopover.show = false"
                                    ></span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div
                        v-if="
                            clipNoteRender(
                                `key_${verse.book_number}_${verse.chapter}_${verse.verse}`
                            )
                        "
                        :style="`background: ${
                            clipNoteRender(
                                `key_${verse.book_number}_${verse.chapter}_${verse.verse}`
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
                                        `key_${verse.book_number}_${verse.chapter}_${verse.verse}`
                                    ).color
                                }`"
                                size="small"
                                @click="
                                    createClipNoteRef &&
                                        createClipNoteRef.toggleClipNoteModal(
                                            clipNoteRender(
                                                `key_${verse.book_number}_${verse.chapter}_${verse.verse}`
                                            )
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
                                        `key_${verse.book_number}_${verse.chapter}_${verse.verse}`
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
                                    `key_${verse.book_number}_${verse.chapter}_${verse.verse}`
                                ).content
                            "
                        ></div>
                    </div>
                </div>
            </div>
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
                <HighlightOptions @setHighlight="showPopOver = false" />
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
