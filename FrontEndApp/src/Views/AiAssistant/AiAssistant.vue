<script lang="ts" setup>
import { NTabs, NTabPane, NInput, NButton, NSpin, useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { ref, computed, h, onMounted, defineComponent, type PropType } from 'vue';
import { useAiStore, AiError, AiChatMessage } from '../../store/aiStore';
import { useAuthStore } from '../../store/authStore';
import { useWebBillingStore } from '../../store/webBillingStore';

// Inline result/error renderer shared by the single-shot tabs. Defined as a
// local component so it can be used directly in the template below.
const AiResult = defineComponent({
    name: 'AiResult',
    props: {
        panel: {
            type: Object as PropType<{ loading: boolean; text: string | null; error: AiError | null }>,
            required: true,
        },
    },
    emits: ['copy'],
    setup(props, { emit }) {
        return () => {
            const p = props.panel;
            if (p.error) {
                return h('div', { class: 'ai-error-card' }, [
                    h('strong', p.error.isPaywall ? 'Upgrade to use this' : 'Something went wrong'),
                    h('p', p.error.message),
                ]);
            }
            if (p.text) {
                return h('div', { class: 'ai-result' }, [
                    h('div', { class: 'ai-result__text' }, p.text),
                    h(NButton, { size: 'small', quaternary: true, onClick: () => emit('copy', p.text) }, () => 'Copy'),
                ]);
            }
            return null;
        };
    },
});

const ai = useAiStore();
const authStore = useAuthStore();
const webBilling = useWebBillingStore();
const message = useMessage();

// Free users: load the web purchase plans (if web billing is configured).
// Existing subscribers (Sync): also find which store backs their plan, so the
// "Upgrade to Pro" path can open web management or steer them to the right store.
onMounted(() => {
    if (!authStore.isAiEnabled && webBilling.supported) {
        webBilling.loadPlans();
        if (authStore.tier !== 'free') void webBilling.refreshActiveStore();
    }
});

// The paywall is shown to non-Pro accounts (Free and Sync). A Sync subscriber
// already pays — they should *upgrade*, not buy a second, stacked subscription.
const isSubscriber = computed(() => authStore.tier !== 'free');

// AI is a Pro-only feature, so the paywall offers Pro alone (Sync doesn't
// include AI). Mirror ProfilePage's lookup: prefer the known id, else match
// by title.
const proPlan = computed(
    () =>
        webBilling.plans.find((p) => p.id === 'pro_monthly') ??
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
        // tier flips reactively → the paywall is replaced by the AI tabs. If the
        // webhook is still in flight, let the user know it'll activate shortly.
        if (authStore.isAiEnabled) {
            message.success('You’re now on Pro — enjoy the AI assistant!');
        } else {
            message.info('Upgrade received — your Pro access will activate shortly.');
        }
    } else if (res.status === 'managed-elsewhere') {
        message.info(
            `Your subscription is billed through ${storeLabel(res.store ?? '')}. Upgrade to Pro there to avoid being charged twice.`,
        );
    } else {
        message.error(webBilling.error ?? 'Couldn’t upgrade. Please try again.');
    }
}

// --- Single-shot feature state (insight / sermon / devotional) ---
const insightRef = ref('');
const insightText = ref('');
const sermonInput = ref('');
const devoInput = ref('');

interface Panel {
    loading: boolean;
    text: string | null;
    error: AiError | null;
}
const insight = ref<Panel>({ loading: false, text: null, error: null });
const sermon = ref<Panel>({ loading: false, text: null, error: null });
const devotional = ref<Panel>({ loading: false, text: null, error: null });

async function run(panel: { value: Panel }, call: () => Promise<{ text: string }>) {
    panel.value = { loading: true, text: null, error: null };
    try {
        const result = await call();
        panel.value = { loading: false, text: result.text, error: null };
    } catch (e) {
        panel.value = { loading: false, text: null, error: e as AiError };
    }
}

const runInsight = () => {
    if (!insightRef.value.trim() || !insightText.value.trim()) return;
    run(insight, () => ai.verseInsight(insightRef.value.trim(), insightText.value.trim()));
};
const runOutline = () => {
    if (!sermonInput.value.trim()) return;
    run(sermon, () => ai.sermonOutline(sermonInput.value.trim()));
};
const runFullSermon = () => {
    if (!sermonInput.value.trim()) return;
    run(sermon, () => ai.fullSermon(sermonInput.value.trim()));
};
const runDevotional = () => {
    if (!devoInput.value.trim()) return;
    run(devotional, () => ai.devotional(devoInput.value.trim()));
};

// --- Chat ---
const chatInput = ref('');
const chatError = ref<AiError | null>(null);
async function sendChat() {
    const text = chatInput.value.trim();
    if (!text || ai.chatSending) return;
    chatInput.value = '';
    chatError.value = null;
    try {
        await ai.sendChat(text);
    } catch (e) {
        chatError.value = e as AiError;
    }
}

function copy(text: string) {
    navigator.clipboard?.writeText(text);
}

function isUser(m: AiChatMessage) {
    return m.role === 'user';
}
</script>

