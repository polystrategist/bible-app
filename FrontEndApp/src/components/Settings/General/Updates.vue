<script setup lang="ts">
import { NButton, NTag, NProgress } from 'naive-ui';
import { ref, onMounted } from 'vue';
import { Icon } from '@iconify/vue';
import { useThemeStore } from '../../../store/theme';

type Status = 'idle' | 'checking' | 'available' | 'downloading' | 'ready' | 'up-to-date' | 'error';
type UpdateProvider = 'electron-updater' | 'microsoft-store' | 'unavailable';

const themeStore = useThemeStore();
const status = ref<Status>('idle');
const errorMsg = ref('');
const downloadPercent = ref(0);
const updateProvider = ref<UpdateProvider>('unavailable');
const providerMessage = ref('');

onMounted(async () => {
    const updateConfig = await window.browserWindow.getUpdateConfig();
    updateProvider.value = updateConfig.provider;
    providerMessage.value = updateConfig.message;

    if (updateConfig.provider !== 'electron-updater') {
        return;
    }

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

function openStoreUpdates() {
    window.browserWindow.openStoreUpdates();
}
</script>

<template>
    <div class="flex flex-col gap-2">
        <div class="text-sm font-600">Updates</div>
        <div
            v-if="updateProvider === 'microsoft-store'"
            class="flex items-center gap-3 flex-wrap"
        >
            <NButton size="small" secondary @click="openStoreUpdates">
                <template #icon><Icon icon="mdi:microsoft-windows" /></template>
                Open Microsoft Store
            </NButton>
            <NTag type="info" size="small">Managed by Microsoft Store</NTag>
        </div>

        <div
            v-else-if="updateProvider === 'electron-updater'"
            class="flex items-center gap-3 flex-wrap"
        >
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
                :style="themeStore.isDark ? 'color: #1a1a1a;' : ''"
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

        <div v-else class="flex items-center gap-3 flex-wrap">
            <NTag type="default" size="small">Updates unavailable here</NTag>
        </div>

        <div v-if="status === 'downloading' && updateProvider === 'electron-updater'" class="flex flex-col gap-1 mt-1">
            <span class="text-xs opacity-60">Downloading update... {{ downloadPercent }}%</span>
            <NProgress
                type="line"
                :percentage="downloadPercent"
                :height="6"
                :border-radius="3"
                :show-indicator="false"
            />
        </div>

        <div v-if="updateProvider !== 'electron-updater'" class="text-xs opacity-70 leading-5">
            {{ providerMessage }}
        </div>
    </div>
</template>
