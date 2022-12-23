<script setup lang="ts">
import { NCard, NModal, NButton } from 'naive-ui';
import { ref } from 'vue';

const data = ref<any>(null);
const showYoutubeModal = ref(false);

function toggleModal(sermon: any) {
    showYoutubeModal.value = true;
    data.value = sermon;
}

function close() {
    showYoutubeModal.value = false;
    data.value = null;
}

defineExpose({
    toggleModal,
});
</script>
<template>
    <NModal :show="showYoutubeModal" size="small">
        <NCard class="my-20px mx-40px min-h-[90vh]">
            <template #header>
                <div class="flex justify-between items-center">
                    <span>{{ data ? data.title : '' }}</span>
                    <NButton @click="close">Close</NButton>
                </div>
            </template>
            <div class="relative w-full h-500px prose-mirror-render-html overflow-y-auto">
                <div v-if="data" class="text-content-sermon" v-html="data ? data.content : ''"></div>
            </div>
        </NCard>
    </NModal>
</template>
