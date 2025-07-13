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
import SermonItems from '../../components/Sermon/SermonItems.vue';
import SelectContentToCreateModal from '../../components/Sermon/SelectContentToCreateModal.vue';
import { Info24Regular, Info28Filled } from '@vicons/fluent';
import { useThemeStore } from '../../store/theme';

const SelectContentToCreateModalRef = ref();
const message = useMessage();
const dialog = useDialog();
const userStore = useUserStore();
const menuStore = useMenuStore();
const sermonItems = ref<HTMLElement | null>(null);
const sermonStore = userSermonStore();
const showYoutubeVideo = ref<null | { toggleModal: Function }>(null);
const textVueContent = ref<null | { toggleModal: Function }>(null);
const themeStore = useThemeStore();

function showContent(from: 'youtube' | 'text', sermon: any) {
    if (from == 'youtube') showYoutubeVideo.value?.toggleModal(sermon);
    else if (from == 'text') textVueContent.value?.toggleModal(sermon);
}

useInfiniteScroll(
    sermonItems as any,
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
            const { error } = await supabase
                .from('sermons')
                .update({ is_published: publish })
                .eq('id', sermon.id);
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

function handleBelieversSwordInfoDialog() {
    dialog.info({
        title: "Believers Feed",
        content: "Believers’ Feed is your spiritual hub within the Believers Sword community—a place where believers come together to share and grow. Here, you’ll find user-submitted sermons, powerful YouTube videos with sermon content, thought-provoking written messages, and engaging discussions centered on faith and the Word of God. Whether you're looking for inspiration, teaching, or fellowship, the Believers’ Feed connects you to a stream of Spirit-led content created and curated by fellow believers"
    })
}

</script>
<template>
    <div id="drawer-target" class="w-full h-full overflowing-div relative">
        <Youtube ref="showYoutubeVideo" />
        <TextVue ref="textVueContent" />
        <div class="!h-50px flex justify-between items-center z-99 w-full">
            <div class="font-700 text-size-25px pl-5 flex items-center gap-2">
                <span>{{ $t('Believers\' Feed') }}</span>
                <NIcon class="cursor-pointer" @click="handleBelieversSwordInfoDialog">
                    <Info24Regular v-if="themeStore.isDark" />
                    <Info28Filled v-else />
                </NIcon>
            </div>
            <div class="flex gap-8px pr-8">
                <NInput v-model:value="sermonStore.search" :disabled="sermonStore.loading" class="!w-300px"
                    placeholder="Search Using Text" size="small" @keydown.enter="sermonStore.getSermons(true)" />
                <NButton :disabled="sermonStore.loading" :loading="sermonStore.loading" size="small"
                    @click="sermonStore.getSermons(true)">
                    <template #icon>
                        <NIcon>
                            <Search />
                        </NIcon>
                    </template>
                    {{ $t('Search') }}
                </NButton>
                <NButton :disabled="sermonStore.loading" :loading="sermonStore.loading" size="small" @click="
                    sermonStore.search = '';
                sermonStore.getSermons(true);
                ">
                    <template #icon>
                        <NIcon>
                            <Reset />
                        </NIcon>
                    </template>
                    {{ $t('Reset') }}
                </NButton>
                <NButton size="small" type="primary" @click="SelectContentToCreateModalRef?.toggleModal()">
                    <template #icon>
                        <Icon icon="iconoir:submit-document" />
                    </template>
                    {{ $t('Submit Sermon') }}
                </NButton>
            </div>
        </div>
        <div ref="sermonItems"
            class="h-[calc(100%-110px)] px-2 pt-3 pb-5 overflow-y-auto overflowing-div scroll-bar-md">
            <div class="flex gap-7 flex-wrap px-5 justify-center">
                <SermonItems v-for="sermon in sermonStore.sermons" :sermon="sermon"
                    @showContent="(sermonType: any, sermon: any) => showContent(sermonType, sermon)"
                    @publishSermon="(sermon: any, isPublish: any) => publishSermon(sermon, isPublish)"
                    @deleteSermon="(sermon: any) => deleteSermon(sermon)" />
            </div>
            <div v-show="sermonStore.loading" class="text-center py-4">LOADING MORE DATA</div>
        </div>
        <SelectContentToCreateModal ref="SelectContentToCreateModalRef" />
    </div>
</template>
