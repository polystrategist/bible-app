<script setup lang="ts">
import { NButton, NCard, NForm, NFormItem, NInput, NModal } from 'naive-ui';
import { ref } from 'vue';
import SpaceStudyStore from '../../store/SpaceStudyStore';

const spaceStudyStore = SpaceStudyStore();
const storeStudySpaceFormRef = ref();
const showStoreStudySpaceDialog = ref(false);
const storeStudySpaceForm = ref({
    id: 0,
    title: '',
    description: '',
});

async function submit(e: MouseEvent) {
    e.preventDefault();
    storeStudySpaceFormRef.value?.validate(async (errors: any) => {
        if (!errors) {
            const result = await spaceStudyStore.store(storeStudySpaceForm.value);
            showStoreStudySpaceDialog.value = false;
        }
    });
}

defineExpose({
    toggleModal: (data: any) => {
        if (data) storeStudySpaceForm.value = data;
        else {
            storeStudySpaceForm.value.id = 0;
            storeStudySpaceForm.value.title = '';
            storeStudySpaceForm.value.description = '';
        }
        showStoreStudySpaceDialog.value = true;
    },
});
</script>

<template>
    <NModal v-model:show="showStoreStudySpaceDialog">
        <NCard title="Create Study Space" class="max-w-450px">
            <NForm
                :model="storeStudySpaceForm"
                ref="storeStudySpaceFormRef"
                :rules="{
                    title: {
                        required: true,
                        message: 'Please input the title',
                    },
                    description: {
                        required: true,
                        message: 'Please a short or brief description for the space',
                    },
                }"
            >
                <NFormItem label="Space Title" path="title">
                    <NInput
                        v-model:value="storeStudySpaceForm.title"
                        placeholder="ex. Study about Divine love"
                    />
                </NFormItem>
                <NFormItem label="Description" path="description">
                    <NInput
                        v-model:value="storeStudySpaceForm.description"
                        type="textarea"
                        placeholder="ex. This is a study about learning and finding out what real love is in the bible."
                        class="max-h-300px"
                    />
                </NFormItem>
                <div class="flex justify-end gap-2">
                    <NButton type="primary" @click="submit">Submit</NButton>
                    <NButton @click="showStoreStudySpaceDialog = false">Cancel</NButton>
                </div>
            </NForm>
        </NCard>
    </NModal>
</template>
