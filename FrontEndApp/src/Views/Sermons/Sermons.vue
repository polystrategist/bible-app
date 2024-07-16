<script lang="ts" setup>
import { NButton, NIcon, NInput, NTag, useDialog, useMessage } from 'naive-ui';
import { SERMON_TYPE, userSermonStore } from '../../store/Sermons';
import { Delete, LogoYoutube, Reset, Search, TextAlignJustify } from '@vicons/carbon';
import Youtube from './Youtube/Youtube.vue';
import { ref } from 'vue';
import TextVue from './Text/Text.vue';
import { useInfiniteScroll } from '@vueuse/core';
import { DAYJS } from '../../util/dayjs';
import { useMenuStore } from '../../store/menu';
import { useUserStore } from '../../store/userStore';
import { supabase } from '../../util/SupaBase/SupaBase';
import { Icon } from '@iconify/vue';

const message = useMessage();
const dialog = useDialog();
const userStore = useUserStore();
const menuStore = useMenuStore();
const sermonItems = ref<HTMLElement | null>(null);
const sermonStore = userSermonStore();
const showYoutubeVideo = ref<null | { toggleModal: Function }>(null);
const textVueContent = ref<null | { toggleModal: Function }>(null);

function showContent(from: 'youtube' | 'text', sermon: any) {
    if (from == 'youtube') showYoutubeVideo.value?.toggleModal(sermon);
    else if (from == 'text') textVueContent.value?.toggleModal(sermon);
}

useInfiniteScroll(
    sermonItems,
    () => {
        if (sermonStore.sermons.length) sermonStore.page++;
    },
    { distance: sermonStore.limit }
);

function publishSermon(sermon: SERMON_TYPE, publish = true) {
    dialog.info({
        title: `${publish ? 'Publish' : 'Unpublish'} Sermon?`,
        content: `Are you sure you want to ${publish ? 'Publish' : 'Unpublish'} this sermon?`,
        positiveText: 'Yes',
        negativeText: 'No, Cancel',
        onPositiveClick: async () => {
            message.loading('Publishing');
            const { error } = await supabase.from('sermons').update({ is_published: publish }).eq('id', sermon.id);
            message.destroyAll();
            if (error) {
                message.error(error.message);
                return;
            }

            message.success('Published!');
            await sermonStore.getSermons(true);
        },
        onNegativeClick: () => {
            message.info('Canceled.');
        },
    });
}

function deleteSermon(sermon: SERMON_TYPE) {
    dialog.error({
        title: 'Delete Sermon?',
        content: 'Are you sure you want to delete this sermon?',
        positiveText: 'Yes',
        negativeText: 'No, Cancel',
        onPositiveClick: async () => {
            message.loading('Deleting Sermon');
            const { error } = await supabase.from('sermons').delete().eq('id', sermon.id);
            message.destroyAll();
            if (error) {
                message.error(error.message);
                return;
            }

            message.success('Sermon Deleted!');
            await sermonStore.getSermons(true);
        },
        onNegativeClick: () => {
            message.info('Canceled.');
        },
    });
}
</script>
<template>
    <div id="drawer-target" class="w-full h-full overflowing-div relative">
        <Youtube ref="showYoutubeVideo" />
        <TextVue ref="textVueContent" />
        <div class="!h-50px flex justify-between items-center z-99 w-full">
            <div class="font-700 text-size-25px pl-5">{{ $t('Sermons') }}</div>
            <div class="flex gap-8px pr-8">
                <NInput
                    v-model:value="sermonStore.search"
                    :disabled="sermonStore.loading"
                    class="!w-300px"
                    placeholder="Search Using Text"
                    size="small"
                    @keydown.enter="sermonStore.getSermons(true)"
                />
                <NButton
                    :disabled="sermonStore.loading"
                    :loading="sermonStore.loading"
                    size="small"
                    @click="sermonStore.getSermons(true)"
                >
                    <template #icon>
                        <NIcon>
                            <Search />
                        </NIcon>
                    </template>
                    {{ $t('Search') }}
                </NButton>
                <NButton
                    :disabled="sermonStore.loading"
                    :loading="sermonStore.loading"
                    size="small"
                    @click="
                        sermonStore.search = '';
                        sermonStore.getSermons(true);
                    "
                >
                    <template #icon>
                        <NIcon>
                            <Reset />
                        </NIcon>
                    </template>
                    {{ $t('Reset') }}
                </NButton>
                <NButton size="small" type="primary" @click="menuStore.setMenu('/create-sermon')">
                    <template #icon>
                        <Icon icon="iconoir:submit-document" />
                    </template>
                    {{ $t('Submit Sermon') }}
                </NButton>
            </div>
        </div>

        <div ref="sermonItems" class="h-[calc(100%-110px)] px-2 pt-3 pb-5 overflow-y-auto overflowing-div scroll-bar-md">
            <div class="flex gap-7 flex-wrap px-5 justify-center">
                <div
                    v-for="sermon in sermonStore.sermons"
                    class="min-w-280px max-w-300px rounded-md overflow-hidden group flex flex-col justify-between cursor-pointer"
                    style="flex: 1 1 160px"
                    @click="showContent(sermon.youtube_video_id ? 'youtube' : 'text', sermon)"
                >
                    <div class="h-150px overflow-hidden relative">
                        <div v-if="sermon.thumbnail" class="transition-all top-[0px] left-[0px] !w-full absolute">
                            <img
                                :src="sermon.thumbnail"
                                alt=""
                                class="w-full transform scale-100 group-hover:scale-120 transition-all"
                            />
                        </div>

                        <div
                            v-else
                            class="font-800 text-size-25px flex items-center justify-center h-full bg-gray-300 dark:bg-gray-300 dark:text-gray-900 p-10px transform scale-100 hover:scale-120 transition-all"
                        >
                            {{ sermon.title }}
                        </div>

                        <div v-if="userStore.user_id == sermon.added_by" class="absolute top-1 left-1 flex flex-col gap-1">
                            <div
                                v-if="!sermon.is_published"
                                class="bg-orange-700 px-2 rounded-md select-none text-white"
                                @click.stop="publishSermon(sermon)"
                            >
                                Not Published
                            </div>
                            <div
                                v-if="sermon.is_published"
                                class="bg-green-700 px-2 rounded-md select-none text-white"
                                @click.stop="publishSermon(sermon, false)"
                            >
                                Published
                            </div>
                            <div class="bg-red-600 px-2 rounded-md select-none text-white" @click.stop="deleteSermon(sermon)">
                                <NIcon>
                                    <Delete />
                                </NIcon>
                                Delete
                            </div>
                        </div>
                    </div>
                    <div class="mt-2">
                        <div class="font-700">{{ sermon.title }}</div>
                        <div class="overflow-hidden overflow-ellipsis whitespace-nowrap">{{ sermon.description }}</div>
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
            </div>
            <div v-show="sermonStore.loading" class="text-center py-4">LOADING MORE DATA</div>
        </div>
    </div>
</template>
