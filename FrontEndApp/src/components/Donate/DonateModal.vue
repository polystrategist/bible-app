<script lang="ts" setup>
import { NIcon, NModal } from 'naive-ui';
import Donate from './Donate.vue';
import { useMainStore } from '../../store/main';
import { Close } from '@vicons/carbon';

const mainStore = useMainStore();
</script>

<template>
    <NModal v-model:show="mainStore.showDonateModal" size="small">
        <div class="overflow-y-auto w-full h-[100vh] relative">
            <div
                class="absolute right-5 top-5 h-30px w-30px bg-dark-800 text-white rounded-md cursor-pointer"
                @click="mainStore.showDonateModal = false"
            >
                <NIcon size="30">
                    <Close />
                </NIcon>
            </div>
            <Donate v-if="mainStore.showDonateModal" />
        </div>
    </NModal>
</template>
