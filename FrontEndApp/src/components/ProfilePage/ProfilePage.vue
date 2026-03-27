<script lang="ts" setup>
import { NButton, NCard, NForm, NFormItem, NInput, NSwitch, useMessage } from 'naive-ui';
import { ref } from 'vue';
import { useAuthStore } from '../../store/authStore';
import { Icon } from '@iconify/vue';

const loading = ref(false);
const authStore = useAuthStore();
const message = useMessage();

async function logout() {
    loading.value = true;
    const result = await authStore.logout();
    loading.value = false;

    if (result.success) {
        message.success('Logged out successfully.');
    } else {
        message.warning('Logged out (offline).');
    }
}

async function onSyncToggle(enabled: boolean) {
    await authStore.setSyncEnabled(enabled);
    message.success(enabled ? 'Sync enabled.' : 'Sync disabled.');
}
</script>
<template>
    <div>
        <NCard size="small">
            <NForm v-if="authStore.user">
                <h3 class="text-lg flex gap-2 items-center mb-2 font-700">
                    <Icon icon="mdi:account-circle" />
                    <span>Profile</span>
                </h3>
                <NFormItem label="Name">
                    <NInput :value="authStore.user.name" disabled />
                </NFormItem>
                <NFormItem label="Email">
                    <NInput :value="authStore.user.email" disabled />
                </NFormItem>
                <NFormItem label="Enable Sync">
                    <div class="flex items-center gap-2">
                        <NSwitch
                            :value="authStore.syncEnabled"
                            @update:value="onSyncToggle"
                        />
                        <span class="text-sm text-gray-500">
                            {{ authStore.syncEnabled ? 'Your data syncs to the cloud.' : 'Data stays local only.' }}
                        </span>
                    </div>
                </NFormItem>
                <NButton type="error" @click="logout" :disabled="loading" :loading="loading">
                    <template #icon>
                        <Icon icon="mdi:logout" />
                    </template>
                    Logout
                </NButton>
            </NForm>
        </NCard>
    </div>
</template>
