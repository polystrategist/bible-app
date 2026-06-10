<script lang="ts" setup>
import { NModal, NButton, NInput, useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { computed, ref, watch } from 'vue';
import axios from 'axios';
import { useFeedbackModalStore } from '../store/feedbackModalStore';
import { useAuthStore } from '../store/authStore';

// Global Feedback dialog (mounted once in App.vue, opened from the Help menu).
// Authenticated users can send one message every 5 days (enforced server-side).
const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

const feedbackModal = useFeedbackModalStore();
const authStore = useAuthStore();
const message = useMessage();

const open = computed({
    get: () => feedbackModal.open,
    set: (v: boolean) => (v ? feedbackModal.show() : feedbackModal.hide()),
});

const categories = [
    { key: 'bug', label: 'Bug' },
    { key: 'idea', label: 'Idea' },
    { key: 'other', label: 'Other' },
];

const text = ref('');
const category = ref<string | null>(null);
const submitting = ref(false);
const loadingStatus = ref(false);
const canSubmit = ref(true);
const cooldownDays = ref(5);
const nextAllowedAt = ref<string | null>(null);

const authHeaders = () => ({ Authorization: `Bearer ${authStore.token}` });

function reset() {
    text.value = '';
    category.value = null;
    submitting.value = false;
}

async function loadStatus() {
    if (!authStore.token) return;
    loadingStatus.value = true;
    try {
        const res = await axios.get(`${API_BASE_URL}/feedback/status`, {
            headers: authHeaders(),
        });
        canSubmit.value = res.data?.can_submit !== false;
        cooldownDays.value = res.data?.cooldown_days ?? 5;
        nextAllowedAt.value = res.data?.next_allowed_at ?? null;
    } catch {
        // Best-effort — let the server enforce on submit.
        canSubmit.value = true;
    } finally {
        loadingStatus.value = false;
    }
}

// Refresh status + clear the form each time the dialog opens.
watch(
    () => feedbackModal.open,
    (isOpen) => {
        if (isOpen) {
            reset();
            void loadStatus();
        }
    },
);

const noticeText = computed(() => {
    const base = `To keep feedback manageable, you can send one message every ${cooldownDays.value} days.`;
    if (!canSubmit.value && nextAllowedAt.value) {
        const d = new Date(nextAllowedAt.value);
        if (!Number.isNaN(d.getTime())) {
            const when = d.toLocaleDateString(undefined, {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
            });
            return `${base} You can send again on ${when}.`;
        }
    }
    return base;
});

async function submit() {
    const body = text.value.trim();
    if (!body || submitting.value || !authStore.token) return;

    submitting.value = true;
    try {
        await axios.post(
            `${API_BASE_URL}/feedback`,
            { message: body, category: category.value, platform: 'desktop' },
            { headers: authHeaders() },
        );
        message.success('Thank you for your feedback!');
        feedbackModal.hide();
    } catch (e: unknown) {
        const msg = axios.isAxiosError(e)
            ? (e.response?.data?.message ?? 'Couldn’t send feedback. Please try again.')
            : 'Couldn’t send feedback. Please try again.';
        message.error(msg);
        // A 429 means the cooldown is active — reflect it in the dialog.
        if (axios.isAxiosError(e) && e.response?.status === 429) {
            canSubmit.value = false;
            nextAllowedAt.value = e.response?.data?.next_allowed_at ?? null;
        }
    } finally {
        submitting.value = false;
    }
}
</script>

<template>
    <NModal
        v-model:show="open"
        preset="card"
        title="Send Feedback"
        :bordered="false"
        :auto-focus="false"
        style="max-width: 480px; width: 92vw;"
    >
        <div class="feedback">
            <p class="feedback__intro">
                Found a bug or have an idea? We’d love to hear from you.
            </p>

            <div class="feedback__notice">
                <Icon icon="lucide:info" />
                <span>{{ noticeText }}</span>
            </div>

            <div class="feedback__label">Category</div>
            <div class="feedback__chips">
                <NButton
                    v-for="c in categories"
                    :key="c.key"
                    size="small"
                    round
                    :type="category === c.key ? 'primary' : 'default'"
                    :secondary="category !== c.key"
                    @click="category = category === c.key ? null : c.key"
                >
                    {{ c.label }}
                </NButton>
            </div>

            <div class="feedback__label">Message</div>
            <NInput
                v-model:value="text"
                type="textarea"
                placeholder="Tell us what’s on your mind…"
                :rows="6"
                :disabled="submitting"
                maxlength="5000"
                show-count
            />
        </div>

        <template #footer>
            <div class="feedback__footer">
                <NButton :disabled="submitting" @click="feedbackModal.hide()">Cancel</NButton>
                <NButton
                    type="primary"
                    :loading="submitting"
                    :disabled="submitting || !text.trim() || !canSubmit || loadingStatus"
                    @click="submit"
                >
                    <template #icon><Icon icon="lucide:send" /></template>
                    {{ submitting ? 'Sending…' : 'Send Feedback' }}
                </NButton>
            </div>
        </template>
    </NModal>
</template>

<style scoped>
.feedback {
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.feedback__intro {
    margin: 0;
    font-size: 13px;
    opacity: 0.8;
    line-height: 1.45;
}
.feedback__notice {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 10px 12px;
    border-radius: 8px;
    font-size: 12px;
    line-height: 1.45;
    color: #8a6314;
    background: rgba(216, 162, 58, 0.1);
    border: 1px solid rgba(216, 162, 58, 0.35);
}
:global(.dark) .feedback__notice {
    color: #e6b45a;
}
.feedback__label {
    font-size: 13px;
    font-weight: 600;
    margin-top: 2px;
}
.feedback__chips {
    display: flex;
    gap: 8px;
}
.feedback__footer {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
}
</style>
