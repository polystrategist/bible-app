<script setup lang="ts">
import { NButton, NCard } from 'naive-ui';
import { useMainStore } from '../../store/main';

const mainStore = useMainStore();

function openDonateWindow() {
    window.browserWindow.openDonateWindow();
}
</script>
<template>
    <NCard size="small">
        <div class="text-size-20px font-800 mb-2">{{ $t('title') }} {{ mainStore.version }}</div>
        <div class="mb-2">
            Believers Sword App is an application to help you study the Bible. I'm so thankful to
            God for giving me the time to create this application and to share it with others. I'm
            not recommending this application, but I am encouraging you to try it, and I hope you
            may like it. I hope we learn to study the Bible better together.
        </div>
        <div class="mb-2"></div>
        <div>
            <div class="font-800">Support</div>
            <div>If you like to support my simple ministry, you can do by one of this ways:</div>
            <NButton @click="openDonateWindow()" class="mt-5" size="large"> Buy Me a Coffee </NButton>
        </div>
    </NCard>
</template>
