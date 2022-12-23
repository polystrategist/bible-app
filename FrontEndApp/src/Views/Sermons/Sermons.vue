<script lang="ts" setup>
import { NIcon, NInput, NTag } from 'naive-ui';
import { userSermonStore } from '../../store/Sermons';
import { LogoYoutube, TextAlignJustify } from '@vicons/carbon';
import Youtube from './Youtube/Youtube.vue';
import { ref } from 'vue';
import TextVue from './Text/Text.vue';

const sermonStore = userSermonStore();
const showYoutubeVideo = ref<null | { toggleModal: Function }>(null);
const textVueContent = ref<null | { toggleModal: Function }>(null);

function showContent(from: 'youtube' | 'text', sermon: any) {
    console.log(from);
    if (from == 'youtube') showYoutubeVideo.value?.toggleModal(sermon);
    else if (from == 'text') textVueContent.value?.toggleModal(sermon);
}
</script>
<template>
    <div class="w-full h-full pl-6">
        <Youtube ref="showYoutubeVideo" />
        <TextVue ref="textVueContent" />
        <div class="h-50px flex justify-between px-2 py-3 items-center">
            <div class="font-700 text-size-25px">Sermons</div>
            <div class="w-300px">
                <NInput />
            </div>
        </div>
        <div class="h-[calc(100%-50px)] px-2 py-3 overflow-y-auto overflowing-div scroll-bar-md flex gap-7 flex-wrap">
            <div
                v-for="sermon in sermonStore.sermons"
                class="min-w-280px max-w-300px rounded-md overflow-hidden group flex flex-col justify-between cursor-pointer"
                @click="showContent(sermon.youtube_video_id ? 'youtube' : 'text', sermon)"
            >
                <div class="w-280px h-150px overflow-hidden relative">
                    <div
                        v-if="sermon.thumbnail"
                        class="transition-all top-[0px] left-[0px] w-280px h-150px absolute group-hover:top-[-20px] group-hover:left-[-20px] group-hover:w-400px group-hover:h-200px"
                    >
                        <img :src="sermon.thumbnail" alt="" />
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
