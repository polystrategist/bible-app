<script setup lang="ts">
import { NSwitch } from 'naive-ui';
import { onMounted, ref, watch } from 'vue';

// English-only for now (mirrors the mobile "Daily encouragement" setting).
const closeToTray = ref(true);
const enabled = ref(true);
const autoStart = ref(true);
const ready = ref(false);

onMounted(async () => {
    try {
        closeToTray.value = await window.browserWindow.getCloseToTray();
        enabled.value = await window.browserWindow.getReminderEnabled();
        autoStart.value = await window.browserWindow.getReminderAutoStart();
    } finally {
        ready.value = true;
    }
});

watch(closeToTray, async (value) => {
    if (!ready.value) return;
    closeToTray.value = await window.browserWindow.setCloseToTray(value);
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
    <div class="flex flex-col gap-3">
        <div class="text-sm font-semibold opacity-80">System tray</div>

        <!-- Parent: close-to-tray. Everything below depends on it. -->
        <div class="flex items-start justify-between gap-4">
            <div>
                <div class="text-sm font-medium">Close to tray</div>
                <div class="text-xs opacity-50">
                    When on, clicking the window's X hides the app to the system tray
                    instead of quitting — reopen it from the tray icon, or right-click
                    the icon and choose Quit to exit. Turn off to quit on close.
                </div>
            </div>
            <NSwitch v-model:value="closeToTray" :disabled="!ready" />
        </div>

        <!-- Child: reminders. Only work while the app stays in the tray. -->
        <div class="flex items-start justify-between gap-4 pl-4 border-l border-gray-500 border-opacity-20 ml-1">
            <div>
                <div class="text-sm font-medium" :class="{ 'opacity-40': !closeToTray }">
                    Daily encouragement
                </div>
                <div class="text-xs opacity-50">
                    Gentle nudges to return when you've been away.
                    <span v-if="!closeToTray">Requires “Close to tray”.</span>
                </div>
            </div>
            <NSwitch v-model:value="enabled" :disabled="!ready || !closeToTray" />
        </div>

        <!-- Grandchild: auto-start. Only meaningful with reminders on. -->
        <div class="flex items-start justify-between gap-4 pl-8 border-l border-gray-500 border-opacity-20 ml-1">
            <div>
                <div class="text-sm font-medium" :class="{ 'opacity-40': !closeToTray || !enabled }">
                    Start with Windows
                </div>
                <div class="text-xs opacity-50">
                    Launch quietly at login so reminders still arrive after a
                    restart. Turn off to only run reminders while the app is open.
                </div>
            </div>
            <NSwitch v-model:value="autoStart" :disabled="!ready || !closeToTray || !enabled" />
        </div>
    </div>
</template>
