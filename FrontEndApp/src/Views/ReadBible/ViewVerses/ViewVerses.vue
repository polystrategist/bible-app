<script lang="ts" setup>
import { onBeforeMount, onMounted, ref, watch } from 'vue';
import { useBibleStore } from '../../../store/BibleStore';
import { NSlider, NIcon, NPopover, useMessage, NButton } from 'naive-ui';
import { ChevronRight, ChevronLeft, BookmarkFilled, Copy, Close, Attachment, Edit } from '@vicons/carbon';
import SESSION from '../../../util/session';
import { useMouse } from '@vueuse/core';
import ContextMenu from './ContextMenu/ContextMenu.vue';
import { useBookmarkStore } from '../../../store/bookmark';
import HighlightOptions from './../../../components/HighlightOptions/HighlightOptions.vue';
import CreateClipNoteVue from '../../../components/ClipNotes/CreateClipNote.vue';
import { useClipNoteStore } from '../../../store/ClipNotes';

const cliptNoteStore = useClipNoteStore();
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
const clipNoteRender = (key: any) => {
    return (cliptNoteStore.chapterClipNotes as any)[key] ? (cliptNoteStore.chapterClipNotes as any)[key] : false;
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

function cancel() {
    showPopOver.value = false;
    if (window.getSelection) {
        window.getSelection()?.removeAllRanges();
    }
}

function checkHere(this: HTMLElement): void {
    const el = this;
    el.addEventListener('keydown', function (event: KeyboardEvent) {
        var key = event.key;
        var ctrl = event.ctrlKey ? true : false;
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
});
</script>
<template>
    <div class="w-full h-full show-chapter-verses">
        <div class="h-30px dark:bg-dark-400 flex items-center px-10px select-none">
            <div>
                <div
                    class="flex items-center hover:text-[var(--primary-color)] cursor-pointer"
                    @click="navigateChapter('before')"
                >
                    <NIcon size="20" :component="ChevronLeft" />
                    <span>Before</span>
                </div>
            </div>
            <div class="flex justify-center items-center gap-5px w-full">
                <NSlider class="max-w-150px" v-model:value="fontSize" :min="10" :max="35" />
                {{ fontSize }}
            </div>
            <div>
                <div class="flex items-center hover:text-[var(--primary-color)] cursor-pointer" @click="navigateChapter('next')">
                    <span>Next</span>
                    <NIcon size="20" :component="ChevronRight" />
                </div>
            </div>
        </div>
        <div
            id="view-verses-container"
            class="w-full h-[calc(100%-30px)] overflow-y-auto overflowing-div p-3 scroll-bar-md flex flex-col gap-5px"
            :style="`font-size:${fontSize}px`"
        >
            <div v-for="verse in bibleStore.renderVerses" :key="verse.verse" class="flex flex-col">
                <div
                    class="flex items-center gap-3 dark:hover:bg-light-50 dark:hover:bg-opacity-10 hover:bg-gray-600 hover:bg-opacity-10 px-10px py-5px relative"
                    :class="{
                        'dark:bg-opacity-5 dark:bg-light-100': verse.verse == bibleStore.selectedVerse,
                        'rounded-t-md': clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`),
                    }"
                    :id="verse.verse == bibleStore.selectedVerse ? 'the-selected-verse' : ''"
                    :data-book="verse.book_number"
                    :data-chapter="verse.chapter"
                    :data-verse="verse.verse"
                    @click="bibleStore.selectVerse(verse.book_number, verse.chapter, verse.verse)"
                    @contextmenu="clickContextMenu(verse)"
                    :style="`border: 1px solid ${
                        clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`).color
                    }`"
                >
                    <div
                        class="h-0 w-5px bg-[var(--primary-color)] absolute left-[-5px] top-0 opacity-60 transition-all"
                        :class="{ '!h-full': verse.verse == bibleStore.selectedVerse }"
                        title="Selected Verse"
                    ></div>
                    <div class="flex flex-col items-center gap-2 min-w-8">
                        <span class="font-700 select-none text-size-30px opacity-60 dark:opacity-70">{{ verse.verse }}</span>
                        <div
                            v-show="bookmarkStore.isBookmarkExists(`${verse.book_number}_${verse.chapter}_${verse.verse}`)"
                            title="This is Bookmarked"
                        >
                            <NIcon size="20">
                                <BookmarkFilled />
                            </NIcon>
                        </div>
                    </div>
                    <div>
                        <div v-for="version in verse.version" :key="version.key">
                            <span class="font-700 opacity-80 dark:opacity-80 mr-10px text-[var(--primary-color)] select-none">
                                {{ version.version.replace('.SQLite3', '') }}
                            </span>
                            <span
                                v-html="version.text"
                                contenteditable="true"
                                class="verse-select-text"
                                spellcheck="false"
                                :data-key="version.key"
                                :data-bible-version="version.version"
                                :data-book="verse.book_number"
                                :data-chapter="verse.chapter"
                                :data-verse="verse.verse"
                                :onfocus="checkHere"
                            ></span>
                        </div>
                    </div>
                </div>
                <div
                    v-if="clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`)"
                    :style="`background: ${clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`).color}`"
                    class="select-none render-clip-note relative text-dark-900 rounded-b-md mb-3"
                >
                    <NIcon class="absolute -top-16px left-1 transform rotate-45 dark:text-gray-600" size="30">
                        <Attachment />
                    </NIcon>
                    <div class="absolute left-2 bottom-0">
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
                        class="pl-55px pr-10px"
                        :style="`font-size:${fontSize - 1}px`"
                        v-html="clipNoteRender(`key_${verse.book_number}_${verse.chapter}_${verse.verse}`).content"
                    ></div>
                </div>
            </div>
        </div>
        <ContextMenu
            :show-context-menu="showContextMenu"
            :x="contextMenuPositionX"
            :y="contextMenuPositionY"
            :data="contextMenuData"
            @close="showContextMenu = false"
            @create-clip-note="(data) => (createClipNoteRef ? createClipNoteRef.toggleClipNoteModal(data) : false)"
        />
        <NPopover :show="showPopOver" :x="contextMenuPositionX" :y="contextMenuPositionY" trigger="click">
            <div id="buttons" class="flex items-center gap-10px">
                <HighlightOptions @setHighlight="showPopOver = false" />
                <NButton size="small" @click="copyText" round strong title="Copy">
                    <template #icon>
                        <NIcon>
                            <Copy />
                        </NIcon>
                    </template>
                    {{ $t('copy') }}
                </NButton>
                <NButton size="small" @click="cancel" circle strong title="Copy">
                    <template #icon>
                        <NIcon>
                            <Close />
                        </NIcon>
                    </template>
                </NButton>
            </div>
        </NPopover>
        <CreateClipNoteVue ref="createClipNoteRef" />
    </div>
</template>
<style lang="scss" src="./ViewVersesStyle.scss"></style>
