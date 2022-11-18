<script lang="ts" setup>
import { onBeforeMount, ref, watch } from 'vue';
import { useBibleStore } from '../../../store/BibleStore';
import { NSlider, NIcon } from 'naive-ui';
import { ChevronRight, ChevronLeft } from '@vicons/carbon';
import SESSION from '../../../util/session';

const fontSizeOfShowChapter = 'font-size-of-show-chapter';
const bibleStore = useBibleStore();
const fontSize = ref(15);

watch(
    () => fontSize.value,
    (FSize: number) => {
        SESSION.set(fontSizeOfShowChapter, FSize);
    }
);

onBeforeMount(() => {
    const savedFontSize = SESSION.get(fontSizeOfShowChapter);
    if (savedFontSize) fontSize.value = savedFontSize;
});

function navigateChapter(action: 'next' | 'before') {
    if (action == 'before' && bibleStore.selectedChapter == 1) return;
    if (action == 'next' && bibleStore.selectedChapter == bibleStore.selectedBook.chapter_count) return;

    bibleStore.selectChapter(action == 'next' ? bibleStore.selectedChapter + 1 : bibleStore.selectedChapter - 1);
}
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
        <div class="w-full h-[calc(100%-30px)] overflow-y-auto overflowing-div p-3 scroll-bar-md">
            <div class="flex flex-col gap-10px" :style="`font-size:${fontSize}px`">
                <div v-for="verse in bibleStore.verses" class="flex items-center gap-3">
                    <div>
                        <span class="font-900 select-none">{{ verse.verse }}</span>
                    </div>
                    <div>
                        <div v-for="version in verse.version">
                            <span class="font-700 opacity-100 dark:opacity-80 mr-10px text-[var(--primary-color)] select-none">
                                {{ version.version.replace('.SQLite3', '') }}
                            </span>
                            <span v-html="version.text"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<style lang="scss" src="./ViewVersesStyle.scss"></style>
