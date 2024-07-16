<script setup lang="ts">
import { TextAlignJustify } from '@vicons/carbon';
import { NButton, NTag, NIcon, NDrawer, NDrawerContent } from 'naive-ui';
import { ref } from 'vue';
import { DAYJS } from '../../../util/dayjs';
import { Icon } from '@iconify/vue';

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
            <div class="pr-5 h-full overflow-auto overflowing-div scroll-bar-md relative">
                <NButton type="error" @click="close" class="top-3 right-5 sticky z-50">Close</NButton>
                <div class="relative w-full max-w-4xl prose-mirror-render-html overflow-y-auto mx-auto">
                    <div class="flex flex-col gap-2">
                        <div class="font-900 text-size-35px">
                            {{ data.title }}
                        </div>
                        <div class="flex items-center mt-2 gap-2">
                            <NTag type="primary" :bordered="false" round>
                                <template #icon><Icon icon="mdi:language" /></template>
                                {{ data ? data.language : '' }}
                            </NTag>
                            <NTag type="info" :bordered="false" round>
                                <template #icon>
                                    <NIcon><TextAlignJustify /></NIcon>
                                </template>
                                Text
                            </NTag>
                        </div>
                        <div>
                            <small>Added {{ DAYJS(data.created_at).fromNow() }}</small>
                        </div>
                    </div>
                    <div class="text-content-sermon ProseMirror" v-html="data ? data.content : ''"></div>
                </div>
            </div>
        </NDrawerContent>
    </NDrawer>
</template>
