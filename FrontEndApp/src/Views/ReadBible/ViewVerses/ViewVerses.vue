<script lang="ts" setup>
import { onBeforeMount, onMounted, ref, watch } from 'vue';
import { useBibleStore } from '../../../store/BibleStore';
import { NButton, NIcon, NPopover, NSlider, useDialog, useMessage } from 'naive-ui';
import { Attachment, BookmarkFilled, ChevronLeft, ChevronRight, Close, Copy, Delete, Edit, SearchLocate } from '@vicons/carbon';
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
import { FastForward20Regular } from '@vicons/fluent';
import { SlideSearch28Filled } from "@vicons/fluent"

const { t } = useI18n();

const dialog = useDialog();
const clipNoteStore = useClipNoteStore();
const fontSizeOfShowChapter = 'font-size-of-show-chapter';
const bibleStore = useBibleStore();
const fontSize = ref(15);
const showContextMenu = ref(false);
const contextMenuPositionX = ref<number>(0);
const contextMenuPositionY = ref<number>(0);
const contextMenuData = ref({});
const bookmarkStore = useBookmarkStore();
const showPopOver = ref(false);
const { x, y } = useMouse();
const message = useMessage();
const createClipNoteRef = ref<null | { toggleClipNoteModal: Function }>(null);
const clipNoteRender: any = (key: any) => {
    return (clipNoteStore.chapterClipNotes as any)[key] ? (clipNoteStore.chapterClipNotes as any)[key] : false;
};

watch(
    () => fontSize.value,
    (FSize: number) => {
        SESSION.set(fontSizeOfShowChapter, FSize);
    }
);

function navigateChapter(action: 'next' | 'before') {
    if (action == 'before' && bibleStore.selectedChapter == 1) return;
    if (action == 'next' && bibleStore.selectedChapter == bibleStore.selectedBook.chapter_count) return;

    bibleStore.selectChapter(action == 'next' ? bibleStore.selectedChapter + 1 : bibleStore.selectedChapter - 1);
}

function clickContextMenu(verse: Object) {
    contextMenuData.value = verse;
    if (showContextMenu.value) {
        showContextMenu.value = false;
    } else {
        showContextMenu.value = true;
        contextMenuPositionX.value = x.value;
        contextMenuPositionY.value = y.value;
    }
}

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
            console.log('prevent');
            event.preventDefault();
        }
    });
}

