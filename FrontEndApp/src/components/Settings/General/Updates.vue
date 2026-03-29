<script setup lang="ts">
import { NButton, NTag } from 'naive-ui';
import { ref } from 'vue';
import { Icon } from '@iconify/vue';

type Status = 'idle' | 'checking' | 'available' | 'up-to-date' | 'error';

const status = ref<Status>('idle');
const errorMsg = ref('');

async function checkForUpdates() {
    status.value = 'checking';
    errorMsg.value = '';
    try {
        const result = await window.browserWindow.checkForUpdates();
        if (!result.success) {
            errorMsg.value = result.error ?? 'Unknown error';
            status.value = 'error';
        } else {
            status.value = result.updateAvailable ? 'available' : 'up-to-date';
        }
    } catch {
        errorMsg.value = 'Could not reach update server.';
        status.value = 'error';
    }
}
</script>

<template>
    <div class="flex flex-col gap-2">
        <div class="text-sm font-600">Updates</div>
        <div class="flex items-center gap-3">
            <NButton
                size="small"
                secondary
                :loading="status === 'checking'"
                @click="checkForUpdates"
            >
                <template #icon><Icon icon="mdi:refresh" /></template>
                Check for Updates
            </NButton>
            <NTag v-if="status === 'available'" type="warning" size="small">Update available — check the download dialog</NTag>
            <NTag v-else-if="status === 'up-to-date'" type="success" size="small">You're up to date</NTag>
            <span v-else-if="status === 'error'" class="text-xs text-red-400">{{ errorMsg }}</span>
        </div>
    </div>
</template>
