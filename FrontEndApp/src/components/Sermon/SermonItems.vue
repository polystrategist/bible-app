<script setup lang="ts">
import { NIcon, NTag } from 'naive-ui';
import { useUserStore } from '../../store/userStore';
import { DAYJS } from '../../util/dayjs';
import { Delete, LogoYoutube, TextAlignJustify } from '@vicons/carbon';
import { Icon } from '@iconify/vue';
import { SERMON_TYPE } from '../../store/Sermons';

const userStore = useUserStore();
const props = defineProps<{
    sermon: SERMON_TYPE
}>();
const emit = defineEmits(['showContent','publishSermon', 'deleteSermon']);

</script>
<template>
    <div
        class="min-w-280px max-w-300px rounded-md overflow-hidden group flex flex-col justify-between cursor-pointer"
        style="flex: 1 1 160px" @click="emit('showContent', sermon.youtube_video_id ? 'youtube' : 'text', sermon)">
        <div class="h-150px overflow-hidden relative">
            <div v-if="sermon.thumbnail" class="transition-all top-[0px] left-[0px] !w-full absolute">
                <img :src="sermon.thumbnail" alt=""
                    class="w-full transform scale-100 group-hover:scale-120 transition-all" />
            </div>

            <div v-else
                class="font-800 text-size-25px flex items-center justify-center h-full bg-gray-300 dark:bg-gray-300 dark:text-gray-900 p-10px transform scale-100 hover:scale-120 transition-all">
                {{ sermon.title }}
            </div>

            <div v-if="userStore.user_id == sermon.added_by" class="absolute top-1 left-1 flex flex-col gap-1">
                <div v-if="!sermon.is_published" class="bg-orange-700 px-2 rounded-md select-none text-white"
                    @click.stop="emit('publishSermon',sermon)">
                    Not Published
                </div>
                <div v-if="sermon.is_published" class="bg-green-700 px-2 rounded-md select-none text-white"
                    @click.stop="emit('publishSermon',sermon, false)">
                    Published
                </div>
                <div class="bg-red-600 px-2 rounded-md select-none text-white" @click.stop="emit('deleteSermon', sermon)">
                    <NIcon>
                        <Delete />
                    </NIcon>
                    Delete
                </div>
            </div>
        </div>
        <div class="mt-2">
            <div class="font-700">{{ sermon.title }}</div>
            <div class="overflow-hidden overflow-ellipsis whitespace-nowrap">
                {{ sermon.description }}
            </div>
            <div>
                <small>{{ DAYJS(sermon.created_at).fromNow() }}</small> -
                <small>{{ DAYJS(sermon.created_at).format('MMMM D, YYYY') }}</small>
            </div>
            <div class="flex items-center mt-2 gap-2">
                <NTag :bordered="false" round type="primary">
                    <template #icon>
                        <Icon icon="mdi:language" />
                    </template>
                    {{ sermon.language }}
                </NTag>
                <NTag v-if="sermon.youtube_video_id" :bordered="false" round type="error">
                    <template #icon>
                        <NIcon>
                            <LogoYoutube />
                        </NIcon>
                    </template>
                    Youtube
                </NTag>
                <NTag v-else :bordered="false" round type="info">
                    <template #icon>
                        <NIcon>
                            <TextAlignJustify />
                        </NIcon>
                    </template>
                    Text
                </NTag>
            </div>
        </div>
    </div>
</template>