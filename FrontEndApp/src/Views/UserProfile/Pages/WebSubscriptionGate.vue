<script setup lang="ts">
import { NButton, NSpin, NIcon, useMessage } from 'naive-ui';
import { Sparkle24Regular } from '@vicons/fluent';
import { Icon } from '@iconify/vue';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../../store/authStore';
import { useWebBillingStore, type PlanOption } from '../../../store/webBillingStore';
import { useSubscriptionPlans } from '../../../composables/useSubscriptionPlans';
import MobileOnlyNotice from '../../../components/MobileOnlyNotice.vue';

// Web access is a paid feature (Sync or Pro). The router sends Free/lapsed
// accounts here. This page lets them subscribe (RevenueCat Web Billing), refresh
// after subscribing elsewhere, or sign out — mirroring the plan cards in
// ProfilePage so the offer is consistent across the app.
const router = useRouter();
const authStore = useAuthStore();
const webBilling = useWebBillingStore();
const message = useMessage();

const refreshing = ref(false);

// Plan cards + prices come from the shared composable (single source of truth).
const { planCards } = useSubscriptionPlans();

async function buyPlan(plan: PlanOption) {
    const ok = await webBilling.purchase(plan);
    if (ok) {
        message.success('Subscription activated.');
        // purchase() already refreshed the tier; enter the app.
        if (authStore.isSyncEntitled) router.replace('/');
    }
}

// "I already subscribed" — re-pull the verified tier (e.g. webhook just landed,
// or they subscribed on mobile) and enter the app if now entitled.
async function refreshStatus() {
    refreshing.value = true;
    try {
        await authStore.getUser(true);
        if (authStore.isSyncEntitled) {
            router.replace('/');
        } else {
            message.info('No active Sync or Pro subscription found yet.');
        }
    } finally {
        refreshing.value = false;
    }
}

async function logout() {
    await authStore.logout();
    router.replace('/login');
}

onMounted(() => {
    if (webBilling.supported && authStore.user && webBilling.plans.length === 0) {
        void webBilling.loadPlans();
    }
});
</script>

<template>
    <div class="gate">
        <div class="gate__inner">
            <NIcon size="34" :component="Sparkle24Regular" class="gate__spark" />
            <h1 class="gate__title">The web app is part of Sync</h1>
            <p class="gate__subtitle">
                Cloud sync and web access are available on Believers Sword
                <strong>Sync</strong> and <strong>Pro</strong>. Subscribe to use Believers Sword in
                your browser — your data syncs automatically across every device.
            </p>

            <div v-if="webBilling.loading" class="gate__loading">
                <NSpin size="small" /> <span>Loading plans…</span>
            </div>

            <div v-else-if="webBilling.supported" class="gate__plans">
                <div
                    v-for="card in planCards"
                    :key="card.key"
                    class="plan-card"
                    :class="{ 'is-highlight': card.highlight }"
                >
                    <div v-if="card.badge" class="plan-card__badge">{{ card.badge }}</div>
                    <div class="plan-card__name">{{ card.name }}</div>
                    <div class="plan-card__price">
                        {{ card.price }}<span class="plan-card__per">/month</span>
                    </div>
                    <p class="plan-card__tagline">{{ card.tagline }}</p>
                    <ul class="plan-card__features">
                        <li v-for="f in card.features" :key="f">
                            <Icon icon="lucide:check" /> <span>{{ f }}</span>
                        </li>
                    </ul>
                    <NButton
                        :type="card.highlight ? 'primary' : 'default'"
                        block
                        :disabled="!card.plan || webBilling.purchasingId !== null"
                        :loading="!!card.plan && webBilling.purchasingId === card.plan.id"
                        @click="card.plan && buyPlan(card.plan)"
                    >
                        Choose {{ card.name }}
                    </NButton>
                </div>
            </div>

            <MobileOnlyNotice v-else class="gate__mobile" />

            <p v-if="webBilling.error" class="gate__error">{{ webBilling.error }}</p>

            <div class="gate__actions">
                <NButton text :loading="refreshing" @click="refreshStatus">
                    I already subscribed — refresh
                </NButton>
                <NButton text type="error" @click="logout">Log out</NButton>
            </div>
        </div>
    </div>
</template>

<style scoped>
.gate {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
}
.gate__inner {
    width: 100%;
    max-width: 760px;
    text-align: center;
}
.gate__spark {
    color: #d8a23a;
}
.gate__title {
    margin: 8px 0 4px;
    font-size: 24px;
    font-weight: 700;
}
.gate__subtitle {
    margin: 0 auto 24px;
    max-width: 560px;
    font-size: 14px;
    line-height: 1.5;
    opacity: 0.8;
}
.gate__loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    opacity: 0.8;
}
.gate__plans {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
    text-align: left;
}
@media (max-width: 640px) {
    .gate__plans {
        grid-template-columns: 1fr;
    }
}
.plan-card {
    position: relative;
    border: 1px solid rgba(127, 127, 127, 0.3);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    flex-direction: column;
}
.plan-card.is-highlight {
    border-color: #d8a23a;
}
.plan-card__badge {
    position: absolute;
    top: -11px;
    left: 16px;
    background: #d8a23a;
    color: #1a1a1a;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 999px;
}
.plan-card__name {
    font-size: 18px;
    font-weight: 700;
}
.plan-card__price {
    font-size: 26px;
    font-weight: 700;
    margin-top: 4px;
}
.plan-card__per {
    font-size: 13px;
    font-weight: 400;
    opacity: 0.6;
}
.plan-card__tagline {
    margin: 4px 0 12px;
    font-size: 13px;
    opacity: 0.75;
}
.plan-card__features {
    list-style: none;
    padding: 0;
    margin: 0 0 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
}
.plan-card__features li {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 13px;
    line-height: 1.35;
}
.plan-card__features li svg {
    margin-top: 2px;
    color: #2e8b68;
    flex-shrink: 0;
}
.gate__hint {
    font-size: 14px;
    opacity: 0.8;
}
.gate__mobile {
    margin-top: 8px;
}
.gate__error {
    color: #f87171;
    font-size: 13px;
    margin-top: 12px;
}
.gate__actions {
    margin-top: 24px;
    display: flex;
    gap: 20px;
    justify-content: center;
}
</style>