<template>
    <div class="ai-page">
        <!-- Free tier → read-only paywall (purchase happens on mobile for now) -->
        <div v-if="!authStore.isAiEnabled" class="ai-paywall">
            <Icon icon="lucide:sparkles" class="ai-paywall__icon" />
            <h2>AI Bible Study Assistant</h2>
            <p>
                Generate verse insights, sermon outlines, devotionals, and chat with an
                assistant.
                <template v-if="isSubscriber">You’re on Sync — upgrade to Pro to unlock it.</template>
                <template v-else>Available with Believers Sword Pro.</template>
            </p>
            <!-- Web purchasing enabled (RevenueCat Web Billing / Paddle) -->
            <template v-if="webBilling.supported">
                <div v-if="webBilling.loading" class="ai-plan-loading">
                    <NSpin size="small" /> <span>Loading plans…</span>
                </div>
                <div v-else class="ai-plan-list">
                    <!-- AI is Pro-only → offer Pro as a single plan card -->
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

            <!-- Web purchasing not configured → direct users to mobile -->
            <p v-else class="ai-paywall__hint">
                Subscribe in the Believers Sword mobile app to unlock AI. Your subscription
                works here automatically once active.
            </p>
        </div>

        <template v-else>
            <div v-if="ai.remaining !== null" class="ai-credits">
                <Icon icon="lucide:sparkles" />
                <span>{{ ai.remaining }} credits left</span>
            </div>

            <NTabs type="line" animated class="ai-tabs">
                <!-- Insight -->
                <NTabPane name="insight" tab="Insight">
                    <div class="ai-form">
                        <NInput v-model:value="insightRef" placeholder="Reference (e.g. John 3:16)" />
                        <NInput v-model:value="insightText" type="textarea" :rows="3"
                            placeholder="Paste the verse text" />
                        <NButton type="primary" :loading="insight.loading" @click="runInsight">
                            Get insight
                        </NButton>
                        <AiResult :panel="insight" @copy="copy" />
                    </div>
                </NTabPane>

                <!-- Sermon -->
                <NTabPane name="sermon" tab="Sermon">
                    <div class="ai-form">
                        <NInput v-model:value="sermonInput" type="textarea" :rows="3"
                            placeholder='Topic or passage (e.g. "Grace" or Romans 8)' />
                        <div class="ai-row">
                            <NButton type="primary" :loading="sermon.loading" @click="runOutline">Outline</NButton>
                            <NButton :loading="sermon.loading" @click="runFullSermon">Full draft</NButton>
                        </div>
                        <small class="ai-note">Full sermon drafts are a Pro feature.</small>
                        <AiResult :panel="sermon" @copy="copy" />
                    </div>
                </NTabPane>

                <!-- Chat -->
                <NTabPane name="chat" tab="Chat">
                    <div class="ai-chat">
                        <div class="ai-chat__log">
                            <p v-if="ai.chat.length === 0" class="ai-chat__empty">
                                Ask anything about the Bible — passages, themes, or questions.
                            </p>
                            <div v-for="(m, i) in ai.chat" :key="i"
                                :class="['ai-bubble', isUser(m) ? 'ai-bubble--user' : 'ai-bubble--ai']">
                                {{ m.content }}
                            </div>
                            <NSpin v-if="ai.chatSending" size="small" />
                            <p v-if="chatError" class="ai-error">{{ chatError.message }}</p>
                        </div>
                        <div class="ai-row">
                            <NInput v-model:value="chatInput" placeholder="Message…" @keyup.enter="sendChat" />
                            <NButton type="primary" :loading="ai.chatSending" @click="sendChat">Send</NButton>
                        </div>
                    </div>
                </NTabPane>

                <!-- Devotional -->
                <NTabPane name="devotional" tab="Devotional">
                    <div class="ai-form">
                        <NInput v-model:value="devoInput"
                            placeholder='Topic or reference (e.g. "Hope" or Psalm 23)' />
                        <NButton type="primary" :loading="devotional.loading" @click="runDevotional">
                            Generate devotional
                        </NButton>
                        <AiResult :panel="devotional" @copy="copy" />
                    </div>
                </NTabPane>
            </NTabs>
        </template>
    </div>
</template>

<style scoped>
.ai-page { max-width: 760px; margin: 0 auto; padding: 16px; }
.ai-form { display: flex; flex-direction: column; gap: 12px; padding-top: 8px; }
.ai-row { display: flex; gap: 10px; align-items: center; }
.ai-note { opacity: 0.65; font-size: 12px; }
.ai-credits { display: flex; align-items: center; gap: 6px; font-size: 12px; opacity: 0.75; padding: 8px 2px; }
.ai-result { border: 1px solid var(--n-border-color, #e5e5e5); border-radius: 10px; padding: 14px; }
.ai-result__text { white-space: pre-wrap; line-height: 1.5; margin-bottom: 8px; }
.ai-error-card { border: 1px solid #d8a23a55; background: #d8a23a1a; border-radius: 10px; padding: 14px; }
.ai-error { color: #b45353; font-size: 13px; }
.ai-paywall { text-align: center; max-width: 460px; margin: 48px auto; }
.ai-paywall__icon { font-size: 44px; color: #d8a23a; }
.ai-paywall__hint { opacity: 0.7; font-size: 13px; margin-top: 8px; }
.ai-plan-list { display: flex; flex-direction: column; gap: 10px; margin-top: 18px; }
.ai-plan-loading { display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 18px; opacity: 0.75; }
.ai-plan-error { color: #b45353; font-size: 13px; margin-top: 8px; }

/* Pro plan card (paywall) */
.plan-card {
    position: relative;
    border: 1px solid rgba(127, 127, 127, 0.3);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    text-align: left;
}
.plan-card.is-highlight { border-color: #d8a23a; }
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
.ai-chat { display: flex; flex-direction: column; height: 60vh; }
.ai-chat__log { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; padding: 12px 0; }
.ai-chat__empty { text-align: center; opacity: 0.6; margin: auto; }
.ai-bubble { max-width: 80%; padding: 9px 12px; border-radius: 12px; white-space: pre-wrap; line-height: 1.4; }
.ai-bubble--user { align-self: flex-end; background: #d8a23a; color: #fff; }
.ai-bubble--ai { align-self: flex-start; background: var(--n-color-embedded, #f1f1f1); }
</style>
