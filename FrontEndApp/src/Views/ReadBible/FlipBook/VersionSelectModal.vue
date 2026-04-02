<script lang="ts" setup>
import { NModal, NButton, NIcon, NCard, NScrollbar } from 'naive-ui';
import { useModuleStore } from '../../../store/moduleStore';
import { useFlipbookStore } from '../../../store/flipbookStore';
import { Icon } from '@iconify/vue';

const moduleStore = useModuleStore();
const flipbookStore = useFlipbookStore();

function selectVersion(fileName: string) {
    flipbookStore.openFlipbook(fileName);
}
</script>
<template>
    <NModal
        v-model:show="flipbookStore.showVersionSelect"
        preset="card"
        :bordered="false"
        size="small"
        title="Open as Flipbook"
        class="max-w-450px"
        :z-index="10000"
    >
        <div class="flex flex-col gap-2">
            <p class="text-sm opacity-70 mb-2">Select a Bible version to read as a flipbook:</p>
            <NScrollbar style="max-height: 400px">
                <div class="flex flex-col gap-1">
                    <NButton
                        v-for="bible in moduleStore.bibleLists.filter((b: any) => !b.title.includes('commentaries'))"
                        :key="bible.file_name"
                        block
                        quaternary
                        class="!justify-start"
                        @click="selectVersion(bible.file_name)"
                    >
                        <template #icon>
                            <Icon icon="mdi:book-open-page-variant" style="font-size: 18px;" />
                        </template>
                        {{ bible.title }}
                    </NButton>
                </div>
            </NScrollbar>
        </div>
    </NModal>
</template>
