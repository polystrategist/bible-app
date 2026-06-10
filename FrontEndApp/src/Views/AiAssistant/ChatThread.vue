<script lang="ts" setup>
import { ref, watch, nextTick } from 'vue';
import { NButton, NSpin, NTooltip, useMessage } from 'naive-ui';
import { Icon } from '@iconify/vue';
import type { AiChatMessage, AiError } from '../../store/aiStore';
import type { AiMode } from '../../store/conversationStore';
import { renderMarkdown } from '../../util/markdown';

const props = defineProps<{
    messages: AiChatMessage[];
    sending: boolean;
    error: AiError | null;
}>();

const emit = defineEmits<{
    (e: 'suggest', payload: { mode: AiMode; text?: string }): void;
    (e: 'retry'): void;
}>();

const message = useMessage();
const logEl = ref<HTMLElement | null>(null);

// Quick-start tiles shown on the empty state — the old tools, folded into chat.
const tools: Array<{ mode: AiMode; icon: string; title: string; desc: string }> = [
    { mode: 'insight', icon: 'lucide:book-open', title: 'Verse insight', desc: 'Explain a passage in context' },
    { mode: 'sermon-outline', icon: 'lucide:list-tree', title: 'Sermon outline', desc: 'Outline a topic or passage' },
    { mode: 'devotional', icon: 'lucide:sun', title: 'Devotional', desc: 'A short, encouraging reflection' },
];

const examples = [
    'What does it mean to walk by faith?',
    'Summarize the book of James',
    'Compare grace and works in Paul’s letters',
];

function isUser(m: AiChatMessage) {
    return m.role === 'user';
}

function copy(text: string) {
    navigator.clipboard?.writeText(text);
    message.success('Copied to clipboard');
}

function scrollToBottom() {
    nextTick(() => {
        const el = logEl.value;
        if (el) el.scrollTop = el.scrollHeight;
    });
}

watch(
    () => [props.messages.length, props.sending],
    () => scrollToBottom(),
);
</script>

<template>
    <div ref="logEl" class="thread">
        <!-- Empty state -->
        <div v-if="messages.length === 0" class="empty">
            <div class="empty__badge">
                <Icon icon="lucide:sparkles" />
            </div>
            <h2 class="empty__title">How can I help with your study today?</h2>
            <p class="empty__sub">
                Ask anything about the Bible, or start with a tool below.
            </p>

            <div class="tools">
                <button
                    v-for="t in tools"
                    :key="t.mode"
                    class="tool-card"
                    @click="emit('suggest', { mode: t.mode })"
                >
                    <Icon :icon="t.icon" class="tool-card__icon" />
                    <div class="tool-card__title">{{ t.title }}</div>
                    <div class="tool-card__desc">{{ t.desc }}</div>
                </button>
            </div>

            <div class="examples">
                <button
                    v-for="ex in examples"
                    :key="ex"
                    class="example-chip"
                    @click="emit('suggest', { mode: 'chat', text: ex })"
                >
                    <Icon icon="lucide:message-circle" /> <span>{{ ex }}</span>
                </button>
            </div>
        </div>

        <!-- Messages -->
        <div v-else class="messages">
            <template v-for="(m, i) in messages" :key="i">
                <div v-if="isUser(m)" class="row row--user">
                    <div class="bubble bubble--user">{{ m.content }}</div>
                </div>
                <div v-else class="row row--ai">
                    <div class="avatar"><Icon icon="lucide:sparkles" /></div>
                    <div class="ai-block">
                        <div class="bubble bubble--ai markdown-body" v-html="renderMarkdown(m.content)" />
                        <NTooltip trigger="hover">
                            <template #trigger>
                                <NButton size="tiny" quaternary circle class="copy-btn" @click="copy(m.content)">
                                    <template #icon><Icon icon="lucide:copy" /></template>
                                </NButton>
                            </template>
                            Copy
                        </NTooltip>
                    </div>
                </div>
            </template>

            <!-- Typing indicator -->
            <div v-if="sending" class="row row--ai">
                <div class="avatar"><Icon icon="lucide:sparkles" /></div>
                <div class="bubble bubble--ai typing">
                    <span></span><span></span><span></span>
                </div>
            </div>

            <!-- Error with retry -->
            <div v-if="error" class="ai-error-card">
                <Icon :icon="error.isPaywall ? 'lucide:lock' : 'lucide:alert-triangle'" />
                <div class="ai-error-card__body">
                    <strong>{{ error.isPaywall ? 'Upgrade to use this' : 'Something went wrong' }}</strong>
                    <p>{{ error.message }}</p>
                </div>
                <NButton v-if="!error.isPaywall" size="small" secondary @click="emit('retry')">Retry</NButton>
            </div>
        </div>
    </div>
</template>

<style scoped>
.thread {
    flex: 1;
    overflow-y: auto;
    padding: 24px 0 8px;
}

