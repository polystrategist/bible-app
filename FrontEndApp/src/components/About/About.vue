<script setup lang="ts">
import { ArrowRight } from '@vicons/carbon';
import { NCard, NIcon, NModal } from 'naive-ui';
import { useMainStore } from '../../store/main';

const mainStore = useMainStore();
const donationLinks = [
    {
        label: 'Buy Me a Coffee',
        link: 'https://buymeacoffee.com/jenuel.dev',
    },
];
</script>
<template>
    <NCard size="small">
        <div class="text-size-20px font-800 mb-2">{{ $t('title') }} {{ mainStore.version }}</div>
        <div class="mb-2">
            Believers Sword App is an application to help you study the Bible. I'm so thankful to God for giving me the time to create this application and to share it with others. I'm not recommending this application, but I am encouraging you to try it, and I hope you may like it. I hope we learn to study the Bible better together.
        </div>
        <div class="mb-2">
        </div>
        <div>
            <div class="font-800">Support</div>
            <div>If you like to support my simple ministry, you can do by one of this ways:</div>
            <ul class="pl-5 flex flex-col gap-1 mt-2">
                <li class="flex items-center gap-1" v-for="donationLink in donationLinks" :key="donationLink.label">
                    <NIcon>
                        <ArrowRight />
                    </NIcon>
                    <a :href="donationLink.link" target="_blank" class="outline-none hover:underline decoration-none dark:text-light">{{ donationLink.label }}</a>
                </li>
            </ul>
        </div>
    </NCard>
</template>
