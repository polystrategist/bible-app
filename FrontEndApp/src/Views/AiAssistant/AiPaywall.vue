<script lang="ts" setup>
import { NButton, NSpin, useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { computed, onMounted } from 'vue';
import { useAuthStore } from '../../store/authStore';
import { useWebBillingStore } from '../../store/webBillingStore';
import MobileOnlyNotice from '../../components/MobileOnlyNotice.vue';

const authStore = useAuthStore();
const webBilling = useWebBillingStore();
const message = useMessage();

// Free users: load the web purchase plans (if web billing is configured).
// Existing subscribers (Sync): also find which store backs their plan, so the
// "Upgrade to Pro" path can open web management or steer them to the right store.
onMounted(() => {
    if (webBilling.supported) {
        webBilling.loadPlans();
        if (authStore.tier !== 'free') void webBilling.refreshActiveStore();
    }
});

// The paywall is shown to non-Pro accounts (Free and Sync). A Sync subscriber
// already pays — they should *upgrade*, not buy a second, stacked subscription.
const isSubscriber = computed(() => authStore.tier !== 'free');

// AI is a Pro-only feature, so the paywall offers Pro alone (Sync doesn't
// include AI). Prefer the known id, else match by title.
const proPlan = computed(
    () =>
        webBilling.plans.find((p) => p.id === 'ai_monthly') ??
        webBilling.plans.find((p) => p.title.toLowerCase().includes('pro')),
);

const proFeatures = [
    'AI verse insights — contextual insight on any passage',
    'AI Bible chat — Scripture-focused answers',
    'Sermon outlines, drafts & devotionals',
    'Everything in Sync — cross-device sync, backup & web access',
];

// Human-readable name for the store backing a subscription bought on mobile.
function storeLabel(store: string): string {
    switch (store) {
        case 'play_store':
            return 'Google Play (your Android device)';
        case 'app_store':
        case 'mac_app_store':
            return 'the App Store (your iPhone, iPad, or Mac)';
        case 'amazon':
            return 'the Amazon Appstore';
        case 'test_store':
            return 'the mobile app (test purchase)';
        default:
            return 'the app where you subscribed';
    }
}

// Free → buy Pro directly. Sync subscriber → upgrade the existing subscription
// in place (backend drives the Paddle plan change, prorated). A plan bought on
// a mobile store can't be changed from here, so we steer the user to that store.
async function choosePro() {
    const plan = proPlan.value;
    if (!plan) return;

    if (!isSubscriber.value) {
        await webBilling.purchase(plan);
        return;
    }

    const res = await webBilling.upgradeToPro();
    if (res.status === 'upgraded') {
        message.success('You’re now on Pro — enjoy the AI assistant!');
    } else if (res.status === 'pending') {
        message.info('Upgrade received — your Pro access will activate shortly.');
    } else if (res.status === 'managed-elsewhere') {
        message.info(
            `Your subscription is billed through ${storeLabel(res.store ?? '')}. Upgrade to Pro there to avoid being charged twice.`,
        );
    } else {
        message.error(webBilling.error ?? 'Couldn’t upgrade. Please try again.');
    }
}
</script>

<template>
    <div class="ai-paywall">
        <div class="ai-paywall__glow">
            <Icon icon="lucide:sparkles" class="ai-paywall__icon" />
        </div>
        <h2>AI Bible Study Assistant</h2>
        <p>
            Chat with a Scripture-focused assistant, generate verse insights, sermon
            outlines and devotionals — all in one place.
            <template v-if="isSubscriber">You’re on Sync — upgrade to Pro to unlock it.</template>
            <template v-else>Available with Believers Sword Pro.</template>
        </p>

        <!-- Web purchasing enabled (RevenueCat Web Billing / Paddle) -->
        <template v-if="webBilling.supported">
            <div v-if="webBilling.loading" class="ai-plan-loading">
                <NSpin size="small" /> <span>Loading plans…</span>
            </div>
            <div v-else class="ai-plan-list">
                <div v-if="proPlan" class="plan-card is-highlight">
                    <div class="plan-card__badge">Best for study &amp; teaching</div>
                    <div class="plan-card__name">Pro</div>
                    <div class="plan-card__price">
                        {{ proPlan.price }}<span class="plan-card__per">/month</span>
                    </div>
                    <p class="plan-card__tagline">Everything in Sync, plus AI study tools</p>
                    <ul class="plan-card__features">
                        <li v-for="f in proFeatures" :key="f">
                            <Icon icon="lucide:check" /> <span>{{ f }}</span>
                        </li>
                    </ul>
                    <NButton
                        type="primary"
                        block
                        :loading="webBilling.purchasingId !== null"
                        :disabled="webBilling.purchasingId !== null"
                        @click="choosePro"
                    >
                        {{ isSubscriber ? 'Upgrade to Pro' : 'Choose Pro' }}
                    </NButton>
                </div>
                <p v-else class="ai-paywall__hint">
                    Plans aren't available yet. Please check back soon.
                </p>
                <p v-if="webBilling.error" class="ai-plan-error">{{ webBilling.error }}</p>
            </div>
        </template>

        <!-- Web purchasing off/not configured → direct users to the mobile app -->
        <MobileOnlyNotice v-else class="ai-paywall__mobile" />
    </div>
</template>

<style scoped>
.ai-paywall { text-align: center; max-width: 460px; margin: 48px auto; padding: 0 16px; }
.ai-paywall__glow {
    width: 76px; height: 76px; margin: 0 auto 8px;
    display: grid; place-items: center; border-radius: 22px;
    background: color-mix(in srgb, var(--primary-color) 16%, transparent);
}
.ai-paywall__icon { font-size: 40px; color: var(--primary-color); }
.ai-paywall h2 { margin: 8px 0 6px; }
.ai-paywall > p { opacity: 0.85; line-height: 1.55; }
.ai-paywall__hint { opacity: 0.7; font-size: 13px; margin-top: 8px; }
.ai-paywall__mobile { margin-top: 22px; }
.ai-plan-list { display: flex; flex-direction: column; gap: 10px; margin-top: 18px; }
.ai-plan-loading { display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 18px; opacity: 0.75; }
.ai-plan-error { color: #b45353; font-size: 13px; margin-top: 8px; }

.plan-card {
    position: relative;
    border: 1px solid var(--theme-border, rgba(127, 127, 127, 0.3));
    border-radius: 14px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    text-align: left;
    background: var(--theme-bg-elevated);
}
.plan-card.is-highlight { border-color: var(--primary-color); }
.plan-card__badge {
    position: absolute;
    top: -11px;
    left: 16px;
    background: var(--primary-color);
    color: #1a1a1a;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 999px;
}
.plan-card__name { font-size: 18px; font-weight: 700; }
.plan-card__price { font-size: 26px; font-weight: 700; margin-top: 4px; }
.plan-card__per { font-size: 13px; font-weight: 400; opacity: 0.6; }
.plan-card__tagline { margin: 4px 0 12px; font-size: 13px; opacity: 0.75; }
.plan-card__features {
    list-style: none;
    padding: 0;
    margin: 0 0 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.plan-card__features li {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 13px;
    line-height: 1.35;
}
.plan-card__features li svg { margin-top: 2px; color: #2e8b68; flex-shrink: 0; }
</style>
