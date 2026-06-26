<script setup lang="ts">
import { NSwitch } from 'naive-ui';
import { onMounted, ref, watch } from 'vue';

// English-only for now (mirrors the mobile "Daily encouragement" setting).
const enabled = ref(true);
const autoStart = ref(true);
const ready = ref(false);

onMounted(async () => {
    try {
        enabled.value = await window.browserWindow.getReminderEnabled();
        autoStart.value = await window.browserWindow.getReminderAutoStart();
    } finally {
        ready.value = true;
    }
});

watch(enabled, async (value) => {
    if (!ready.value) return;
    enabled.value = await window.browserWindow.setReminderEnabled(value);
});

watch(autoStart, async (value) => {
    if (!ready.value) return;
    autoStart.value = await window.browserWindow.setReminderAutoStart(value);
});
</script>

<template>
    <div class="flex flex-col gap-4">
        <div class="flex items-start justify-between gap-4">
            <div>
                <div class="text-sm font-medium">Daily encouragement</div>
                <div class="text-xs opacity-50">
                    Gentle nudges to return when you've been away. Keeps the app in
                    the system tray so reminders can reach you.
                </div>
            </div>
            <NSwitch v-model:value="enabled" :disabled="!ready" />
        </div>

        <div class="flex items-start justify-between gap-4 pl-4">
            <div>
                <div class="text-sm font-medium" :class="{ 'opacity-50': !enabled }">
                    Start with Windows
                </div>
                <div class="text-xs opacity-50">
                    Launch quietly at login so reminders still arrive after a
                    restart. Turn off to only run reminders while the app is open.
                </div>
            </div>
            <NSwitch v-model:value="autoStart" :disabled="!ready || !enabled" />
        </div>
    </div>
</template>
