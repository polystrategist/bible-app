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
                <div class="flex justify-between">
                    <div>
                        <NIcon><Attachment /></NIcon> {{ $t('Clip Note') }}
                    </div>
                    <div class="flex gap-1 items-center">
                        <div class="w-40px h-20px rounded-md" :style="`background-color: ${selectedColor}`"></div>
                        <span> {{ $t('Select Color') }}:</span>
                        <button
                            v-for="color in colors"
                            :key="color.color"
                            @click="selectedColor = color.color"
                            :style="`background-color: ${color.color}`"
                            class="border-1 border-opacity-0 border-light-50 hover:border-[var(--primaryColor)] rounded-1 flex items-center justify-center h-30px w-30px rounded-full"
                        ></button>
                    </div>
                </div>
            </template>
            <div>
                <EditorVue v-model="content" />
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
