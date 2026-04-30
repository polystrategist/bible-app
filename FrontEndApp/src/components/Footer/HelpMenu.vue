<script setup lang="ts">
import { NPopover, NButton, NIcon, NDivider } from 'naive-ui';
import { QuestionCircle24Regular } from '@vicons/fluent';
import { ref } from 'vue';
import { useMenuStore } from '../../store/menu';

const menuStore = useMenuStore();
const show = ref(false);

function navigate(path: string) {
    show.value = false;
    menuStore.setMenu(path);
}

function open(url: string) {
    show.value = false;
    window.browserWindow.openExternal(url);
}
</script>
<template>
    <NPopover
        v-model:show="show"
        trigger="click"
        placement="bottom-end"
        :show-arrow="false"
        style="padding: 0; border-radius: 10px; overflow: hidden; min-width: 220px"
    >
        <template #trigger>
            <NButton round size="small" quaternary>
                <template #icon>
                    <NIcon size="20">
                        <QuestionCircle24Regular />
                    </NIcon>
                </template>
                Help
            </NButton>
        </template>

        <div class="flex flex-col p-2">
            <NButton quaternary style="justify-content: flex-start; padding: 6px 10px; border-radius: 8px" @click="navigate('/help-portal')">
                📖&nbsp; Help Portal
            </NButton>
            <NButton quaternary style="justify-content: flex-start; padding: 6px 10px; border-radius: 8px" @click="open('https://believersword.com')">
                🌐&nbsp; Visit Website
            </NButton>
            <NButton quaternary style="justify-content: flex-start; padding: 6px 10px; border-radius: 8px" @click="open('https://discord.gg/BVqhNEYZ')">
                💬&nbsp; Join Discord
            </NButton>
            <NButton quaternary style="justify-content: flex-start; padding: 6px 10px; border-radius: 8px" @click="open('https://t.me/+hdasBPLzCwc0ZTJh')">
                ✈️&nbsp; Join Telegram
            </NButton>
        </div>
        <NDivider style="margin: 0" />
        <div class="flex flex-col p-2">
            <NButton quaternary style="justify-content: flex-start; padding: 6px 10px; border-radius: 8px" @click="open('https://github.com/sponsors/JenuelDev')">
                ❤️&nbsp; Donate (GitHub Sponsors)
            </NButton>
            <NButton quaternary style="justify-content: flex-start; padding: 6px 10px; border-radius: 8px" @click="open('https://buymeacoffee.com/jenuel.dev')">
                ☕&nbsp; Donate (Buy Me a Coffee)
            </NButton>
        </div>
        <NDivider style="margin: 0" />
        <div class="flex flex-col p-2">
            <NButton quaternary style="justify-content: flex-start; padding: 6px 10px; border-radius: 8px" @click="open('https://github.com/JenuelDev/Believers-Sword/releases')">
                📋&nbsp; Release Notes
            </NButton>
            <NButton quaternary style="justify-content: flex-start; padding: 6px 10px; border-radius: 8px" @click="navigate('/about-page')">
                ℹ️&nbsp; About
            </NButton>
        </div>
    </NPopover>
</template>
