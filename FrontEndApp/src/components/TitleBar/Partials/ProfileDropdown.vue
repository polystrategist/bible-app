<script lang="ts" setup>
import { computed, ref, onMounted } from 'vue';
import {
    NAvatar,
    NButton,
    NDivider,
    NIcon,
    NPopover,
    useDialog,
    useMessage,
    MessageReactive,
} from 'naive-ui';
import { Login, Logout as LogoutIcon, Settings as SettingsIcon, UserProfile as UserIcon } from '@vicons/carbon';
import { useMenuStore } from '../../../store/menu';
import { useMainStore } from '../../../store/main';
import { useAuthStore } from '../../../store/authStore';
import { useAvatarUrl } from '../../../util/avatar';
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import { useI18n } from 'vue-i18n';

const router = useRouter();
const dialog = useDialog();
const authStore = useAuthStore();
const message = useMessage();
const menuStore = useMenuStore();
const mainStore = useMainStore();
const { t } = useI18n();
let loadingReactive: MessageReactive | null = null;

function formatLastSync(ts: string | null): string {
    if (!ts) return t('Never');
    const date = new Date(ts);
    if (isNaN(date.getTime())) return t('Never');
    return new Intl.DateTimeFormat(undefined, {
        month: 'short', day: 'numeric',
        hour: 'numeric', minute: '2-digit',
    }).format(date);
}

const showDropdown = ref(false);

onMounted(() => authStore.loadLastSyncAt());

const initials = computed(() => {
    const name = authStore.user?.name ?? '';
    return name
        .split(' ')
        .map((w) => w[0])
        .slice(0, 2)
        .join('')
        .toUpperCase();
});

const firstName = computed(() => {
    if (authStore.user?.username) return '@' + authStore.user.username;
    return authStore.user?.name?.split(' ')[0] ?? t('Account');
});

// Current plan label for the header chip — null for Free (no chip up top).
const tierLabel = computed(() => {
    switch (authStore.tier) {
        case 'pro':
            return 'Pro';
        case 'sync':
            return 'Sync';
        default:
            return null;
    }
});

// Plan name for the "Manage subscription" row chip — always shows, incl. Free.
const planName = computed(() => tierLabel.value ?? 'Free');

// 25px for the compact trigger chip; 50px for the dropdown header
const avatarSmall  = useAvatarUrl(25);
const avatarMedium = useAvatarUrl(50);

function goToProfile() {
    showDropdown.value = false;
    menuStore.setMenu('/profile');
}

function goToSettings() {
    showDropdown.value = false;
    menuStore.setMenu('/settings-page');
}

function goToManageSubscription() {
    showDropdown.value = false;
    // Ask the Profile page to open the subscription manager once it's shown.
    mainStore.openSubscriptionRequested = true;
    menuStore.setMenu('/profile');
}

