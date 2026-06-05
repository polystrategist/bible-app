import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useAiStore, AiChatMessage, AiError } from './aiStore';

/** The AI tools, folded into the chat as composer "modes". */
export type AiMode = 'chat' | 'insight' | 'sermon-outline' | 'full-sermon' | 'devotional';

export interface ConversationMeta {
    id: string;
    title: string;
    created_at: string;
    updated_at: string;
}

interface SendArgs {
    mode: AiMode;
    /** Main text — chat message, topic/passage, or (for insight) the verse text. */
    text: string;
    /** Insight only: the verse reference (e.g. "John 3:16"). */
    reference?: string;
}

function genId(): string {
    return globalThis.crypto?.randomUUID?.() ?? `c_${Date.now()}_${Math.random().toString(36).slice(2)}`;
}

/** First line / ~48 chars of the first user message, used as the auto title. */
function deriveTitle(messages: AiChatMessage[]): string {
    const first = messages.find((m) => m.role === 'user');
    const raw = (first?.content ?? 'New chat').replace(/\s+/g, ' ').trim();
    return raw.length > 48 ? `${raw.slice(0, 48)}…` : raw || 'New chat';
}

/** Human-readable user-bubble text for a one-shot tool request. */
function userPrompt({ mode, text, reference }: SendArgs): string {
    switch (mode) {
        case 'insight':
            return reference ? `Insight on ${reference}\n${text}` : `Insight\n${text}`;
        case 'sermon-outline':
            return `Sermon outline: ${text}`;
        case 'full-sermon':
            return `Full sermon: ${text}`;
        case 'devotional':
            return `Devotional: ${text}`;
        default:
            return text;
    }
}

/**
 * Owns the AI Assistant chat history: the active conversation's messages plus
 * the saved-conversation list. Persists to the local SQLite `ai_conversations`
 * table via Electron IPC (in-memory only when running outside Electron).
 */
export const useConversationStore = defineStore('aiConversationStore', () => {
    const ai = useAiStore();

    const conversations = ref<ConversationMeta[]>([]);
    const activeId = ref<string | null>(null);
    const activeTitle = ref<string>('');
    const messages = ref<AiChatMessage[]>([]);
    const sending = ref(false);
    const lastError = ref<AiError | null>(null);
    const lastSend = ref<SendArgs | null>(null);

    const persistent = typeof window !== 'undefined' && !!window.browserWindow?.getAiConversations;
    const hasMessages = computed(() => messages.value.length > 0);

    async function loadConversations(): Promise<void> {
        if (!persistent) return;
        try {
            conversations.value = await window.browserWindow.getAiConversations();
        } catch {
            conversations.value = [];
        }
    }

    /** Reset to a blank, unsaved conversation. */
    function newConversation(): void {
        activeId.value = null;
        activeTitle.value = '';
        messages.value = [];
        lastError.value = null;
        lastSend.value = null;
    }

    async function selectConversation(id: string): Promise<void> {
        if (id === activeId.value) return;
        if (!persistent) return;
        const convo = await window.browserWindow.getAiConversation(id);
        if (!convo) return;
        activeId.value = convo.id;
        activeTitle.value = convo.title;
        messages.value = convo.messages as AiChatMessage[];
        lastError.value = null;
        lastSend.value = null;
    }

    async function persist(): Promise<void> {
        if (!persistent || !messages.value.length) return;
        if (!activeId.value) activeId.value = genId();
        if (!activeTitle.value) activeTitle.value = deriveTitle(messages.value);
        try {
            await window.browserWindow.saveAiConversation({
                id: activeId.value,
                title: activeTitle.value,
                // Strip Vue reactive wrappers before crossing IPC — Electron's
                // structured clone throws on reactive proxies.
                messages: messages.value.map((m) => ({ role: m.role, content: m.content })),
            });
            await loadConversations();
        } catch (e) {
            /* persistence is best-effort — chat keeps working in memory */
            console.warn('saveAiConversation failed', e);
        }
    }

    async function renameConversation(id: string, title: string): Promise<void> {
        const trimmed = title.trim();
        if (!trimmed || !persistent) return;
        if (id === activeId.value) activeTitle.value = trimmed;
        const convo = await window.browserWindow.getAiConversation(id);
        if (!convo) return;
        await window.browserWindow.saveAiConversation({ id, title: trimmed, messages: convo.messages });
        await loadConversations();
    }

    async function deleteConversation(id: string): Promise<void> {
        if (persistent) await window.browserWindow.deleteAiConversation(id);
        if (id === activeId.value) newConversation();
        await loadConversations();
    }

    /** Run the request for the active mode and append the assistant reply. */
    async function send(args: SendArgs): Promise<void> {
        if (sending.value) return;
        const text = args.text.trim();
        if (!text) return;

        lastSend.value = args;
        lastError.value = null;
        messages.value.push({ role: 'user', content: userPrompt(args) });
        sending.value = true;
        await persist();

        try {
            let resultText: string;
            switch (args.mode) {
                case 'insight':
                    resultText = (await ai.verseInsight(args.reference?.trim() || text, text)).text;
                    break;
                case 'sermon-outline':
                    resultText = (await ai.sermonOutline(text)).text;
                    break;
                case 'full-sermon':
                    resultText = (await ai.fullSermon(text)).text;
                    break;
                case 'devotional':
                    resultText = (await ai.devotional(text)).text;
                    break;
                default:
                    resultText = (await ai.bibleChat(messages.value)).text;
            }
            messages.value.push({ role: 'assistant', content: resultText });
        } catch (e) {
            lastError.value = e as AiError;
        } finally {
            sending.value = false;
            await persist();
        }
    }

    /** Retry the last send after an error (the user turn is already in place). */
    async function retryLast(): Promise<void> {
        const prev = lastSend.value;
        if (!prev || sending.value) return;
        // Drop the failed user turn so send() can re-add it cleanly.
        if (messages.value.at(-1)?.role === 'user') messages.value.pop();
        await send(prev);
    }

    return {
        conversations,
        activeId,
        activeTitle,
        messages,
        sending,
        lastError,
        hasMessages,
        persistent,
        loadConversations,
        newConversation,
        selectConversation,
        renameConversation,
        deleteConversation,
        send,
        retryLast,
    };
});
