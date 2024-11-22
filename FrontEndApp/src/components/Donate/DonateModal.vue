<script lang="ts" setup>
import { NCard, NIcon, NModal } from 'naive-ui';
import Donate from './Donate.vue';
import { useMainStore } from '../../store/main';
import { Close } from '@vicons/carbon';

const mainStore = useMainStore();
</script>

<template>
    <NModal v-model:show="mainStore.showDonateModal" size="small">
        <NCard class="overflow-y-auto w-700px h-80vh relative" content-class="!p-0 overflow-hidden">
            <Donate v-if="mainStore.showDonateModal" />
        </NCard>
    </NModal>
</template>
