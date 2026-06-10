<script lang="ts" setup>
import { NModal, NSpin } from 'naive-ui';
import { computed, watch } from 'vue';
import { useWebBillingStore } from '../store/webBillingStore';
import { usePlanModalStore } from '../store/planModalStore';
import SubscriptionSections from './SubscriptionSections.vue';

// Global "Choose your plan" dialog (mounted once in App.vue, opened via
// usePlanModalStore — e.g. the title-bar "Manage subscription" for Free users).
// Shows the same subscription surface as the profile page (SubscriptionSections),
// so the two stay identical.
const planModal = usePlanModalStore();
const webBilling = useWebBillingStore();

const open = computed({
    get: () => planModal.open,
    set: (v: boolean) => (v ? planModal.show() : planModal.hide()),
});

// Pull live prices the first time the dialog opens.
watch(
    () => planModal.open,
    async (isOpen) => {
        if (isOpen && webBilling.plans.length === 0) {
            await webBilling.loadPlans();
        }
    },
);
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
        <div v-else class="sub-card">
            <SubscriptionSections @purchased="planModal.hide()" />
        </div>
        <p v-if="webBilling.error" class="plan-error">{{ webBilling.error }}</p>
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
.sub-card {
    border-radius: 18px;
    background: rgba(67, 97, 176, 0.10);
    border: 1px solid rgba(107, 145, 255, 0.20);
    overflow: hidden;
}
.plan-error {
    color: #f87171;
    font-size: 13px;
    margin-top: 12px;
}
</style>
