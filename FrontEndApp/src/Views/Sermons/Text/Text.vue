<script setup lang="ts">
import { TextAlignJustify } from '@vicons/carbon';
import { NCard, NModal, NButton, NTag, NIcon, NDrawer, NDrawerContent } from 'naive-ui';
import { ref } from 'vue';

const data = ref<any>(null);
const showYoutubeModal = ref(false);

function toggleModal(sermon: any) {
    showYoutubeModal.value = true;
    data.value = sermon;
}

function close() {
    showYoutubeModal.value = false;
}

defineExpose({
    toggleModal,
});
</script>
<template>
    <NDrawer :show="showYoutubeModal" size="small" width="100%" to="#drawer-target">
        <NDrawerContent>
            <div class="pr-5 h-full overflow-auto overflowing-div relative scroll-bar-md">
                <span class="flex justify-between items-center float-left text-size-35px font-800">{{
                    data ? data.title : ''
                }}</span>
                <NButton type="error" @click="close" class="sticky top-3 absolute float-right z-50">Close</NButton>

                <div class="relative w-full prose-mirror-render-html overflow-y-auto">
                    <div class="flex items-center mt-2 gap-2">
                        <NTag type="primary" :bordered="false" round>{{ data ? data.language : '' }}</NTag>
                        <NTag :color="{ color: '#227C70' }" :bordered="false" round>
                            <template #icon>
                                <NIcon><TextAlignJustify /></NIcon>
                            </template>
                            Text
                        </NTag>
                    </div>
                    <div class="text-content-sermon" v-html="data ? data.content : ''"></div>
                </div>
            </div>
        </NDrawerContent>
    </NDrawer>
</template>