function deleteClipNote(args: { book_number: number; chapter: number; verse: number }) {
    dialog.warning({
        title: t('Confirm'),
        content: t('Are You Sure You want to remove?'),
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
    <div class="w-full h-full show-chapter-verses">
        <div class="h-30px dark:bg-dark-400 flex items-center pb-10px pt-10px select-none px-10px">
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
                <VerseSelector circle>
                    <NIcon size="25" :component="SlideSearch28Filled" />
                </VerseSelector>
            </div>
            <div>
                <div class="flex items-center hover:text-[var(--primary-color)] cursor-pointer" @click="navigateChapter('next')">
                    <span>{{ $t('Next') }}</span>
                    <NIcon :component="FastForward20Regular" size="20" />
                </div>
            </div>
        </div>
        <div
            id="view-verses-container"
            class="w-full h-[calc(100%-30px)] scroll-bar-md flex flex-col gap-5px overflow-y-auto overflowing-div"
            :class="{}"
        >
            <div
                v-if="
                    bibleStore.renderVerses[0] &&
                    bibleStore.renderVerses[0].version &&
                    bibleStore.renderVerses[0].version.length <= 3
                "
                class="sticky top-0 flex w-full mx-auto gap-20 dark:bg-dark-400 bg-white z-9 py-2"
            >
                <div v-for="version in bibleStore.renderVerses[0].version" :key="version.key" class="w-full text-center">
                    <div class="opacity-80 dark:opacity-80 text-[var(--primary-color)] select-none font-700">
                        {{ version.version.replace('.SQLite3', '') }}
                    </div>
                </div>
            </div>
            <div v-for="verse in bibleStore.renderVerses" :key="verse.verse" class="flex flex-col w-full max-w-1100px mx-auto">
                <div
                    :id="verse.verse == bibleStore.selectedVerse ? 'the-selected-verse' : ''"
                    :class="{
                        'dark:bg-opacity-5 dark:bg-light-100': verse.verse == bibleStore.selectedVerse,
                        'rounded-t-md': clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`),
                    }"
                    :data-book="verse.book_number"
                    :data-chapter="verse.chapter"
                    :data-verse="verse.verse"
                    :style="`border: 1px solid ${
                        clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`).color
                    }`"
                    class="flex items-center gap-3 dark:hover:bg-light-50 dark:hover:bg-opacity-10 hover:bg-gray-600 hover:bg-opacity-10 px-10px py-5 relative"
                    @click="bibleStore.selectVerse(verse.book_number, verse.chapter, verse.verse)"
                    @contextmenu="clickContextMenu(verse)"
                >
                    <div
                        :class="{ '!h-full': verse.verse == bibleStore.selectedVerse }"
                        class="h-0 w-5px bg-[var(--primary-color)] absolute left-[-5px] top-0 opacity-60 transition-all"
                        title="Selected Verse"
                    ></div>
                    <div class="flex flex-col items-center gap-2 min-w-8">
                        <span
                            v-show="verse.version.length > 3"
                            class="font-700 select-none text-size-30px opacity-60 dark:opacity-70"
                        >
                            {{ verse.verse }}
                        </span>
                        <div
                            v-show="bookmarkStore.isBookmarkExists(`${verse.book_number}_${verse.chapter}_${verse.verse}`)"
                            title="This is Bookmarked"
                        >
                            <NIcon size="20">
                                <BookmarkFilled />
                            </NIcon>
                        </div>
                    </div>
                    <div class="flex flex-row gap-3 w-full" :class="{ '!flex-col': verse.version.length > 3 }">
                        <div v-for="version in verse.version" :key="version.key" class="w-full">
                            <div
                                v-if="verse.version.length > 3"
                                class="font-700 opacity-80 dark:opacity-80 mr-10px text-[var(--primary-color)] select-none"
                                :style="`font-size: ${fontSize - 2}px`"
                            >
                                {{ version.version.replace('.SQLite3', '') }}
                            </div>
                            <div :style="`font-size:${fontSize}px`">
                                <span v-show="verse.version.length <= 3" class="font-bold select-none italic">
                                    {{ verse.verse }}.
                                </span>
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
                                ></span>
                            </div>
                        </div>
                    </div>
                </div>
                <div
                    v-if="clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`)"
                    :style="`background: ${clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`).color}`"
                    class="prose-mirror-render-html relative text-dark-900 rounded-b-md mb-3"
                >
                    <NIcon class="absolute -top-16px left-1 transform rotate-45 dark:text-gray-600" size="30">
                        <Attachment />
                    </NIcon>
                    <div class="absolute left-2 bottom-0 flex flex-col gap-3">
                        <NIcon
                            class="cursor-pointer opacity-50 hover:opacity-100 transition-all"
                            @click="
                                deleteClipNote({
                                    book_number: verse.book_number,
                                    chapter: verse.chapter,
                                    verse: verse.verse,
                                })
                            "
                        >
                            <Delete />
                        </NIcon>
                        <NIcon
                            class="cursor-pointer opacity-50 hover:opacity-100 transition-all"
                            @click="
                                createClipNoteRef &&
                                    createClipNoteRef.toggleClipNoteModal(
                                        clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`)
                                    )
                            "
                        >
                            <Edit />
                        </NIcon>
                    </div>
                    <div
                        :style="`font-size:${fontSize - 1}px`"
                        class="pl-55px pr-10px view-verse-rendered-clip-note"
                        v-html="clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`).content"
                    ></div>
                </div>
            </div>
        </div>
        <ContextMenu
            :data="contextMenuData"
            :show-context-menu="showContextMenu"
            :x="contextMenuPositionX"
            :y="contextMenuPositionY"
            @close="showContextMenu = false"
            @create-clip-note="(data) => (createClipNoteRef ? createClipNoteRef.toggleClipNoteModal(data) : false)"
        />
        <NPopover :show="showPopOver" :x="contextMenuPositionX" :y="contextMenuPositionY" trigger="click">
            <div id="buttons" class="flex items-center gap-10px">
                <HighlightOptions @setHighlight="showPopOver = false" />
                <NButton round size="small" strong title="Copy" @click="copyText">
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
    </div>
</template>
<style lang="scss" src="./ViewVersesStyle.scss"></style>
