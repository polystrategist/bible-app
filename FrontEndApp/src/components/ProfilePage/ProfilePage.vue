<script lang="ts" setup>
import { NAlert, NButton, NForm, NSwitch, useMessage } from 'naive-ui';
import { computed, ref } from 'vue';
import { useAuthStore } from '../../store/authStore';
import { Icon } from '@iconify/vue';
import { useRouter } from 'vue-router';

const loading = ref(false);
const authStore = useAuthStore();
const message = useMessage();
const router = useRouter();

const initials = computed(() => {
    const name = authStore.user?.name ?? '';
    return name
        .split(' ')
        .map((part) => part[0])
        .filter(Boolean)
        .slice(0, 2)
        .join('')
        .toUpperCase();
});

async function logout() {
    loading.value = true;
    const result = await authStore.logout();
    loading.value = false;

    if (result.success) {
        message.success('Logged out successfully.');
    } else {
        message.warning('Logged out (offline).');
    }
    router.push('/profile');
}

async function onSyncToggle(enabled: boolean) {
    if (enabled) {
        message.info('To enable sync, download the Believers Sword mobile app and enable sync there.');
        return;
    }

    await authStore.setSyncEnabled(false);
    message.success('Sync disabled.');
}
</script>

<template>
    <div class="profile-shell">
            <NForm v-if="authStore.user">
                <div class="flex items-start justify-between gap-4 mb-6">
                    <div class="flex items-center gap-4">
                        <div class="profile-avatar">
                            {{ initials }}
                        </div>
                        <div class="flex flex-col gap-1">
                            <h3 class="text-lg flex gap-2 items-center font-700 m-0">
                                <Icon icon="mdi:account-circle" />
                                <span>Profile</span>
                            </h3>
                            <span class="text-sm opacity-65">
                                Your account information and sync status.
                            </span>
                        </div>
                    </div>
                    <div class="profile-status-chip" :class="authStore.syncEnabled ? 'is-enabled' : 'is-disabled'">
                        <Icon :icon="authStore.syncEnabled ? 'mdi:cloud-check' : 'mdi:cloud-off-outline'" />
                        <span>{{ authStore.syncEnabled ? 'Sync On' : 'Desktop Only' }}</span>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div class="profile-info-block">
                        <span class="profile-label">Name</span>
                        <div class="profile-value-row">
                            <Icon icon="mdi:account-outline" class="opacity-60" />
                            <span class="profile-value">{{ authStore.user.name }}</span>
                        </div>
                    </div>
                    <div class="profile-info-block">
                        <span class="profile-label">Email</span>
                        <div class="profile-value-row">
                            <Icon icon="mdi:email-outline" class="opacity-60" />
                            <span class="profile-value">{{ authStore.user.email }}</span>
                        </div>
                    </div>
                </div>

                <div class="sync-panel">
                    <div class="flex items-start justify-between gap-4">
                        <div>
                            <div class="flex items-center gap-2 font-700 mb-1">
                                <Icon icon="mdi:sync" />
                                <span>Sync</span>
                            </div>
                            <p class="m-0 text-sm opacity-70">
                                Sync can be managed from the Believers Sword mobile app.
                            </p>
                        </div>
                        <NSwitch
                            :value="authStore.syncEnabled"
                            :disabled="true"
                            @update:value="onSyncToggle"
                        />
                    </div>

                    <NAlert type="info" :show-icon="false" class="mt-4">
                        To sync your data, download the Believers Sword mobile app and enable sync in it.
                    </NAlert>

                    <div class="sync-footer">
                        <div v-if="authStore.syncEnabled" class="sync-footer-item is-active">
                            <Icon icon="mdi:check-circle-outline" />
                            <span>Sync is currently enabled for this account</span>
                        </div>
                    </div>
                </div>

                <div class="mt-6 flex justify-end">
                    <NButton type="error" secondary @click="logout" :disabled="loading" :loading="loading">
                        <template #icon>
                            <Icon icon="mdi:logout" />
                        </template>
                        Logout
                    </NButton>
                </div>
            </NForm>
    </div>
</template>

<style scoped>
.profile-shell {
    max-width: 900px;
    margin: 0 auto;
    padding: 4px 4px 0;
    background:
        radial-gradient(circle at top right, rgba(111, 132, 255, 0.18), transparent 26%),
        linear-gradient(180deg, rgba(255, 255, 255, 0.02), rgba(255, 255, 255, 0));
    border-radius: 24px;
}

.profile-avatar {
    width: 56px;
    height: 56px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 700;
    color: #fff;
    background: linear-gradient(135deg, #6f84ff 0%, #5fb0ff 100%);
    box-shadow: 0 10px 30px rgba(95, 176, 255, 0.25);
}

.profile-status-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
}

.profile-status-chip.is-enabled {
    background: rgba(74, 222, 128, 0.14);
    color: #86efac;
}

.profile-status-chip.is-disabled {
    background: rgba(148, 163, 184, 0.14);
    color: rgba(255, 255, 255, 0.72);
}

.profile-info-block {
    padding: 16px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.profile-label {
    display: block;
    font-size: 12px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    opacity: 0.55;
    margin-bottom: 10px;
}

.profile-value-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

.profile-value {
    font-size: 16px;
    font-weight: 600;
    line-height: 1.4;
    word-break: break-word;
}

.sync-panel {
    padding: 18px;
    border-radius: 18px;
    background: rgba(67, 97, 176, 0.16);
    border: 1px solid rgba(107, 145, 255, 0.22);
}

.sync-footer {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 14px;
}

.sync-footer-item {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.06);
    font-size: 12px;
    opacity: 0.82;
}

.sync-footer-item.is-active {
    background: rgba(74, 222, 128, 0.14);
    color: #bbf7d0;
}
</style>