/* ---- Empty state ---- */
.empty {
    max-width: 720px;
    margin: 0 auto;
    padding: 32px 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.empty__badge {
    width: 64px; height: 64px; border-radius: 20px;
    display: grid; place-items: center; margin-bottom: 16px;
    font-size: 30px; color: var(--primary-color);
    background: color-mix(in srgb, var(--primary-color) 15%, transparent);
}
.empty__title { font-size: 24px; font-weight: 700; margin: 0; }
.empty__sub { opacity: 0.7; margin: 8px 0 28px; }

.tools {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    width: 100%;
}
.tool-card {
    text-align: left;
    background: var(--theme-bg-elevated);
    border: 1px solid var(--theme-border);
    border-radius: 14px;
    padding: 16px;
    cursor: pointer;
    transition: border-color 0.15s, transform 0.15s, background 0.15s;
    color: inherit;
}
.tool-card:hover {
    border-color: var(--primary-color);
    transform: translateY(-2px);
    background: var(--theme-bg-soft);
}
.tool-card__icon { font-size: 22px; color: var(--primary-color); }
.tool-card__title { font-weight: 600; margin-top: 10px; }
.tool-card__desc { font-size: 12.5px; opacity: 0.65; margin-top: 2px; line-height: 1.4; }

.examples {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-top: 22px;
}
.example-chip {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 13px;
    padding: 8px 14px;
    border-radius: 999px;
    border: 1px solid var(--theme-border);
    background: var(--theme-bg-elevated);
    color: inherit;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
}
.example-chip:hover { border-color: var(--primary-color); background: var(--theme-bg-soft); }

/* ---- Messages ---- */
.messages {
    max-width: 760px;
    margin: 0 auto;
    padding: 0 16px;
    display: flex;
    flex-direction: column;
    gap: 18px;
}
.row { display: flex; gap: 12px; }
.row--user { justify-content: flex-end; }
.row--ai { justify-content: flex-start; }
.avatar {
    flex-shrink: 0;
    width: 30px; height: 30px; border-radius: 9px;
    display: grid; place-items: center;
    color: var(--primary-color);
    background: color-mix(in srgb, var(--primary-color) 15%, transparent);
}
.ai-block { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.bubble {
    max-width: 100%;
    padding: 11px 14px;
    border-radius: 14px;
    line-height: 1.55;
    white-space: pre-wrap;
    word-break: break-word;
}
.bubble--user {
    background: var(--primary-color);
    color: #fff;
    border-bottom-right-radius: 5px;
    max-width: 78%;
}
.bubble--ai {
    background: var(--theme-bg-elevated);
    border: 1px solid var(--theme-border);
    border-bottom-left-radius: 5px;
}
.bubble--ai.markdown-body { white-space: normal; }
.copy-btn { align-self: flex-start; opacity: 0.55; }
.copy-btn:hover { opacity: 1; }

/* Typing indicator */
.typing { display: inline-flex; gap: 5px; align-items: center; }
.typing span {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--theme-text-soft, currentColor);
    opacity: 0.5;
    animation: blink 1.2s infinite ease-in-out;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink {
    0%, 80%, 100% { opacity: 0.25; transform: translateY(0); }
    40% { opacity: 1; transform: translateY(-3px); }
}

.ai-error-card {
    display: flex;
    align-items: center;
    gap: 12px;
    border: 1px solid #d8a23a55;
    background: #d8a23a14;
    border-radius: 12px;
    padding: 12px 14px;
    max-width: 760px;
    margin: 0 auto;
}
.ai-error-card > svg { font-size: 20px; color: #d8a23a; flex-shrink: 0; }
.ai-error-card__body { flex: 1; }
.ai-error-card__body p { margin: 2px 0 0; font-size: 13px; opacity: 0.85; }

/* Rendered Markdown */
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) { font-weight: 700; line-height: 1.3; margin: 14px 0 6px; }
.markdown-body :deep(h2) { font-size: 18px; }
.markdown-body :deep(h3) { font-size: 16px; }
.markdown-body :deep(h4) { font-size: 14.5px; }
.markdown-body :deep(h5), .markdown-body :deep(h6) { font-size: 13px; opacity: 0.9; }
.markdown-body :deep(p) { margin: 8px 0; line-height: 1.6; }
.markdown-body :deep(ul), .markdown-body :deep(ol) { margin: 8px 0; padding-left: 22px; }
.markdown-body :deep(li) { margin: 3px 0; line-height: 1.5; }
.markdown-body :deep(strong) { font-weight: 700; }
.markdown-body :deep(em) { font-style: italic; }
.markdown-body :deep(code) {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 0.9em; background: rgba(127, 127, 127, 0.15);
    padding: 1px 5px; border-radius: 5px;
}
.markdown-body :deep(blockquote) {
    margin: 8px 0; padding: 4px 12px;
    border-left: 3px solid rgba(127, 127, 127, 0.4); opacity: 0.9;
}
.markdown-body :deep(> :first-child) { margin-top: 0; }
.markdown-body :deep(> :last-child) { margin-bottom: 0; }

@media (max-width: 720px) {
    .tools { grid-template-columns: 1fr; }
}
</style>
