<script lang="ts" setup>
import { computed, ref } from 'vue';
import { NAvatar, NButton, NDivider, NIcon, NPopover, useDialog, useMessage, MessageReactive } from 'naive-ui';
import { Login, Logout as LogoutIcon, UserProfile as UserIcon } from '@vicons/carbon';
import { useMenuStore } from '../../../store/menu';
import { useAuthStore } from '../../../store/authStore';
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';

const router = useRouter();
const dialog = useDialog();
const authStore = useAuthStore();
const message = useMessage();
const menuStore = useMenuStore();
let loadingReactive: MessageReactive | null = null;

const showDropdown = ref(false);

const initials = computed(() => {
    const name = authStore.user?.name ?? '';
    return name
        .split(' ')
        .map((w) => w[0])
        .slice(0, 2)
        .join('')
        .toUpperCase();
});

const firstName = computed(() => authStore.user?.name?.split(' ')[0] ?? 'Account');

function goToProfile() {
    showDropdown.value = false;
    menuStore.setMenu('/profile');
}

async function logout() {
    showDropdown.value = false;
    dialog.warning({
        title: 'Confirm',
        content: 'Are you sure you want to logout?',
        positiveText: 'Yes',
        negativeText: 'No',
        onPositiveClick: async () => {
            if (!loadingReactive) {
                loadingReactive = message.loading('Signing Out...', { duration: 0 });
            }
            await authStore.logout();
            if (loadingReactive) {
                loadingReactive.destroy();
                loadingReactive = null;
            }
            message.success('Logged Out!');
            await menuStore.setMenu('/profile');
            router.push('/profile');
        },
    });
}
</script>

<template>
    <NPopover
        v-if="authStore.isAuthenticated"
        v-model:show="showDropdown"
        trigger="click"
        placement="bottom-end"
        :show-arrow="false"
        style="padding: 0; border-radius: 12px; overflow: hidden; min-width: 220px;"
    >
        <template #trigger>
            <NButton size="tiny" quaternary style="gap: 6px;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 18px; height: 18px; border-radius: 50%; background: #7c6af7; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: white; flex-shrink: 0; overflow: hidden;">
                        {{ initials }}
                    </div>
                    {{ firstName }}
                </div>
            </NButton>
        </template>

        <!-- Dropdown card -->
        <div>
            <!-- User info header -->
            <div class="flex items-center gap-3 px-4 py-3">
                <NAvatar
                    round
                    :size="40"
                    color="#7c6af7"
                    style="font-size: 16px; font-weight: 700; color: white; flex-shrink: 0;"
                >
                    {{ initials }}
                </NAvatar>
                <div class="flex flex-col min-w-0">
                    <span class="font-600 text-sm truncate">{{ authStore.user?.name }}</span>
                    <span class="text-xs opacity-50 truncate">{{ authStore.user?.email }}</span>
                </div>
            </div>

            <!-- Sync status -->
            <div v-if="authStore.syncEnabled" class="mx-4 mb-2 flex items-center gap-1 text-xs px-2 py-1 rounded-full bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 w-fit">
                <Icon icon="mdi:cloud-check" />
                <span>Sync Enabled</span>
            </div>

            <NDivider style="margin: 4px 0;" />

            <!-- Actions -->
            <div class="flex flex-col px-2 pb-2 gap-0.5">
                <NButton text type="primary" style="justify-content: flex-start; padding: 8px 10px; border-radius: 8px;" @click="goToProfile">
                    <template #icon>
                        <NIcon><UserIcon /></NIcon>
                    </template>
                    Profile
                </NButton>
                <NButton text block type="error" style="justify-content: flex-start; padding: 8px 10px; border-radius: 8px;" @click="logout">
                    <template #icon>
                        <NIcon><LogoutIcon /></NIcon>
                    </template>
                    Log Out
                </NButton>
            </div>
        </div>
    </NPopover>

    <NButton v-else round size="tiny" quaternary @click="menuStore.setMenu('/profile')">
        <template #icon>
            <NIcon>
                <Login />
            </NIcon>
        </template>
        Sign In
    </NButton>
</template>
