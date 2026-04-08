<script lang="ts" setup>
import { ref } from 'vue';
import { NButton, NModal, NIcon, NCard, NInput, NCheckbox, useMessage } from 'naive-ui';
import { Close, Add, Save } from '@vicons/carbon';
import Editor from '../../components/Editor/Editor.vue';
import { usePrayerListStore } from '../../store/prayerListStore';

const message = useMessage();
const showModal = ref(false);
const prayerTitle = ref('');
const prayerGroup = ref('');
const prayerContent = ref('');
const isAnswered = ref(false);

const prayerListStore = usePrayerListStore();

const closeModal = () => {
    showModal.value = false;
    prayerTitle.value = '';
    prayerGroup.value = '';
    prayerContent.value = '';
    isAnswered.value = false;
};

const SaveEditorContent = () => {
    try {
        prayerListStore.savePrayerItem({
            title: prayerTitle.value.trim() || null,
            content: prayerContent.value,
            group: prayerGroup.value.trim() || null,
            status: isAnswered.value ? 'done' : 'ongoing',
        });
        closeModal();
    } catch (e) {
        if (e instanceof Error) message.error(e.message);
    }
};
</script>

<template>
    <NButton @click="showModal = true" round secondary size="tiny">
        <template #icon>
            <NIcon><Add /></NIcon>
        </template>
        <span class="capitalize">{{ $t('new') }}</span>
    </NButton>

    <NModal :show="showModal" class="min-w-500px max-w-600px">
        <NCard class="my-20px" size="small">
            <template #header>
                <span class="capitalize">{{ $t('create') }}</span>
            </template>

            <div class="flex flex-col gap-12px mb-16px">
                <div class="flex flex-col gap-4px">
                    <label class="text-12px font-600 opacity-70">Title</label>
                    <NInput v-model:value="prayerTitle" placeholder="Enter prayer title..." />
                </div>
                <div class="flex flex-col gap-4px">
                    <label class="text-12px font-600 opacity-70">Group</label>
                    <NInput v-model:value="prayerGroup" placeholder="Family, health, work..." />
                </div>
                <NCheckbox v-model:checked="isAnswered">
                    Mark as answered
                </NCheckbox>
                <div class="flex flex-col gap-4px">
                    <label class="text-12px font-600 opacity-70">Content</label>
                    <Editor
                        v-model="prayerContent"
                        :button-actions="['bold', 'italic', 'underline', 'strike', 'bulletList', 'orderedList', 'clearFormat']"
                    />
                </div>
            </div>

            <div class="p-10px flex flex-row justify-end gap-15px">
                <NButton ghost @click="closeModal()">
                    <NIcon><Close /></NIcon>
                    <span class="capitalize">{{ $t('close') }}</span>
                </NButton>
                <NButton type="info" @click="SaveEditorContent()">
                    <NIcon><Save /></NIcon>
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
