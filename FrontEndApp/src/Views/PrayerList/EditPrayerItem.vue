<script lang="ts" setup>
import { ref } from 'vue';
import { NButton, NModal, NIcon, NCard, NInput, NCheckbox, useMessage } from 'naive-ui';
import { Save } from '@vicons/carbon';
import Editor from '../../components/Editor/Editor.vue';
import { usePrayerListStore } from '../../store/prayerListStore';

const keyOfItem = ref('');
const prayerTitle = ref('');
const prayerGroup = ref('');
const prayerItemContent = ref('');
const isAnswered = ref(false);
const prayerListStore = usePrayerListStore();
const showModal = ref(false);
const message = useMessage();

const SaveEditorContent = () => {
    try {
        prayerListStore.savePrayerItem(
            {
                title: prayerTitle.value.trim() || null,
                content: prayerItemContent.value,
                group: prayerGroup.value.trim() || null,
                status: isAnswered.value ? 'done' : 'ongoing',
            },
            keyOfItem.value
        );
        showModal.value = false;
    } catch (e) {
        if (e instanceof Error) message.error(e.message);
    }
};

function modalTrigger(item: {
    key: string;
    title?: string | null;
    content?: string;
    group?: string | null;
    status?: string | null;
}) {
    keyOfItem.value = item.key;
    prayerTitle.value = item.title ?? '';
    prayerGroup.value = item.group ?? '';
    prayerItemContent.value = item.content ?? '';
    isAnswered.value = item.status === 'done';
    showModal.value = true;
}

defineExpose({ modalTrigger });
</script>

<template>
    <NModal v-model:show="showModal">
        <NCard class="max-w-500px my-20px" size="small">
            <template #header>
                <span class="capitalize">{{ $t('edit') }}</span>
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
                        v-model="prayerItemContent"
                        :button-actions="['bold', 'italic', 'underline', 'strike', 'clearFormat']"
                    />
                </div>
            </div>

            <div class="p-10px flex flex-row justify-end gap-15px">
                <NButton class="flex-grow" type="info" @click="SaveEditorContent()">
                    <template #icon>
                        <NIcon><Save /></NIcon>
                    </template>
                    <span class="capitalize">{{ $t('save changes') }}</span>
                </NButton>
                <NButton ghost @click="showModal = false">
                    <span class="capitalize">{{ $t('cancel') }}</span>
                </NButton>
            </div>
        </NCard>
    </NModal>
</template>
