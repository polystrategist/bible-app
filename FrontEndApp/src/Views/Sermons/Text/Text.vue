<script setup lang="ts">
import { TextAlignJustify } from '@vicons/carbon';
import { NButton, NTag, NIcon, NDrawer, NDrawerContent } from 'naive-ui';
import { ref } from 'vue';
import { DAYJS } from '../../../util/dayjs';

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
            <div class="pr-5 h-full overflow-auto overflowing-div scroll-bar-md">
                <NButton type="error" @click="close" class="fixed top-3 right-5 absolute z-50">Close</NButton>

                <div class="relative w-full prose-mirror-render-html overflow-y-auto">
                    <div class="flex flex-col gap-2 items-center">
                        <div
                            class="font-800 text-size-40px flex items-center justify-center h-250px w-full bg-gray-300 dark:bg-gray-300 dark:text-gray-900 p-10px rounded-md"
                        >
                            {{ data.title }}
                        </div>
                        <div class="flex items-center mt-2 gap-2">
                            <NTag type="primary" :bordered="false" round>{{ data ? data.language : '' }}</NTag>
                            <NTag :color="{ color: '#227C70' }" :bordered="false" round>
                                <template #icon>
                                    <NIcon><TextAlignJustify /></NIcon>
                                </template>
                                Text
                            </NTag>
                        </div>
                        <div>
                            <small>{{ DAYJS(data.created_at).fromNow() }}</small> -
                            <small>{{ DAYJS(data.created_at).format('MMMM D, YYYY') }}</small>
                        </div>
                    </div>

                    <div class="pt-10 max-w-600px mx-auto">
                        <div class="text-content-sermon" v-html="data ? data.content : ''"></div>
                    </div>
                </div>
            </div>
        </NDrawerContent>
    </NDrawer>
</template>
