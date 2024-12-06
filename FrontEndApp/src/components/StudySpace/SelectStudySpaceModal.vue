<script setup lang="ts">
import { NButton, NCard, NEmpty, NModal } from 'naive-ui';
import SpaceStudyStore from '../../store/SpaceStudyStore';
import { ref } from 'vue';
import StoreStudySpaceModal from './StoreStudySpaceModal.vue';
import { DAYJS } from '../../util/dayjs';

const StoreStudySpaceModalRef = ref<{
    toggleModal: Function;
}>();
const spaceStudyStore = SpaceStudyStore();

function toggleCreateNewSpaceDialog() {
    StoreStudySpaceModalRef.value?.toggleModal();
}
</script>

<template>
    <div>
        <NModal v-model:show="spaceStudyStore.showSpaceStudy">
            <NCard class="max-w-500px">
                <template #header>
                    <div class="flex items-center justify-between">
                        <h3 class="!m-0">Select Study Space</h3>
                        <NButton secondary type="primary" @click="toggleCreateNewSpaceDialog()">
                            + New Space
                        </NButton>
                    </div>
                </template>
                <div
                    v-if="spaceStudyStore.lists.length"
                    class="flex flex-col gap-2 max-h-70vh overflow-auto overflowing-div pr-2 pb-20px"
                >
                    <div
                        v-for="StudySpace in spaceStudyStore.lists"
                        @click="spaceStudyStore.selectStudySpace(StudySpace)"
                        class="cursor-pointer relative group dark:hover:bg-white dark:hover:bg-opacity-10"
                    >
                        <div
                            class="absolute top-0 w-10px left-0 h-0 group-hover:h-full bg-[var(--primary-color)] transition-all opacity-50"
                        ></div>
                        <div class="pl-20px py-10px">
                            <h3 class="m-0">{{ StudySpace.title }}</h3>
                            <div>{{ StudySpace.description }}</div>
                            <small class="opacity-50">{{ DAYJS(StudySpace.updated_at).format('MMMM D, YYYY') }}</small>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <NEmpty description="Lists Is Empty, Start By Creating A New Space">
                        <template #description>
                            Lists Is Empty, Start By Creating A New Space
                        </template>
                        <template #extra>
                            <NButton secondary type="primary" @click="toggleCreateNewSpaceDialog()">
                                + New Space
                            </NButton>
                        </template>
                    </NEmpty>
                </div>
            </NCard>
        </NModal>
        <StoreStudySpaceModal ref="StoreStudySpaceModalRef" />
    </div>
</template>
