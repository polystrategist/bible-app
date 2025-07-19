<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { NCard, NIcon, NModal, useDialog } from 'naive-ui';
import { ref } from 'vue';
import { useThemeStore } from '../../store/theme';
import { TextEditStyle24Filled, TextEditStyle24Regular } from "@vicons/fluent"
import { hasInternetConnection } from '../../util/internet';
import { useRouter } from 'vue-router';
import { useMenuStore } from '../../store/menu';

const themeStore = useThemeStore();
const showModal = ref(false);
const dialog = useDialog();
const router = useRouter();
const menuStore = useMenuStore();

function toggleModal() {
    hasInternetConnection().then((isOnline) => {
        if (isOnline) {
            showModal.value = true;
        } else {
            dialog.warning({
                title: 'No Internet Connection',
                content: 'You are not connected to the internet. To be able to submit a sermon, you need to be connected to the internet.',
                positiveText: 'OK',
                onPositiveClick: () => {
                }
            })
        }
    })
}

defineExpose({
    toggleModal
})
</script>

<template>
    <NModal v-model:show="showModal">
        <NCard style="max-width: 600px;">
            <div class="flex flex-col gap-5 w-full">
                <div class="flex gap-5 w-full">
                    <div class="flex justify-center items-center flex-col text-center gap-1 group dark:hover:bg-gray-6 cursor-pointer rounded-md p-2 w-full"
                        @click="menuStore.setMenu('/create-text-base-sermon'); showModal = false">
                        <NIcon size="40">
                            <TextEditStyle24Filled v-if="themeStore.isDark"
                                class="text-size-40px group-hover:text-blue-5" />
                            <TextEditStyle24Regular v-else class="text-size-40px group-hover:text-blue-5" />
                        </NIcon>
                        <h3 class="m-0 leading-tight group-hover:underline">Text Based Sermon</h3>
                        <p class="m-0 leading-tight">Submit a sermon in text format. Others cant comment on this.</p>
                    </div>
                    <div class="flex justify-center items-center flex-col text-center gap-1 group dark:hover:bg-gray-6 cursor-pointer rounded-md p-2 w-full"
                        @click="menuStore.setMenu('/create-sermon-youtube-share'); showModal = false">
                        <Icon icon="mdi:youtube" class="text-size-40px group-hover:text-red-5" />
                        <h3 class="m-0 leading-tight group-hover:underline">Share a Youtube Content</h3>
                        <p class="m-0 leading-tight">Share a youtube video link. Other people cant comment on this video
                            on this platform. </p>
                    </div>
                </div>
                <div
                    class="flex justify-center items-center flex-col text-center gap-1 group dark:hover:bg-gray-6 cursor-pointer rounded-md p-2 w-full">
                    <Icon icon="healthicons:group-discussion-meetingx3"
                        class="text-size-40px group-hover:text-amber-5" />
                    <h3 class="m-0 leading-tight group-hover:underline">Discussion</h3>
                    <p class="m-0 leading-tight"> Submit a discussion, so that you and others can have a reply based
                        discussion.</p>
                </div>
            </div>
        </NCard>
    </NModal>
</template>