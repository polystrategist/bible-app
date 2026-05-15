<script setup lang="ts">
import { NIcon, NTag } from 'naive-ui';
import { useAuthStore } from '../../store/authStore';
import { DAYJS } from '../../util/dayjs';
import { Delete, TextAlignJustify } from '@vicons/carbon';
import { Icon } from '@iconify/vue';
import { SermonType } from '../../store/Sermons';

const authStore = useAuthStore();
const props = defineProps<{
    sermon: SermonType
}>();
const emit = defineEmits(['showContent', 'publishSermon', 'deleteSermon']);
</script>

<template>
    <div
        class="min-w-280px max-w-300px rounded-md overflow-hidden group flex flex-col justify-between cursor-pointer"
        style="flex: 1 1 160px"
        @click="emit('showContent', sermon.video_url ? 'video' : 'text', sermon)"
    >
        <div class="h-150px overflow-hidden relative">
            <div v-if="sermon.thumbnail_url" class="transition-all top-[0px] left-[0px] !w-full absolute">
                <img :src="sermon.thumbnail_url" :alt="sermon.title"
                     class="w-full transform scale-100 group-hover:scale-120 transition-all" />
            </div>
            <div v-else
                 class="font-800 text-size-25px flex items-center justify-center h-full bg-gray-300 dark:bg-gray-300 dark:text-gray-900 p-10px">
                {{ sermon.title }}
            </div>
            <div v-if="authStore.user?.id === sermon.created_by" class="absolute top-1 left-1 flex flex-col gap-1">
                <div v-if="sermon.status !== 'published'" class="bg-orange-700 px-2 rounded-md select-none text-white"
                     @click.stop="emit('publishSermon', sermon)">
                    Not Published
                </div>
                <div v-else class="bg-green-700 px-2 rounded-md select-none text-white"
                     @click.stop="emit('publishSermon', sermon, false)">
                    Published
                </div>
                <div class="bg-red-600 px-2 rounded-md select-none text-white" @click.stop="emit('deleteSermon', sermon)">
                    <NIcon><Delete /></NIcon>
                    Delete
                </div>
            </div>
        </div>
        <div class="mt-2">
            <div class="font-700">{{ sermon.title }}</div>
            <div class="overflow-hidden overflow-ellipsis whitespace-nowrap">{{ sermon.short_summary }}</div>
            <div>
                <small>{{ DAYJS(sermon.created_at).fromNow() }}</small>
            </div>
            <div class="flex items-center mt-2 gap-2">
                <NTag v-if="sermon.video_url" :bordered="false" round type="error">
                    <template #icon><Icon icon="mdi:play-circle-outline" /></template>
                    Video
                </NTag>
                <NTag v-else :bordered="false" round type="info">
                    <template #icon><NIcon><TextAlignJustify /></NIcon></template>
                    Text
                </NTag>
            </div>
        </div>
    </div>
</template>
