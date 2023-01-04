<script lang="ts" setup>
import { NButton, NIcon, NInput, NSkeleton, NTag } from 'naive-ui';
import { userSermonStore } from '../../store/Sermons';
import { LogoYoutube, Search, TextAlignJustify } from '@vicons/carbon';
import Youtube from './Youtube/Youtube.vue';
import { reactive, ref } from 'vue';
import TextVue from './Text/Text.vue';

const sermonStore = userSermonStore();
const filter = reactive({
    search: null,
});
const showYoutubeVideo = ref<null | { toggleModal: Function }>(null);
const textVueContent = ref<null | { toggleModal: Function }>(null);

function showContent(from: 'youtube' | 'text', sermon: any) {
    if (from == 'youtube') showYoutubeVideo.value?.toggleModal(sermon);
    else if (from == 'text') textVueContent.value?.toggleModal(sermon);
}
</script>
<template>
    <div id="drawer-target" class="w-full h-full pl-6">
        <Youtube ref="showYoutubeVideo" />
        <TextVue ref="textVueContent" />
        <div class="h-50px flex justify-between px-2 py-3 items-center">
            <div class="font-700 text-size-25px">Sermons</div>
            <div class="flex gap-8px">
                <NInput class="!w-300px" v-model:value="filter.search" placeholder="Search Using Text" />
                <NButton>
                    <template #icon>
                        <NIcon>
                            <Search />
                        </NIcon>
                    </template>
                    Search
                </NButton>
            </div>
        </div>
        <div
            v-if="sermonStore.loading"
            class="h-[calc(100%-50px)] px-2 pt-3 pb-5 overflow-y-auto overflowing-div scroll-bar-md flex gap-7 flex-wrap"
        >
            <div
                v-for="count in 20"
                class="min-w-280px max-w-500px rounded-md overflow-hidden group flex flex-col justify-between cursor-pointer"
                style="flex: 1 1 160px"
            >
                <NSkeleton height="150px" class="w-full" />
                <NSkeleton height="30px" class="w-full my-1" />
                <NSkeleton text class="w-full my-5px" />
                <n-skeleton text style="width: 60%" />
            </div>
        </div>
        <div v-else class="h-[calc(100%-50px)] px-2 pt-3 pb-5 overflow-y-auto overflowing-div scroll-bar-md flex gap-7 flex-wrap">
            <div
                v-for="sermon in sermonStore.sermons"
                class="min-w-280px max-w-500px rounded-md overflow-hidden group flex flex-col justify-between cursor-pointer"
                @click="showContent(sermon.youtube_video_id ? 'youtube' : 'text', sermon)"
                style="flex: 1 1 160px"
            >
                <div class="h-150px overflow-hidden relative">
                    <div
                        v-if="sermon.thumbnail"
                        class="transition-all top-[0px] left-[0px] !w-full absolute group-hover:top-[-20px] group-hover:left-[-20px] group-hover:w-400px group-hover:h-200px"
                    >
                        <img class="w-full" :src="sermon.thumbnail" alt="" />
                    </div>

                    <div
                        v-else
                        class="font-800 text-size-25px flex items-center justify-center h-full bg-gray-300 dark:bg-gray-300 dark:text-gray-900 p-10px"
                    >
                        {{ sermon.title }}
                    </div>
                </div>
                <div class="mt-2">
                    <div class="font-700">{{ sermon.title }}</div>
                    <div class="overflow-hidden overflow-ellipsis whitespace-nowrap">{{ sermon.description }}</div>
                    <div class="flex items-center mt-2 gap-2">
                        <NTag type="primary" :bordered="false" round>{{ sermon.language }}</NTag>
                        <NTag v-if="sermon.youtube_video_id" :color="{ color: '#FF0000' }" round :bordered="false">
                            <template #icon>
                                <NIcon><LogoYoutube /></NIcon>
                            </template>
                            Youtube
                        </NTag>
                        <NTag v-else :color="{ color: '#227C70' }" :bordered="false" round>
                            <template #icon>
                                <NIcon><TextAlignJustify /></NIcon>
                            </template>
                            Text
                        </NTag>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
