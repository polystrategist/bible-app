<script setup lang="ts">
import { YoutubeVue3 } from 'youtube-vue3';
import { NButton, NTag, NIcon, NDrawer, NDrawerContent } from 'naive-ui';
import { ref, reactive } from 'vue';
import { LogoYoutube, TextAlignJustify } from '@vicons/carbon';
import { DAYJS } from '../../../util/dayjs';
import { Icon } from '@iconify/vue';

const data = ref<any>(null);
const youtube: any = ref(null);
const showYoutubeModal = ref(false);
const play = reactive({
    video_id: null,
    loop: 1,
});

function toggleModal(sermon: any) {
    if (!sermon.youtube_video_id) window.message.warning('Video ID does not exist.');
    showYoutubeModal.value = true;
    play.video_id = sermon.youtube_video_id;
    data.value = sermon;
}

function stopCurrentVideo() {
    youtube.value.player.stopVideo();
}

function onEnded() {
    stopCurrentVideo();
}
function onPaused() {
    console.info('## OnPaused');
}
function onPlayed() {
    console.info('## OnPlayed');
}

function close() {
    showYoutubeModal.value = false;
    play.video_id = null;
}

defineExpose({
    toggleModal,
});
</script>
<template>
    <NDrawer :show="showYoutubeModal" width="100%" to="#drawer-target">
        <NDrawerContent>
            <div class="pr-5 h-full overflow-auto overflowing-div relative scroll-bar-md">
                <NButton type="error" @click="close" size="large" class="sticky top-0 absolute float-right z-50">Close</NButton>
                <div v-if="play.video_id" class="w-full max-w-4xl mx-auto">
                    <div class="relative w-full h-500px">
                        <YoutubeVue3
                            class="absolute top-0 left-0 w-[100%] h-[100%]"
                            ref="youtube"
                            :videoid="play.video_id"
                            :loop="play.loop"
                            :controls="1"
                            :width="800"
                            :height="400"
                            @ended="onEnded"
                            @paused="onPaused"
                            @played="onPlayed"
                        />
                    </div>

                    <div class="mt-5 flex flex-col gap-10px">
                        <div class="text-700 text-size-30px">{{ data.title }}</div>
                        <div class="flex items-center mt-2 gap-2">
                            <NTag type="primary" :bordered="false" round>
                                <template #icon><Icon icon="mdi:language" /></template>
                                {{ data ? data.language : '' }}
                            </NTag>
                            <NTag v-if="data.youtube_video_id" type="error" round :bordered="false">
                                <template #icon>
                                    <NIcon><LogoYoutube /></NIcon>
                                </template>
                                Youtube
                            </NTag>
                            <NTag v-else :bordered="false" round type="info">
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
                        <div>{{ data.description }}</div>
                    </div>
                </div>
            </div>
        </NDrawerContent>
    </NDrawer>
</template>
