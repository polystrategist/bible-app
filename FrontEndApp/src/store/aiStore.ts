import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from './authStore';

const API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL}/api`;

export interface AiChatMessage {
    role: 'user' | 'assistant';
    content: string;
}

export type AiErrorCode =
    | 'subscription_required'
    | 'upgrade_required'
    | 'rate_limited'
    | 'unavailable'
    | 'network'
    | 'unknown';

export class AiError extends Error {
    code: AiErrorCode;
    resetAt: string | null;
    constructor(code: AiErrorCode, message: string, resetAt: string | null = null) {
        super(message);
        this.code = code;
        this.resetAt = resetAt;
    }
    /** Free-tier or feature-cost errors should surface the upgrade prompt. */
    get isPaywall(): boolean {
        return this.code === 'subscription_required' || this.code === 'upgrade_required';
    }
}

export interface AiResult {
    text: string;
    remaining: number | null;
    resetAt: string | null;
}

/**
 * AI Assistant client (read-only entitlement on desktop/web — the backend
 * gates every call by the verified tier). Mirrors the Flutter `AiService`.
 */
export const useAiStore = defineStore('aiStore', () => {
    const authStore = useAuthStore();

    // Latest usage metadata for the credits bar.
    const remaining = ref<number | null>(null);
    const resetAt = ref<string | null>(null);

    async function post(path: string, body: Record<string, unknown>): Promise<AiResult> {
        if (!authStore.token) {
            throw new AiError('unknown', 'Please sign in to use AI.');
        }
        try {
            const res = await axios.post(`${API_BASE_URL}/ai/${path}`, body, {
                headers: { Authorization: `Bearer ${authStore.token}` },
            });
            const data = res.data ?? {};
            remaining.value = typeof data.remaining === 'number' ? data.remaining : remaining.value;
            resetAt.value = data.reset_at ?? resetAt.value;
            return { text: data?.data?.text ?? '', remaining: data.remaining ?? null, resetAt: data.reset_at ?? null };
        } catch (e: unknown) {
            throw toAiError(e);
        }
    }

    function toAiError(e: unknown): AiError {
        if (axios.isAxiosError(e)) {
            if (e.response) {
                const d = e.response.data ?? {};
                const code = (d.code as AiErrorCode) ?? 'unknown';
                return new AiError(code, d.message ?? 'AI request failed.', d.reset_at ?? null);
            }
            return new AiError('network', "Couldn't reach the server. Please try again.");
        }
        return e instanceof AiError ? e : new AiError('unknown', 'Something went wrong.');
    }

    const verseInsight = (reference: string, verseText: string, bibleVersion?: string) =>
        post('verse-insight', { reference, verse_text: verseText, bible_version: bibleVersion });
    const sermonOutline = (topicOrPassage: string) =>
        post('sermon-outline', { topic_or_passage: topicOrPassage });
    const fullSermon = (topicOrPassage: string) =>
        post('full-sermon', { topic_or_passage: topicOrPassage });
    const devotional = (topicOrReference: string) =>
        post('devotional', { topic_or_reference: topicOrReference });

    /**
     * Multi-turn chat. Stateless on the client — the caller passes the full
     * message history each turn and the conversation state is owned by the
     * conversation store (so it can be persisted to SQLite).
     */
    const bibleChat = (messages: AiChatMessage[]) =>
        post('bible-chat', { messages });

    return {
        remaining,
        resetAt,
        verseInsight,
        sermonOutline,
        fullSermon,
        devotional,
        bibleChat,
    };
});
