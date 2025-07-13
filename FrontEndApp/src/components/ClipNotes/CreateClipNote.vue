<script setup lang="ts">
import { NModal, NCard, NButton, NIcon, useMessage } from 'naive-ui';
import { Attachment } from '@vicons/carbon';
import { ref } from 'vue';
import EditorVue from '../Editor/Editor.vue';
import { useClipNoteStore } from '../../store/ClipNotes';
import { colors } from '../../util/highlighter';
import { useBibleStore } from '../../store/BibleStore';

const bibleStore = useBibleStore();
const clipNoteStore = useClipNoteStore();
const showModal = ref(false);
const verseData = ref<{
    book_number: number;
    chapter: number;
    verse: number;
} | null>(null);

const message = useMessage();
const content = ref('');
const selectedColor = ref('#FFD26A');

function toggleClipNoteModal(data: any) {
    content.value = '';
    selectedColor.value = '#FFD26A';
    if (data.content) content.value = data.content;
    if (data.color) selectedColor.value = data.color;
    verseData.value = data;
    showModal.value = true;
}

async function addClipNotes() {
    if (!content.value) {
        message.warning('Oops, Please Write Something 😊');
        return false;
    }

    await clipNoteStore
        .storeClipNote({
            book_number: verseData.value?.book_number as number,
            chapter: verseData.value?.chapter as number,
            verse: verseData.value?.verse as number,
            content: content.value as string,
            color: selectedColor.value,
        })
        .then(() => {
            content.value = '';
            verseData.value = null;
            showModal.value = false;
        });

    await clipNoteStore.getChapterClipNotes(bibleStore.selectedBookNumber, bibleStore.selectedChapter);
}

defineExpose({
    toggleClipNoteModal,
});
</script>
<template>
    <NModal :show="showModal">
        <NCard class="max-w-700px my-30px" size="small">
            <template #header>
                <div class="flex justify-between mb-4">
                    <div>
                        <NIcon class="mr-3">
                            <Attachment />
                        </NIcon>
                        <span class="text-lg">
                            {{ $t('Clip Note') }}
                        </span>
                    </div>
                    <div class="flex gap-1 items-center h-50px">
                        <span> {{ $t('Select Color') }}:</span>
                        <button v-for="color in colors" :key="color.color" @click="selectedColor = color.color"
                            :style="`background-color: ${color.color}`"
                            class="h-25px w-25px cursor-pointer rounded-full transition-all border-none" :class="{
                                'h-40px w-40px': selectedColor == color.color,
                            }"></button>
                    </div>
                </div>
            </template>
            <div>
                <EditorVue v-model="content"
                    :editorContentStyle="`background-color: ${selectedColor}; color: #000; padding: 10px; border-radius: 5px;`" />
            </div>
            <template #footer>
                <div class="flex gap-2">
                    <NButton class="w-[70%]" type="primary" @click="addClipNotes">{{ $t('Save') }}</NButton>
                    <NButton class="w-[30%]" @click="showModal = false">{{ $t('Cancel') }}</NButton>
                </div>
            </template>
        </NCard>
    </NModal>
</template>
