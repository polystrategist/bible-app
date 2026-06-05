<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { NButton, NTooltip, NPopover, NSwitch } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { useAuthStore } from '../../store/authStore';
import { useConversationStore, type AiMode } from '../../store/conversationStore';
import AiPaywall from './AiPaywall.vue';
import ConversationSidebar from './ConversationSidebar.vue';
import ChatThread from './ChatThread.vue';
import ChatComposer from './ChatComposer.vue';

const authStore = useAuthStore();
const convo = useConversationStore();

const collapsed = ref(false);
const composerText = ref('');
const composerReference = ref('');
const composerMode = ref<AiMode>('chat');

// Conversation sync is a paid-tier extra layered on the local history; on by
// default, so users back up their chats unless they explicitly opt out.
// Hidden on web — the web build talks to the backend directly, so there's no
// local history to back up and the toggle is meaningless there.
const syncEnabled = ref(true);
const syncAvailable = computed(() => window.isElectron && convo.persistent && authStore.isSyncEntitled);

onMounted(async () => {
    if (!authStore.isAiEnabled) return;
    await convo.loadConversations();
    if (convo.persistent) {
        const stored = await window.browserWindow.getSyncSetting('ai_conversations_sync');
        // No stored preference yet → default on and persist it.
        if (stored === null || stored === undefined) {
            syncEnabled.value = true;
            await window.browserWindow.setSyncSetting('ai_conversations_sync', true);
        } else {
            syncEnabled.value = Boolean(stored);
        }
    }
});

function onSend(payload: { mode: AiMode; text: string; reference: string }) {
    convo.send(payload);
    composerText.value = '';
    composerReference.value = '';
}

// A tile/chip on the empty state: switch mode and optionally prefill the input.
function onSuggest(payload: { mode: AiMode; text?: string }) {
    composerMode.value = payload.mode;
    composerText.value = payload.text ?? '';
    if (payload.mode !== 'insight') composerReference.value = '';
}

function onNew() {
    convo.newConversation();
    composerText.value = '';
    composerReference.value = '';
    composerMode.value = 'chat';
}

async function onToggleSync(value: boolean) {
    syncEnabled.value = value;
    if (convo.persistent) {
        await window.browserWindow.setSyncSetting('ai_conversations_sync', value);
    }
}
</script>

<template>
    <div class="ai-page">
        <AiPaywall v-if="!authStore.isAiEnabled" />

        <div v-else class="ai-shell">
            <ConversationSidebar
                v-if="!collapsed"
                :conversations="convo.conversations"
                :active-id="convo.activeId"
                @new="onNew"
                @select="convo.selectConversation"
                @rename="convo.renameConversation($event.id, $event.title)"
                @delete="convo.deleteConversation"
                @collapse="collapsed = true"
            />

            <section class="ai-main">
                <header class="ai-main__header">
                    <NTooltip v-if="collapsed" trigger="hover">
                        <template #trigger>
                            <NButton quaternary circle size="small" @click="collapsed = false">
                                <template #icon><Icon icon="lucide:panel-left-open" /></template>
                            </NButton>
                        </template>
                        Show conversations
                    </NTooltip>
                    <div class="ai-main__title">
                        <Icon icon="lucide:sparkles" class="ai-main__title-icon" />
                        {{ convo.activeTitle || 'AI Assistant' }}
                    </div>
                    <NTooltip v-if="collapsed" trigger="hover">
                        <template #trigger>
                            <NButton quaternary circle size="small" @click="onNew">
                                <template #icon><Icon icon="lucide:plus" /></template>
                            </NButton>
                        </template>
                        New chat
                    </NTooltip>

                    <NPopover v-if="syncAvailable" trigger="click" placement="bottom-end" :show-arrow="false">
                        <template #trigger>
                            <NButton quaternary circle size="small">
                                <template #icon><Icon icon="lucide:settings-2" /></template>
                            </NButton>
                        </template>
                        <div class="ai-settings">
                            <label class="ai-settings__row">
                                <span class="ai-settings__label">
                                    <Icon icon="lucide:refresh-cw" />
                                    Sync conversations
                                </span>
                                <NSwitch :value="syncEnabled" size="small" @update:value="onToggleSync" />
                            </label>
                            <p class="ai-settings__hint">Back up &amp; access this chat history on your other devices.</p>
                        </div>
                    </NPopover>
                </header>

                <ChatThread
                    :messages="convo.messages"
                    :sending="convo.sending"
                    :error="convo.lastError"
                    @suggest="onSuggest"
                    @retry="convo.retryLast"
                />

                <ChatComposer
                    v-model:text="composerText"
                    v-model:reference="composerReference"
                    v-model:mode="composerMode"
                    :sending="convo.sending"
                    @send="onSend"
                />
            </section>
        </div>
    </div>
</template>

<style scoped>
.ai-page { height: 100%; }
.ai-shell { display: flex; height: 100%; }

.ai-main {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    height: 100%;
    background: var(--theme-bg-main);
}
.ai-main__header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    border-bottom: 1px solid var(--theme-border);
    flex-shrink: 0;
}
.ai-main__title {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.ai-main__title-icon { color: var(--primary-color); flex-shrink: 0; }

.ai-settings { width: 230px; }
.ai-settings__row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    cursor: pointer;
    font-size: 13px;
}
.ai-settings__label { display: inline-flex; align-items: center; gap: 7px; }
.ai-settings__hint { font-size: 11px; opacity: 0.55; margin: 8px 0 0; line-height: 1.4; }
</style>
