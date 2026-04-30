<script setup lang="ts">
import { NButton, NScrollbar } from 'naive-ui';
import { useMainStore } from '../../store/main';

const mainStore = useMainStore();

function openExternal(url: string) {
    window.browserWindow.openExternal(url);
}

const features = [
    'Read multiple Bible translations in a focused reader',
    'Highlight verses and organize them by color',
    'Create notes and clip notes while studying',
    'Save bookmarks for quick return',
    'Manage prayer lists and answered prayers',
    'Use Study Space to keep research organized',
    'Listen with audio and TTS features',
    'Explore commentary and verse comparison tools',
    'Work offline with local resources',
];
</script>
<template>
    <NScrollbar class="h-full">
        <div class="max-w-600px mx-auto px-6 py-10 flex flex-col gap-8">
            <!-- Header -->
            <div class="flex flex-col items-center text-center gap-3">
                <div class="text-size-36px font-900 tracking-tight">⚔️ {{ $t('title') }}</div>
                <div class="text-size-13px opacity-50">Version {{ mainStore.version }}</div>
                <div class="text-size-14px italic opacity-70 max-w-400px">
                    "Your word is a lamp to my feet and a light to my path."
                    <span class="not-italic font-600 opacity-100"> — Psalm 119:105</span>
                </div>
            </div>

            <!-- Description -->
            <div class="flex flex-col gap-2">
                <div class="text-size-16px font-700">About</div>
                <div class="text-size-14px leading-relaxed opacity-80">
                    Believers Sword is a desktop Bible study companion that helps believers stay close to
                    Scripture throughout the day. It combines Bible reading, study tools, notes,
                    highlights, prayer tracking, sermons, and offline-friendly access in one focused
                    experience. I'm so thankful to God for giving me the time to create this
                    application and share it with others.
                </div>
            </div>

            <!-- Features -->
            <div class="flex flex-col gap-3">
                <div class="text-size-16px font-700">Features</div>
                <ul class="flex flex-col gap-2 pl-2">
                    <li
                        v-for="feature in features"
                        :key="feature"
                        class="flex items-start gap-2 text-size-13px opacity-80"
                    >
                        <span class="mt-1px shrink-0">✓</span>
                        <span>{{ feature }}</span>
                    </li>
                </ul>
            </div>

            <!-- Links -->
            <div class="flex flex-col gap-3">
                <div class="text-size-16px font-700">Links</div>
                <div class="flex flex-wrap gap-2">
                    <NButton size="small" @click="openExternal('https://believersword.com')">
                        🌐 Website
                    </NButton>
                    <NButton size="small" @click="openExternal('https://discord.gg/BVqhNEYZ')">
                        💬 Discord
                    </NButton>
                    <NButton size="small" @click="openExternal('https://t.me/+hdasBPLzCwc0ZTJh')">
                        ✈️ Telegram
                    </NButton>
                    <NButton
                        size="small"
                        @click="openExternal('https://github.com/JenuelDev/Believers-Sword/releases')"
                    >
                        📋 Release Notes
                    </NButton>
                    <NButton
                        size="small"
                        @click="openExternal('https://github.com/JenuelDev/Believers-Sword')"
                    >
                        ⭐ GitHub
                    </NButton>
                </div>
            </div>

            <!-- Support -->
            <div class="flex flex-col gap-3">
                <div class="text-size-16px font-700">Support Development</div>
                <div class="text-size-13px opacity-80 leading-relaxed">
                    If the app blesses you and you want to support development, you can buy me a
                    coffee or become a member.
                </div>
                <div class="flex gap-2">
                    <NButton
                        type="primary"
                        size="small"
                        @click="openExternal('https://buymeacoffee.com/jenuel.dev')"
                    >
                        ☕ Buy Me a Coffee
                    </NButton>
                    <NButton
                        size="small"
                        @click="openExternal('https://github.com/sponsors/JenuelDev')"
                    >
                        ❤️ GitHub Sponsors
                    </NButton>
                </div>
            </div>

            <!-- License -->
            <div class="text-size-11px opacity-40 text-center pb-4">
                Licensed under GPL-3.0 &nbsp;·&nbsp;
                <span
                    class="cursor-pointer hover:opacity-70 underline"
                    @click="openExternal('https://github.com/JenuelDev/Believers-Sword')"
                >
                    View source on GitHub
                </span>
            </div>
        </div>
    </NScrollbar>
</template>
