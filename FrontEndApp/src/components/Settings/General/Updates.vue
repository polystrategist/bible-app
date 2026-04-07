<script setup lang="ts">
import { NButton, NTag, NProgress } from 'naive-ui';
import { ref, onMounted } from 'vue';
import { Icon } from '@iconify/vue';

type Status = 'idle' | 'checking' | 'available' | 'downloading' | 'ready' | 'up-to-date' | 'error';

const status = ref<Status>('idle');
const errorMsg = ref('');
const downloadPercent = ref(0);

onMounted(() => {
    window.browserWindow.onUpdateAvailable(() => {
        status.value = 'downloading';
        downloadPercent.value = 0;
    });
    window.browserWindow.onUpdateProgress((percent: number) => {
        downloadPercent.value = percent;
    });
    window.browserWindow.onUpdateDownloaded(() => {
        status.value = 'ready';
    });
});

async function checkForUpdates() {
    status.value = 'checking';
    errorMsg.value = '';
    try {
        const result = await window.browserWindow.checkForUpdates();
        if (!result.success) {
            errorMsg.value = result.error ?? 'Unknown error';
            status.value = 'error';
        } else if (result.updateAvailable) {
            status.value = 'available';
        } else {
            status.value = 'up-to-date';
        }
    } catch {
        errorMsg.value = 'Could not reach update server.';
        status.value = 'error';
    }
}

function downloadUpdate() {
    status.value = 'downloading';
    downloadPercent.value = 0;
    window.browserWindow.downloadUpdate();
}

function installUpdate() {
    window.browserWindow.installUpdate();
}
</script>

<template>
    <div class="flex flex-col gap-2">
        <div class="text-sm font-600">Updates</div>
        <div class="flex items-center gap-3 flex-wrap">
            <NButton
                size="small"
                secondary
                :loading="status === 'checking'"
                :disabled="status === 'downloading' || status === 'ready'"
                @click="checkForUpdates"
            >
                <template #icon><Icon icon="mdi:refresh" /></template>
                Check for Updates
            </NButton>

            <NButton
                v-if="status === 'available'"
                size="small"
                type="primary"
                @click="downloadUpdate"
            >
                <template #icon><Icon icon="mdi:download" /></template>
                Download Update
            </NButton>

            <NButton
                v-if="status === 'ready'"
                size="small"
                type="warning"
                @click="installUpdate"
            >
                <template #icon><Icon icon="mdi:restart" /></template>
                Install &amp; Restart
            </NButton>

            <NTag v-if="status === 'up-to-date'" type="success" size="small">You're up to date</NTag>
            <NTag v-else-if="status === 'available'" type="info" size="small">Update available</NTag>
            <NTag v-else-if="status === 'ready'" type="warning" size="small">Update ready to install</NTag>
            <span v-else-if="status === 'error'" class="text-xs text-red-400">{{ errorMsg }}</span>
        </div>

        <div v-if="status === 'downloading'" class="flex flex-col gap-1 mt-1">
            <span class="text-xs opacity-60">Downloading update... {{ downloadPercent }}%</span>
            <NProgress
                type="line"
                :percentage="downloadPercent"
                :height="6"
                :border-radius="3"
                :show-indicator="false"
            />
        </div>
    </div>
</template>
