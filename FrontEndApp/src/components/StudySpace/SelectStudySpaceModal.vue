<script setup lang="ts">
import { NButton, NCard, NEmpty, NIcon, NModal, NInput } from 'naive-ui';
import SpaceStudyStore from '../../store/SpaceStudyStore';
import { ref } from 'vue';
import StoreStudySpaceModal from './StoreStudySpaceModal.vue';
import { DAYJS } from '../../util/dayjs';
import {
    Delete24Filled,
    Delete24Regular,
    Edit24Filled,
    Edit24Regular,
    Search24Filled,
    Search24Regular,
} from '@vicons/fluent';
import { useThemeStore } from '../../store/theme';

const searchValue = ref<string | null>(null);
const themeStore = useThemeStore();
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
            <NCard class="max-w-700px">
                <template #header>
                    <div>
                        <div class="flex items-center justify-between">
                            <h3 class="!m-0">Select Study Space</h3>
                            <NButton secondary type="primary" @click="toggleCreateNewSpaceDialog()">
                                + New Space
                            </NButton>
                        </div>
                        <div class="mt-2">
                            <NInput v-model:value="searchValue" placeholder="Search">
                                <template #prefix>
                                    <NIcon>
                                        <Search24Filled v-if="themeStore.isDark" />
                                        <Search24Regular v-else />
                                    </NIcon>
                                </template>
                            </NInput>
                        </div>
                    </div>
                </template>
                <div
                    v-if="spaceStudyStore.lists.length"
                    class="flex flex-col gap-2 max-h-70vh overflow-auto overflowing-div pr-2 pb-20px"
                >
                    <div
                        v-for="StudySpace in spaceStudyStore.lists.filter((sentence) => {
                            if (!searchValue) return true;

                            return (
                                searchValue &&
                                (sentence.title
                                    .split(/\s+/)
                                    .some(
                                        (word) => word.toLowerCase() === searchValue?.toLowerCase()
                                    ) ||
                                    sentence.title
                                        .toLowerCase()
                                        .includes(searchValue.toLowerCase()))
                            );
                        })"
                        @click="spaceStudyStore.selectStudySpace(StudySpace)"
                        class="cursor-pointer relative group dark:hover:bg-white dark:hover:bg-opacity-10"
                        :class="{
                            'bg-white bg-opacity-10':
                                spaceStudyStore.selectedSpaceStudy?.id === StudySpace.id,
                        }"
                    >
                        <div
                            class="absolute top-0 w-10px left-0 h-0 bg-[var(--primary-color)] transition-all opacity-50"
                            :class="{
                                '!h-full': spaceStudyStore.selectedSpaceStudy?.id === StudySpace.id,
                            }"
                        ></div>
                        <div class="pl-20px pr-10px py-10px flex items-center">
                            <div class="w-full">
                                <h3 class="m-0">
                                    {{ StudySpace.title }}
                                </h3>
                                <div>{{ StudySpace.description }}</div>
                                <small class="opacity-50">
                                    {{ DAYJS(StudySpace.updated_at).format('MMMM D, YYYY') }}
                                </small>
                            </div>
                            <div>
                                <NButton
                                    type="warning"
                                    quaternary
                                    circle
                                    @click.stop="StoreStudySpaceModalRef?.toggleModal(StudySpace)"
                                >
                                    <template #icon>
                                        <NIcon>
                                            <Edit24Filled v-if="themeStore.isDark" />
                                            <Edit24Regular v-else />
                                        </NIcon>
                                    </template>
                                </NButton>
                                <NButton
                                    v-show="spaceStudyStore.lists.length > 1 || true"
                                    type="error"
                                    quaternary
                                    circle
                                    @click.stop="
                                        spaceStudyStore.deleteStudySpace(StudySpace.id as number)
                                    "
                                >
                                    <template #icon>
                                        <NIcon>
                                            <Delete24Filled v-if="themeStore.isDark" />
                                            <Delete24Regular v-else />
                                        </NIcon>
                                    </template>
                                </NButton>
                            </div>
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