async function logout() {
    showDropdown.value = false;
    dialog.warning({
        title: t('Confirm'),
        content: t('Are you sure you want to logout?'),
        positiveText: t('Yes'),
        negativeText: t('No'),
        onPositiveClick: async () => {
            if (!loadingReactive) {
                loadingReactive = message.loading(t('Signing Out'), { duration: 0 });
            }
            await authStore.logout();
            if (loadingReactive) {
                loadingReactive.destroy();
                loadingReactive = null;
            }
            message.success(t('Logged Out'));
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
        style="padding: 0; border-radius: 12px; overflow: hidden; min-width: 220px"
    >
        <template #trigger>
            <NButton size="small" round quaternary>
                <template #icon>
                    <div
                        style="
                            width: 18px;
                            height: 18px;
                            border-radius: 50%;
                            background: #7c6af7;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 10px;
                            font-weight: 700;
                            color: white;
                            flex-shrink: 0;
                            overflow: hidden;
                        "
                    >
                        <img v-if="avatarSmall" :src="avatarSmall" style="width:100%;height:100%;object-fit:cover;display:block;" />
                        <span v-else>{{ initials }}</span>
                    </div>
                </template>
                {{ firstName }}
                <span
                    v-if="tierLabel"
                    class="plan-chip plan-chip--mini"
                    :class="`tier-${authStore.tier}`"
                >{{ tierLabel }}</span>
            </NButton>
        </template>

        <!-- Dropdown card -->
        <div>
            <!-- User info header -->
            <div class="flex items-center gap-3 px-4 py-3">
                <NAvatar
                    v-if="avatarMedium"
                    round
                    :size="40"
                    :src="avatarMedium"
                    object-fit="cover"
                    style="flex-shrink: 0"
                />
                <NAvatar
                    v-else
                    round
                    :size="40"
                    color="#7c6af7"
                    style="font-size: 16px; font-weight: 700; color: white; flex-shrink: 0"
                >
                    {{ initials }}
                </NAvatar>
                <div class="flex flex-col min-w-0">
                    <span class="font-600 text-sm truncate">{{ authStore.user?.name }}</span>
                    <span class="text-xs opacity-50 truncate">{{ authStore.user?.email }}</span>
                </div>
            </div>

            <!-- Sync status -->
            <div class="mx-4 mb-2 flex flex-col gap-1">
                <div class="flex items-center gap-1 text-xs opacity-40 px-1">
                    <Icon icon="mdi:clock-outline" style="font-size: 12px" />
                    <span>{{ $t('Last sync') }}: {{ formatLastSync(authStore.lastSyncAt) }}</span>
                </div>
            </div>

            <NDivider style="margin: 0" />

            <div class="flex flex-col p-2">
                <!-- Actions -->
                <NButton
                    quaternary
                    type="primary"
                    style="justify-content: flex-start; padding: 8px 10px; border-radius: 8px"
                    @click="goToProfile"
                >
                    <template #icon>
                        <NIcon><UserIcon /></NIcon>
                    </template>
                    {{ $t('Profile') }}
                </NButton>
                <NButton
                    quaternary
                    type="primary"
                    style="justify-content: flex-start; padding: 8px 10px; border-radius: 8px"
                    @click="goToSettings"
                >
                    <template #icon>
                        <NIcon><SettingsIcon /></NIcon>
                    </template>
                    {{ $t('Settings') }}
                </NButton>
                <NButton
                    quaternary
                    type="primary"
                    style="justify-content: flex-start; padding: 8px 10px; border-radius: 8px"
                    @click="goToManageSubscription"
                >
                    <template #icon>
                        <NIcon><Icon icon="lucide:credit-card" /></NIcon>
                    </template>
                    {{ $t('Manage subscription') }}
                    <span
                        class="plan-chip plan-chip--mini ml-auto"
                        :class="`tier-${authStore.tier}`"
                    >{{ planName }}</span>
                </NButton>
            </div>
            <NDivider style="margin: 0" />
            <div class="flex flex-col p-2">
                <NButton
                    quaternary
                    type="error"
                    style="justify-content: flex-start; padding: 8px 10px; border-radius: 8px"
                    @click="logout"
                >
                    <template #icon>
                        <NIcon><LogoutIcon /></NIcon>
                    </template>
                    {{ $t('Log Out') }}
                </NButton>
            </div>
        </div>
    </NPopover>

    <NButton v-else round size="small" quaternary @click="menuStore.setMenu('/profile')">
        <template #icon>
            <NIcon>
                <Login />
            </NIcon>
        </template>
        {{ $t('Sign In') }}
    </NButton>
</template>

<style scoped>
/* Tier chips — colours mirror the Subscription card's plan pills
   (Sync = green, Pro = purple). */
.plan-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    line-height: 1.5;
    border: 1px solid transparent;
}

/* Compact variant shown beside the username in the header trigger. */
.plan-chip--mini {
    margin-left: 6px;
    padding: 0 7px;
    font-size: 10px;
}

.plan-chip.tier-free {
    color: #94a3b8;
    background: rgba(148, 163, 184, 0.16);
    border-color: rgba(148, 163, 184, 0.3);
}

.plan-chip.tier-sync {
    color: #2e8b68;
    background: rgba(46, 139, 104, 0.16);
    border-color: rgba(46, 139, 104, 0.3);
}

.plan-chip.tier-pro {
    color: #8b5cf6;
    background: rgba(139, 92, 246, 0.16);
    border-color: rgba(139, 92, 246, 0.3);
}
</style>
