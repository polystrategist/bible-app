<script lang="ts" setup>
import { NModal, NButton, NSpin } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { computed, watch } from 'vue';
import { useWebBillingStore, type PlanOption } from '../store/webBillingStore';
import { usePlanModalStore } from '../store/planModalStore';
import { useAuthStore } from '../store/authStore';
import { useSubscriptionPlans } from '../composables/useSubscriptionPlans';
import MobileOnlyNotice from './MobileOnlyNotice.vue';

// Global "Choose your plan" dialog (mounted once in App.vue, opened via
// usePlanModalStore). While web/desktop checkout is disabled the plan cards are
// shown for reference but their buttons are disabled, and a QR notice points the
// user to the mobile app (see MobileOnlyNotice.vue / webBillingStore).
const planModal = usePlanModalStore();
const webBilling = useWebBillingStore();
const authStore = useAuthStore();
const { planCards } = useSubscriptionPlans();

const open = computed({
    get: () => planModal.open,
    set: (v: boolean) => (v ? planModal.show() : planModal.hide()),
});

// Pull live prices the first time the dialog opens, even while checkout is
// disabled — the prices are shown for reference (loadPlans no-ops without a web
// key, in which case the cards simply show "—").
watch(
    () => planModal.open,
    async (isOpen) => {
        if (isOpen && webBilling.plans.length === 0) {
            await webBilling.loadPlans();
        }
    },
);

async function buyPlan(plan: PlanOption) {
    if (!authStore.user?.email_verified_at) return; // store also enforces this
    const ok = await webBilling.purchase(plan);
    if (ok) planModal.hide();
}
</script>

<template>
    <NModal
        v-model:show="open"
        preset="card"
        title="Choose your plan"
        :bordered="false"
        :auto-focus="false"
        style="max-width: 720px; width: 92vw;"
    >
        <div v-if="webBilling.loading" class="plan-loading">
            <NSpin size="small" /> <span>Loading plans…</span>
        </div>
        <template v-else>
            <div class="plans-grid">
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
                        :disabled="
                            !webBilling.supported ||
                            !card.plan ||
                            webBilling.purchasingId !== null
                        "
                        :loading="!!card.plan && webBilling.purchasingId === card.plan.id"
                        @click="card.plan && buyPlan(card.plan)"
                    >
                        Choose {{ card.name }}
                    </NButton>
                </div>
            </div>

            <!-- Checkout disabled (Paddle not yet live) → subscribe on mobile. -->
            <MobileOnlyNotice v-if="!webBilling.supported" class="plan-mobile-notice" />
            <p v-if="webBilling.error" class="plan-error">{{ webBilling.error }}</p>
        </template>
    </NModal>
</template>

<style scoped>
.plan-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 24px;
    opacity: 0.8;
}
.plans-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
}
@media (max-width: 560px) {
    .plans-grid {
        grid-template-columns: 1fr;
    }
}
.plan-card {
    position: relative;
    border: 1px solid var(--theme-border, rgba(127, 127, 127, 0.3));
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
.plan-card__features li .iconify {
    margin-top: 2px;
    color: #2e8b68;
    flex-shrink: 0;
}
.plan-mobile-notice {
    margin-top: 22px;
    padding-top: 20px;
    border-top: 1px solid var(--theme-border, rgba(127, 127, 127, 0.2));
}
.plan-error {
    color: #f87171;
    font-size: 13px;
    margin-top: 12px;
}
</style>
