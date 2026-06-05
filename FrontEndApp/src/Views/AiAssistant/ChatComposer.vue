<script lang="ts" setup>
import { computed, h } from 'vue';
import { NInput, NButton, NDropdown } from 'naive-ui';
import { Icon } from '@iconify/vue';
import type { AiMode } from '../../store/conversationStore';

const props = defineProps<{
    text: string;
    reference: string;
    mode: AiMode;
    sending: boolean;
}>();

const emit = defineEmits<{
    (e: 'update:text', v: string): void;
    (e: 'update:reference', v: string): void;
    (e: 'update:mode', v: AiMode): void;
    (e: 'send', payload: { mode: AiMode; text: string; reference: string }): void;
}>();

const MODES: Record<AiMode, { label: string; icon: string; placeholder: string }> = {
    'chat': { label: 'Chat', icon: 'lucide:message-circle', placeholder: 'Ask anything about the Bible…' },
    'insight': { label: 'Verse insight', icon: 'lucide:book-open', placeholder: 'Paste the verse text…' },
    'sermon-outline': { label: 'Sermon outline', icon: 'lucide:list-tree', placeholder: 'Topic or passage (e.g. “Grace” or Romans 8)' },
    'full-sermon': { label: 'Full sermon', icon: 'lucide:scroll-text', placeholder: 'Topic or passage for a full draft' },
    'devotional': { label: 'Devotional', icon: 'lucide:sun', placeholder: 'Topic or reference (e.g. “Hope” or Psalm 23)' },
};

const current = computed(() => MODES[props.mode]);
const isInsight = computed(() => props.mode === 'insight');

const dropdownOptions = (Object.keys(MODES) as AiMode[]).map((key) => ({
    key,
    label: MODES[key].label,
    icon: () => h(Icon, { icon: MODES[key].icon }),
}));

const canSend = computed(() =>
    !props.sending &&
    props.text.trim().length > 0 &&
    (!isInsight.value || props.reference.trim().length > 0),
);

function submit() {
    if (!canSend.value) return;
    emit('send', { mode: props.mode, text: props.text, reference: props.reference });
}

function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submit();
    }
}
</script>

<template>
    <div class="composer-wrap">
        <div class="composer">
            <!-- Insight needs a reference in addition to the verse text -->
            <NInput
                v-if="isInsight"
                :value="reference"
                class="ref-input"
                placeholder="Reference (e.g. John 3:16)"
                @update:value="emit('update:reference', $event)"
            />

            <div class="composer__box">
                <NDropdown
                    trigger="click"
                    :options="dropdownOptions"
                    @select="emit('update:mode', $event)"
                >
                    <button class="mode-pill" :title="'Mode: ' + current.label">
                        <Icon :icon="current.icon" />
                        <span class="mode-pill__label">{{ current.label }}</span>
                        <Icon icon="lucide:chevron-down" class="mode-pill__caret" />
                    </button>
                </NDropdown>

                <NInput
                    :value="text"
                    type="textarea"
                    :autosize="{ minRows: 1, maxRows: 6 }"
                    :placeholder="current.placeholder"
                    class="composer__input"
                    @update:value="emit('update:text', $event)"
                    @keydown="onKeydown"
                />

                <NButton
                    type="primary"
                    circle
                    class="send-btn"
                    :disabled="!canSend"
                    :loading="sending"
                    @click="submit"
                >
                    <template #icon><Icon icon="lucide:arrow-up" /></template>
                </NButton>
            </div>

            <p class="composer__hint">
                Press <kbd>Enter</kbd> to send · <kbd>Shift</kbd>+<kbd>Enter</kbd> for a new line.
                AI can make mistakes — verify against Scripture.
            </p>
        </div>
    </div>
</template>

<style scoped>
.composer-wrap {
    padding: 10px 16px 14px;
    background: linear-gradient(to top, var(--theme-bg-main) 60%, transparent);
}
.composer { max-width: 760px; margin: 0 auto; }
.ref-input { margin-bottom: 8px; }

.composer__box {
    display: flex;
    align-items: flex-end;
    gap: 8px;
    padding: 8px 8px 8px 8px;
    border: 1px solid var(--theme-border);
    border-radius: 18px;
    background: var(--theme-bg-elevated);
    transition: border-color 0.15s, box-shadow 0.15s;
}
.composer__box:focus-within {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--primary-color) 18%, transparent);
}

.mode-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    flex-shrink: 0;
    height: 34px;
    padding: 0 10px;
    border-radius: 12px;
    border: 1px solid var(--theme-border);
    background: var(--theme-bg-soft);
    color: inherit;
    cursor: pointer;
    font-size: 13px;
    transition: border-color 0.15s, background 0.15s;
}
.mode-pill:hover { border-color: var(--primary-color); }
.mode-pill__caret { font-size: 13px; opacity: 0.6; }

.composer__input { flex: 1; }
/* strip the NInput border — the wrapper box provides it */
.composer__input :deep(.n-input) { background: transparent; }
.composer__input :deep(.n-input__border),
.composer__input :deep(.n-input__state-border) { display: none; }
.composer__input :deep(.n-input-wrapper) { padding-left: 4px; }

.send-btn { flex-shrink: 0; }

.composer__hint {
    text-align: center;
    font-size: 11.5px;
    opacity: 0.5;
    margin: 8px 0 0;
}
.composer__hint kbd {
    font-family: inherit;
    font-size: 10.5px;
    padding: 1px 5px;
    border-radius: 5px;
    border: 1px solid var(--theme-border);
    background: var(--theme-bg-soft);
}

@media (max-width: 560px) {
    .mode-pill__label { display: none; }
}
</style>
