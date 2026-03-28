<script setup lang="ts">
import { NIcon } from 'naive-ui';
import { CheckmarkCircle24Filled } from '@vicons/fluent';
import { useSettingStore } from '../../../store/settingStore';

const settings = useSettingStore();

const options = [
    {
        value: 'browser-tts',
        title: 'Browser Text to Speech',
        description:
            "Uses your device's built-in speech engine to read Bible verses aloud. Works fully offline — no internet or external service required.",
    },
];
</script>

<template>
    <div class="flex flex-col gap-3">
        <div
            v-for="option in options"
            :key="option.value"
            class="flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-colors"
            :class="
                settings.verseReaderMode === option.value
                    ? 'border-[var(--primary-color)] bg-[var(--primary-color)] bg-opacity-5'
                    : 'border-gray-500 border-opacity-30 hover:border-opacity-60'
            "
            @click="settings.verseReaderMode = option.value"
        >
            <div class="flex-1">
                <div class="font-600 text-sm">{{ option.title }}</div>
                <div class="text-xs opacity-50 mt-0.5">{{ option.description }}</div>
            </div>
            <NIcon
                v-if="settings.verseReaderMode === option.value"
                size="30"
                class="flex-shrink-0 mt-0.5"
            >
                <CheckmarkCircle24Filled />
            </NIcon>
        </div>
    </div>
</template>
