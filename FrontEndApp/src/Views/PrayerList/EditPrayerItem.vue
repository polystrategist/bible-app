<script lang="ts" setup>
import { ref } from 'vue';
import { NButton, NModal, NIcon, NCard } from 'naive-ui';
import { Save } from '@vicons/carbon';
import Editor from '../../components/Editor/Editor.vue';
import { usePrayerListStore } from '../../store/prayerListStore';

const keyOfItem = ref('');
const prayerItemContent = ref('');
const prayerListStore = usePrayerListStore();
const showModal = ref(false);

const SaveEditorContent = () => {
    try {
        prayerListStore.savePrayerItem(
            {
                title: null,
                content: prayerItemContent.value,
                group: null,
                status: null,
            },
            keyOfItem.value
        );
        showModal.value = false;
    } catch (e) {
        if (e instanceof Error) console.log(e.message);
    }
};

function modalTrigger(content: string, key: string) {
    console.log(key);
    prayerItemContent.value = content;
    keyOfItem.value = key;
    showModal.value = !showModal.value;
}

defineExpose({
    modalTrigger,
});
</script>

<template>
    <NModal v-model:show="showModal">
        <NCard class="max-w-500px my-20px" size="small">
            <template #header>
                <span class="capitalize">{{ $t('edit') }}</span>
            </template>
            <Editor v-model="prayerItemContent" />

            <div class="p-10px flex flex-row justify-end gap-15px">
                <NButton class="flex-grow" type="info" @click="SaveEditorContent()">
                    <template #icon>
                        <NIcon>
                            <Save />
                        </NIcon>
                    </template>
                    <span class="capitalize"> {{ $t('save changes') }} </span>
                </NButton>
                <NButton ghost @click="showModal = false">
                    <span class="capitalize"> {{ $t('cancel') }} </span>
                </NButton>
            </div>
        </NCard>
    </NModal>
</template>
