<script setup lang="ts">
import { YoutubeVue3 } from 'youtube-vue3';
import { NCard, NModal, NButton } from 'naive-ui';
import { ref, reactive } from 'vue';

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
    console.log('## OnEnded');
    stopCurrentVideo();
}
function onPaused() {
    console.log('## OnPaused');
}
function onPlayed() {
    console.log('## OnPlayed');
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
    <NModal :show="showYoutubeModal" size="small">
        <NCard class="my-20px mx-40px min-h-[90vh]">
            <template #header>
                <div class="flex justify-between items-center">
                    <span>{{ data.title ? data.title : '' }}</span>
                    <NButton @click="close">Close</NButton>
                </div>
            </template>
            <div class="relative w-full h-500px">
                <YoutubeVue3
                    v-if="play.video_id"
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
        </NCard>
    </NModal>
</template>
