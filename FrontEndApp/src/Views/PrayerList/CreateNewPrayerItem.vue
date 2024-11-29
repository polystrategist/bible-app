<script lang="ts" setup>
import { ref } from 'vue';
import { NButton, NModal, NIcon, NCard, useMessage } from 'naive-ui';
import initialContent from './initialContent';
import { Close, Add, Save } from '@vicons/carbon';
import Editor from '../../components/Editor/Editor.vue';
import { usePrayerListStore } from '../../store/prayerListStore';

const message = useMessage();
const showModal = ref(false);
const prayerContent = ref('');
const closeCreateNewModal = () => {
    showModal.value = false;
    let initialValue = initialContent;
};
const prayerListStore = usePrayerListStore();

const SaveEditorContent = () => {
    try {
        prayerListStore.savePrayerItem({
            title: null,
            content: prayerContent.value,
            group: null,
            status: 'ongoing',
        });
        showModal.value = false;
        prayerContent.value = '';
    } catch (e) {
        if (e instanceof Error) message.error(e.message);
    }
};
</script>

<template>
    <NButton @click="showModal = true" round secondary size='tiny'>
        <template #icon>
            <NIcon>
                <Add />
            </NIcon>
        </template>
        <span class="capitalize">{{ $t('new') }}</span>
    </NButton>
    <NModal :show="showModal" class="min-w-500px max-w-600px">
        <NCard class="my-20px" size="small">
            <template #header>
                <span class="capitalize">{{ $t('create') }}</span>
            </template>
            <Editor v-model="prayerContent" :button-actions="['bold', 'italic', 'underline', 'strike', 'clearFormat']" />
            <div class="p-10px flex flex-row justify-end gap-15px dark:bg-black dark:bg-opacity-10">
                <NButton ghost @click="closeCreateNewModal()">
                    <NIcon>
                        <Close />
                    </NIcon>
                    <span class="capitalize">{{ $t('close') }}</span>
                </NButton>
                <NButton type="info" @click="SaveEditorContent()">
                    <NIcon>
                        <Save />
                    </NIcon>
                    <span class="capitalize">{{ $t('create new') }}</span>
                </NButton>
            </div>
        </NCard>
    </NModal>
</template>

<style lang="scss">
.create-new-prayer-list-editor {
    @apply dark:bg-gray-800 bg-gray-200 rounded-md overflow-hidden;

    .prayer-list-button {
        @apply p-10px flex flex-row items-center;

        button {
            @apply p-7px text-size-[20px] rounded-md;

            &:hover {
                @apply dark:bg-gray-700 bg-gray-300;
            }
        }
        button.is-active {
            @apply dark:bg-gray-700 bg-gray-300;
        }
    }

    .ProseMirror {
        @apply p-10px rounded-md max-h-500px min-h-200px overflow-y-auto;
    }
}
</style>
