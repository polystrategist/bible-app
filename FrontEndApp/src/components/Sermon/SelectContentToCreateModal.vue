<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { NCard, NModal } from 'naive-ui';
import { ref } from 'vue';

const showModal = ref(false);

function toggleModal() {
    showModal.value = !showModal.value
}

defineExpose({
    toggleModal
})
</script>

<template>
    <NModal v-model:show="showModal">
        <NCard style="max-width: 600px;">
            <div class="flex gap-5 w-full">
                <div
                    class="flex justify-center items-center flex-col text-center gap-1 group dark:hover:bg-gray-6 cursor-pointer rounded-md p-2 w-full">
                    <Icon icon="material-symbols:text-fields-rounded" class="text-size-40px" />
                    <h3 class="m-0 leading-tight group-hover:underline">Text Based Sermon</h3>
                    <p class="m-0 leading-tight">Submit a sermon in text format.</p>
                </div>
                <div
                    class="flex justify-center items-center flex-col text-center gap-1 group dark:hover:bg-gray-6 cursor-pointer rounded-md p-2 w-full">
                    <Icon icon="mdi:youtube" class="text-size-40px group-hover:text-red-5" />
                    <h3 class="m-0 leading-tight group-hover:underline">Share a Youtube Content</h3>
                    <p class="m-0 leading-tight">Share a youtube video link.</p>
                </div>
            </div>
        </NCard>
    </NModal>
</template>