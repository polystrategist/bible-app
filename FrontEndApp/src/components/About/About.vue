<script setup lang="ts">
import { ArrowRight } from '@vicons/carbon';
import { NCard, NIcon, NModal } from 'naive-ui';
import { useMainStore } from '../../store/main';

const mainStore = useMainStore();
const donationLinks = [
    {
        label: 'Debit/Credit',
        link: 'https://www.paypal.com/donate?hosted_button_id=DCZYF7KWPUVB4',
    },
    {
        label: 'GCash',
        link: 'https://i.ibb.co/kJGg32y/GCash-My-QR-06102021230745.png',
    },
    {
        label: 'BuyMeCoffee.com',
        link: 'https://www.buymeacoffee.com/BroJenuel',
    },
    {
        label: 'Ko-Fi.com',
        link: 'https://ko-fi.com/brojenuel',
    },
];
</script>
<template>
    <NCard size="small">
        <div class="text-size-20px font-800">{{ $t('title') }} {{ mainStore.version }}</div>
        <div class="mb-2">
            Believers Sword App is an application to help you study the bible. I built this apps specifically from my taste of
            view. I just really want to create an application including the features that I like to have in the application. Im so
            thankful to God for giving me time to create this application and also to share to others. Im not recommending this
            application, but I am encouraging you to try the application I built, and hoping that you may like it. I hope we learn
            to study the bible better.
        </div>
        <div class="mb-2">
            The reason why I recreate the application is to apply good practice, because the old code base was made for me to
            learn electron development and how to implement in real world, I just realize some people are actually using the
            application, As the project grows, I realized that it can become a problem in the future because it was made without
            planning. So for now I recreated this application to make sure that adding feature will be easy to implement.
        </div>
        <div>
            <div class="font-800">Support</div>
            <div>If you like to support my simple ministry, you can do by one of this ways:</div>
            <ul class="pl-5 flex flex-col gap-1 mt-2">
                <li class="flex items-center gap-1" v-for="donationLink in donationLinks" :key="donationLink.label">
                    <NIcon>
                        <ArrowRight />
                    </NIcon>
                    <a :href="donationLink.link" class="outline-none hover:underline">{{ donationLink.label }}</a>
                </li>
            </ul>
        </div>
    </NCard>
</template>
