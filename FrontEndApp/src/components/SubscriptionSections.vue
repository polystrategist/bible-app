<script lang="ts" setup>
import { NButton } from 'naive-ui';
import { useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { computed } from 'vue';
import { useAuthStore } from '../store/authStore';
import { useWebBillingStore } from '../store/webBillingStore';
import { useSubscriptionPlans } from '../composables/useSubscriptionPlans';
import MobileOnlyNotice from './MobileOnlyNotice.vue';

/**
 * The shared subscription surface — independent Sync and AI Assistant plans,
 * each with feature checklist and a Get/Active state, plus a "Payment method &
 * cancel" link for subscribers. Used both inline on the profile page and inside
 * the Manage-plan dialog so the two stay identical.
 */
const emit = defineEmits<{ purchased: [] }>();

const authStore = useAuthStore();
const webBilling = useWebBillingStore();
const message = useMessage();
const { planCards, syncPrice, proPrice, syncPlan, proPlan } = useSubscriptionPlans();

const syncFeatures = computed(() => planCards.value.find((c) => c.key === 'sync')?.features ?? []);
const aiFeatures = computed(() => planCards.value.find((c) => c.key === 'ai')?.features ?? []);
const isSubscriber = computed(() => authStore.hasService('sync') || authStore.hasService('ai'));

// Subscribe to a single service (Sync / AI Assistant are independent).
async function getService(key: 'sync' | 'ai') {
    if (webBilling.plans.length === 0) await webBilling.loadPlans();
    const card = planCards.value.find((c) => c.key === key);
    if (!card?.plan) {
        message.error('This plan isn’t available right now. Please try again.');
        return;
    }
    const ok = await webBilling.purchase(card.plan);
    if (ok) {
        message.success(`You’re now subscribed to ${card.name}.`);
        emit('purchased');
    } else if (webBilling.error) {
        message.error(webBilling.error);
    }
}

function storeInfo(store: string): { where: string; url?: string } {
    switch (store) {
        case 'play_store':
            return {
                where: 'Google Play (your Android device)',
                url: 'https://play.google.com/store/account/subscriptions',
            };
        case 'app_store':
        case 'mac_app_store':
            return { where: 'the App Store (your iPhone, iPad, or Mac)' };
        case 'amazon':
            return { where: 'the Amazon Appstore' };
        case 'test_store':
            return { where: 'the mobile app (test purchase)' };
        default:
            return { where: 'the app where you subscribed' };
    }
}

// "Payment method & cancel" — opens the web (Paddle) portal, or points the user
// to the store that owns a mobile-purchased subscription.
async function managePayment() {
    const res = await webBilling.manageSubscription();
    if (res.status === 'managed-elsewhere') {
        const { where, url } = storeInfo(res.store);
        message.info(`Your subscription was purchased through ${where}. Manage or cancel it there.`);
        if (url) void window.browserWindow.openExternal(url);
    } else if (res.status === 'none') {
        message.error('Couldn’t open subscription management. Please try again.');
    }
}
</script>

<template>
    <!-- ── Sync ───────────────────────────────────────────── -->
    <div class="sub-section">
        <div class="sub-head">
            <Icon icon="mdi:sync" class="sub-head__icon" />
            <span class="sub-head__title">Sync</span>
            <span class="onoff-chip" :class="authStore.syncEnabled ? 'is-on' : 'is-off'">
                <span class="onoff-dot" /> {{ authStore.syncEnabled ? 'On' : 'Off' }}
            </span>
        </div>
        <p class="sub-blurb">
            Keep your bookmarks, highlights, notes, and prayer lists backed up and in sync across devices.
        </p>
        <ul class="sub-features">
            <li v-for="f in syncFeatures" :key="f">
                <Icon icon="lucide:check" /> <span>{{ f }}</span>
            </li>
        </ul>
        <div v-if="authStore.syncEnabled" class="sync-footer-item is-active">
            <Icon icon="mdi:check-circle-outline" />
            <span>Sync is included in your subscription and stays on automatically</span>
        </div>
        <NButton
            v-else
            type="primary"
            block
            :disabled="!webBilling.supported || webBilling.purchasingId !== null"
            :loading="webBilling.purchasingId === syncPlan?.id"
            @click="getService('sync')"
        >
            <template #icon><Icon icon="lucide:sparkles" /></template>
            Get Sync · {{ syncPrice }}/mo
        </NButton>
    </div>

    <div class="sub-divider" />

    <!-- ── AI Assistant ───────────────────────────────────── -->
    <div class="sub-section">
        <div class="sub-head">
            <Icon icon="lucide:sparkles" class="sub-head__icon" />
            <span class="sub-head__title">AI Assistant</span>
            <span class="onoff-chip" :class="authStore.isAiEnabled ? 'is-on' : 'is-off'">
                <span class="onoff-dot" /> {{ authStore.isAiEnabled ? 'On' : 'Off' }}
            </span>
        </div>
        <p class="sub-blurb">
            Verse insights, sermon outlines, devotionals, and Bible chat.
        </p>
        <ul class="sub-features">
            <li v-for="f in aiFeatures" :key="f">
                <Icon icon="lucide:check" /> <span>{{ f }}</span>
            </li>
        </ul>
        <div v-if="authStore.isAiEnabled" class="sync-footer-item is-active">
            <Icon icon="mdi:check-circle-outline" />
            <span>Included with your AI Assistant plan — an allowance that refreshes every few hours</span>
        </div>
        <NButton
            v-else
            type="primary"
            block
            :disabled="!webBilling.supported || webBilling.purchasingId !== null"
            :loading="webBilling.purchasingId === proPlan?.id"
            @click="getService('ai')"
        >
            <template #icon><Icon icon="lucide:sparkles" /></template>
            Get AI Assistant · {{ proPrice }}/mo
        </NButton>
    </div>

    <!-- Checkout off → subscribing is mobile-only (QR to the app). -->
    <template v-if="!webBilling.supported">
        <div class="sub-divider" />
        <div class="sub-section">
            <MobileOnlyNotice />
        </div>
    </template>

    <!-- Checkout on + subscriber → manage payment / cancel. -->
    <template v-else-if="isSubscriber">
        <div class="sub-divider" />
        <div class="sub-section manage-portal-row">
            <NButton text type="primary" @click="managePayment">
                <template #icon><Icon icon="lucide:external-link" /></template>
                Payment method &amp; cancel
            </NButton>
        </div>
    </template>
</template>

<style scoped>
.sub-section {
    padding: 18px;
}
.sub-divider {
    height: 1px;
    background: rgba(107, 145, 255, 0.16);
}
.sub-head {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}
.sub-head__icon {
    font-size: 18px;
    color: #d8a23a;
}
.sub-head__title {
    font-weight: 800;
}
.sub-blurb {
    margin: 0 0 14px;
    font-size: 13px;
    line-height: 1.4;
    opacity: 0.75;
}
.sub-features {
    list-style: none;
    padding: 0;
    margin: 0 0 14px;
    display: flex;
    flex-direction: column;
    gap: 7px;
}
.sub-features li {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 13px;
    line-height: 1.35;
    opacity: 0.9;
}
.sub-features li .iconify {
    margin-top: 2px;
    color: #2e8b68;
    flex-shrink: 0;
}
.onoff-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 2px 9px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    border: 1px solid transparent;
}
.onoff-chip .onoff-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: currentColor;
}
.onoff-chip.is-on {
    color: #2e8b68;
    background: rgba(46, 139, 104, 0.16);
    border-color: rgba(46, 139, 104, 0.30);
}
.onoff-chip.is-off {
    color: #b45353;
    background: rgba(180, 83, 83, 0.16);
    border-color: rgba(180, 83, 83, 0.30);
}
.sync-footer-item {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 999px;
    background: var(--theme-bg-soft);
    font-size: 12px;
    opacity: 0.82;
}
.sync-footer-item.is-active {
    background: rgba(74, 222, 128, 0.14);
    color: #15803d;
}
body.dark .sync-footer-item.is-active {
    color: #bbf7d0;
}
.manage-portal-row {
    display: flex;
    justify-content: center;
}
</style>
