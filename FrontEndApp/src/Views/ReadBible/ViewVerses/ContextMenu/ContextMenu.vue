<script setup lang="ts">
import { NIcon, NPopover, NModal, NSpin, NButton, useMessage } from 'naive-ui';
import { Sparkle24Regular } from '@vicons/fluent';
import { BookmarkFilled } from '@vicons/carbon';
import { Icon } from '@iconify/vue';
import { onClickOutside } from '@vueuse/core';
import { ref, computed, nextTick, watch, type PropType } from 'vue';
import { AiContextMenuOptions, ContextMenuOptions, ClearHighlightOption } from './ContextMenuOptions';
import { useBookmarkStore } from '../../../../store/bookmark';
import { useBibleStore } from '../../../../store/BibleStore';
import { useAiStore, AiError } from '../../../../store/aiStore';
import { useAuthStore } from '../../../../store/authStore';
import { usePlanModalStore } from '../../../../store/planModalStore';
import { useConversationStore } from '../../../../store/conversationStore';
import { useMenuStore } from '../../../../store/menu';
import { debouncedRunSync } from '../../../../util/Sync/sync';
import { renderMarkdown } from '../../../../util/markdown';
import { stripVerseHtml } from '../../../../util/helper';
import { colors } from '../../../../util/highlighter';

const bibleStore = useBibleStore();
const aiStore = useAiStore();
const authStore = useAuthStore();
const planModal = usePlanModalStore();
const convo = useConversationStore();
const menuStore = useMenuStore();
const message = useMessage();
const contextMenuRef = ref(null);
const emits = defineEmits(['close', 'create-clip-note']);
const bookmarkStore = useBookmarkStore();
const showColorPicker = ref(false);

// ─── AI Insight / Sermon ────────────────────────────────────────────────────
type AiKind = 'insight' | 'sermon';
const showAiModal = ref(false);
const aiKind = ref<AiKind>('insight');
const aiReference = ref('');
const aiVersion = ref<string | undefined>(undefined);
const aiVerseText = ref('');
const aiLoading = ref(false);
const aiResult = ref('');
const aiError = ref('');
const aiUpgrade = ref(false);
const aiCopied = ref(false);

const aiTitle = computed(() =>
    aiKind.value === 'sermon'
        ? `Sermon · ${aiReference.value}`
        : `AI Insight · ${aiReference.value}`,
);

// Cache key for the local ai_insights store: mode + reference + (insight) version.
function aiCacheKey(): string {
    return `${aiKind.value}:${aiReference.value}:${aiVersion.value ?? ''}`;
}

/**
 * Open the AI modal for the current verse in [kind] mode. Serves a fresh cached
 * result when present; otherwise calls the API and caches the result (3-day TTL,
 * handled by the local cache). Pass `force` to bypass the cache (regenerate).
 */
async function runAi(kind: AiKind, opts: { force?: boolean } = {}) {
    const d: any = props.data;
    aiKind.value = kind;
    aiReference.value = `${bibleStore.selectedBook.title} ${d.chapter}:${d.verse}`;
    aiVersion.value =
        kind === 'insight' && typeof d.bibleVersion === 'string'
            ? d.bibleVersion.replace(/\.SQLite3$/i, '')
            : undefined;
    aiVerseText.value = stripVerseHtml(d.text ?? '');
    aiResult.value = '';
    aiError.value = '';
    aiUpgrade.value = false;
    aiCopied.value = false;
    showAiModal.value = true;

    // AI is a Pro feature — surface the upgrade prompt without a failed request.
    if (!authStore.isAiEnabled) {
        aiUpgrade.value = true;
        return;
    }

    // Serve from the local cache unless the user asked to regenerate.
    if (!opts.force) {
        try {
            const cached = await window.browserWindow.getAiInsight(aiCacheKey());
            if (cached?.content) {
                aiResult.value = cached.content;
                return;
            }
        } catch {
            /* a cache miss/error is non-fatal — fall through to the API */
        }
    }

    aiLoading.value = true;
    try {
        const res =
            kind === 'sermon'
                ? await aiStore.sermonOutline(aiReference.value)
                : await aiStore.verseInsight(
                      aiReference.value,
                      aiVerseText.value,
                      aiVersion.value,
                  );
        aiResult.value = res.text;
        try {
            await window.browserWindow.saveAiInsight({
                key: aiCacheKey(),
                mode: kind,
                reference: aiReference.value,
                version: aiVersion.value ?? null,
                content: res.text,
            });
        } catch {
            /* best-effort cache write (no-op on web) */
        }
    } catch (e) {
        if (e instanceof AiError && e.isPaywall) {
            aiUpgrade.value = true;
        } else {
            aiError.value =
                e instanceof AiError ? e.message : 'Could not load. Please try again.';
        }
    } finally {
        aiLoading.value = false;
    }
}

const runAiInsight = () => runAi('insight');
const runAiSermon = () => runAi('sermon');
function regenerateAi() {
    runAi(aiKind.value, { force: true });
}

async function copyAiResult() {
    try {
        await navigator.clipboard.writeText(aiResult.value);
        aiCopied.value = true;
        setTimeout(() => (aiCopied.value = false), 1500);
    } catch {
        /* clipboard unavailable */
    }
}

// Carry the generated result into a new AI chat so the user can ask follow-ups.
async function continueInChat() {
    const userContent =
        aiKind.value === 'sermon'
            ? `Sermon outline: ${aiReference.value}`
            : `Insight on ${aiReference.value}`;
    await convo.seedConversation([
        { role: 'user', content: userContent },
        { role: 'assistant', content: aiResult.value },
    ]);
    showAiModal.value = false;
    emits('close');
    await menuStore.setMenu('/ai-assistant');
}

// From the AI upsell → open the global Choose-your-plan dialog.
function openPlansFromUpsell() {
    showAiModal.value = false;
    planModal.show();
}

const props = defineProps({
    showContextMenu: {
        type: Boolean,
        default: false,
    },
    x: {
        type: Number,
        default: 0,
    },
    y: {
        type: Number,
        default: 0,
    },
    data: {
        type: Object,
        default: {},
    },
    selectedVersesData: {
        type: Array as PropType<any[]>,
        default: () => [],
    },
});

// Clamped open position. The parent passes the raw cursor x/y; a tall menu
// opened near the right/bottom edge would otherwise spill off-screen, so once
// the menu is rendered we measure it and pull it back inside the viewport.
const posX = ref(0);
const posY = ref(0);

watch(
    () => [props.showContextMenu, props.x, props.y] as const,
    async ([show, x, y]) => {
        if (!show) return;
        posX.value = x;
        posY.value = y;
        await nextTick();
        const el = contextMenuRef.value as HTMLElement | null;
        if (!el) return;
        const margin = 10;
        const vw = window.innerWidth;
        const vh = window.innerHeight;
        const { offsetWidth: w, offsetHeight: h } = el;
        if (x + w + margin > vw) posX.value = Math.max(margin, vw - w - margin);
        if (y + h + margin > vh) posY.value = Math.max(margin, vh - h - margin);
    },
    { immediate: true },
);

// Whether every target verse is already bookmarked — flips the bookmark row
// to an "Unbookmark" (remove) action.
const isBookmarked = computed(() => {
    const verses =
        props.selectedVersesData.length > 0 ? props.selectedVersesData : [props.data];
    if (verses.length === 0) return false;
    return verses.every(
        (v) =>
            v &&
            bookmarkStore.isBookmarkExists(`${v.book_number}_${v.chapter}_${v.verse}`),
    );
});

// Whether the target verse(s) currently carry a highlight — gates the
// "Clear Highlight" row so it only appears when there's something to clear.
const hasHighlight = computed(() => {
    const verses =
        props.selectedVersesData.length > 0 ? props.selectedVersesData : [props.data];
    const map = bibleStore.chapterHighlights as any;
    return verses.some((v) => {
        if (!v) return false;
        const key = `${v.book_number}_${v.chapter}_${v.verse}`;
        return !!(map?.[key] || (v.key && map?.[v.key]));
    });
});

// Write [text] to the clipboard, preferring Electron's native clipboard. The
// renderer's navigator.clipboard is unreliable on desktop (it needs a secure
// context/focus and silently rejects — the cause of "Could not copy"), so route
// through the IPC bridge first and only fall back to the web API.
async function writeToClipboard(text: string): Promise<void> {
    const bridge = window.browserWindow as any;
    if (bridge?.writeClipboard) {
        await bridge.writeClipboard(text);
        return;
    }
    await navigator.clipboard.writeText(text);
}

// Copy the selected verse(s) as `"text" Book chapter:verse` to the clipboard.
// With no multi-selection this copies props.data — the verse the context menu
// was opened on.
async function copyVerses() {
    const book = bibleStore.selectedBook.title;
    const verses =
        props.selectedVersesData.length > 0 ? props.selectedVersesData : [props.data];
    const sorted = [...verses].sort((a, b) => (a.verse ?? 0) - (b.verse ?? 0));
    const text = sorted
        .map((v) => `"${stripVerseHtml(v.text ?? '')}" ${book} ${v.chapter}:${v.verse}`)
        .join('\n');
    try {
        await writeToClipboard(text);
        message.success(verses.length > 1 ? 'Verses copied' : 'Verse copied');
    } catch {
        message.error('Could not copy. Please try again.');
    }
}

async function highlightVerse(color: string) {
    const verses = props.selectedVersesData.length > 0 ? props.selectedVersesData : [props.data];
    for (const verseData of verses) {
        const { book_number, chapter, verse } = verseData;
        const key = `${book_number}_${chapter}_${verse}`;
        await window.browserWindow.saveHighlight(
            JSON.stringify({ key, book_number, chapter, verse, content: color }),
        );
    }
    await bibleStore.getChapterHighlights();
    debouncedRunSync();
    showColorPicker.value = false;
    emits('close');
}

async function clickContextMenu(key: string) {
    if (key == 'ai-insight') {
        emits('close');
        runAiInsight();
        return;
    } else if (key == 'ai-sermon') {
        emits('close');
        runAiSermon();
        return;
    } else if (key == 'add-to-bookmark') {
        const verses = props.selectedVersesData.length > 0 ? props.selectedVersesData : [props.data];
        if (isBookmarked.value) {
            for (const verseData of verses) {
                await window.browserWindow.deleteBookmark(JSON.stringify(verseData));
            }
            await bookmarkStore.getBookmarks();
        } else {
            for (const verseData of verses) {
                bookmarkStore.bookmarks = await window.browserWindow.saveBookMark(
                    JSON.stringify(verseData),
                );
            }
        }
        debouncedRunSync();
    } else if (key == 'copy-verse') {
        await copyVerses();
    } else if (key == 'create-clip-note') {
        emits('create-clip-note', props.data);
    } else if (key == 'highlight-verse') {
        showColorPicker.value = !showColorPicker.value;
        return; // Don't close menu
    } else if (key == 'compare-verse') {
        (window as any).browserWindow.openCompareVerseWindow({
            book_number: props.data.book_number,
            chapter: props.data.chapter,
            verse: props.data.verse,
            book_name: bibleStore.selectedBook.title,
        });
    } else if (key == 'clear-highlight') {
        const verses = props.selectedVersesData.length > 0 ? props.selectedVersesData : [props.data];
        for (const verseData of verses) {
            const verseKey = `${verseData.book_number}_${verseData.chapter}_${verseData.verse}`;
            await bibleStore.removeHighlightInDb(verseKey);
            await bibleStore.removeHighlightInDb(verseData.key);
        }
    }
    showColorPicker.value = false;
    emits('close');
}
onClickOutside(contextMenuRef, (event) => {
    showColorPicker.value = false;
    emits('close');
});
</script>
<template>
    <NPopover
        :show="showContextMenu"
        :x="posX"
        :y="posY"
        placement="bottom-start"
        trigger="manual"
        content-style="padding: 0 !important;"
        class="!p-0 !rounded-md"
    >
        <div
            ref="contextMenuRef"
            class="cm-root flex flex-col select-none"
        >
            <!-- ── Verse Actions ──────────────────────────────────── -->
            <div class="cm-section-label">{{ $t('Verse Actions') }}</div>
            <template v-for="option in ContextMenuOptions" :key="option.key">
                <div class="cm-action" @click="clickContextMenu(option.key)">
                    <div
                        class="cm-action__icon"
                        :style="{ color: option.color, background: `${option.color}1f` }"
                    >
                        <NIcon
                            size="17"
                            :component="option.key === 'add-to-bookmark' && isBookmarked ? BookmarkFilled : option.icon"
                        />
                    </div>
                    <span class="cm-action__label">
                        {{ option.key === 'add-to-bookmark' && isBookmarked ? 'Unbookmark' : $t(option.label) }}
                    </span>
                    <Icon icon="lucide:chevron-right" class="cm-action__chev" />
                </div>
                <!-- Color picker drops in directly under Highlight Verse. -->
                <div
                    v-if="showColorPicker && option.key === 'highlight-verse'"
                    class="cm-colors"
                >
                    <button
                        v-for="c in colors"
                        :key="c.color"
                        :style="`background: ${c.color}`"
                        class="h-24px w-24px rounded-full cursor-pointer border-2 border-transparent hover:border-white transition-all hover:scale-110"
                        :title="c.name"
                        @click="highlightVerse(c.color)"
                    ></button>
                </div>
            </template>

            <!-- ── AI Tools ───────────────────────────────────────── -->
            <div class="cm-section-label cm-section-label--ai">
                <Icon icon="lucide:sparkles" /> {{ $t('AI Tools') }}
            </div>
            <div
                v-for="option in AiContextMenuOptions"
                :key="option.key"
                class="ai-grad-card"
                @click="clickContextMenu(option.key)"
            >
                <div class="ai-grad-card__icon">
                    <NIcon size="18" :component="option.icon" />
                </div>
                <div class="flex flex-col leading-tight min-w-0 flex-1">
                    <span class="text-size-14px font-700 whitespace-nowrap">{{ $t(option.label) }}</span>
                    <span v-if="option.description" class="text-size-11px ai-grad-card__desc">
                        {{ option.description }}
                    </span>
                </div>
                <span class="ai-grad-card__badge">AI</span>
            </div>

            <!-- ── Clear Highlight (destructive) ──────────────────── -->
            <template v-if="hasHighlight">
            <div class="cm-divider"></div>
            <div
                class="cm-action cm-action--danger"
                @click="clickContextMenu(ClearHighlightOption.key)"
            >
                <div
                    class="cm-action__icon"
                    :style="{ color: ClearHighlightOption.color, background: `${ClearHighlightOption.color}1f` }"
                >
                    <NIcon size="17" :component="ClearHighlightOption.icon" />
                </div>
                <div class="flex flex-col leading-tight min-w-0 flex-1">
                    <span class="cm-action__label">{{ $t(ClearHighlightOption.label) }}</span>
                    <span v-if="ClearHighlightOption.description" class="text-size-11px opacity-55">
                        {{ ClearHighlightOption.description }}
                    </span>
                </div>
                <Icon icon="lucide:chevron-right" class="cm-action__chev" />
            </div>
            </template>
        </div>
    </NPopover>

    <!-- AI Insight / Sermon modal -->
    <NModal
        v-model:show="showAiModal"
        preset="card"
        :title="aiTitle"
        :bordered="false"
        style="max-width: 560px; width: 92vw;"
    >
        <!-- Regenerate (top-right) — only once a result is shown. -->
        <template v-if="aiResult && !aiLoading" #header-extra>
            <NButton quaternary circle size="small" title="Regenerate" @click="regenerateAi">
                <template #icon><Icon icon="lucide:refresh-cw" /></template>
            </NButton>
        </template>

        <div v-if="aiLoading" class="ai-insight-loading">
            <NSpin size="small" />
            <span>{{ aiKind === 'sermon' ? 'Drafting sermon…' : 'Generating insight…' }}</span>
        </div>

        <div v-else-if="aiUpgrade" class="ai-insight-upsell">
            <div class="ai-insight-upsell__glow">
                <NIcon size="30" :component="Sparkle24Regular" />
            </div>
            <p class="ai-insight-upsell__title">
                {{ aiKind === 'sermon' ? 'Sermons are part of Pro' : 'AI Insight is part of Pro' }}
            </p>
            <p class="ai-insight-upsell__text">
                Go deeper in the Word with Believers Sword <strong>Pro</strong>:
            </p>
            <ul class="ai-insight-upsell__features">
                <li><Icon icon="lucide:check" /> <span>Plain-language verse explanations</span></li>
                <li><Icon icon="lucide:check" /> <span>Original-language (Hebrew &amp; Greek) word studies</span></li>
                <li><Icon icon="lucide:check" /> <span>Sermon outlines from any verse</span></li>
                <li><Icon icon="lucide:check" /> <span>AI Bible chat &amp; devotionals</span></li>
            </ul>
            <NButton type="primary" size="medium" class="ai-insight-upsell__cta" @click="openPlansFromUpsell">
                <template #icon><Icon icon="lucide:sparkles" /></template>
                View plans
            </NButton>
        </div>

        <p v-else-if="aiError" class="ai-insight-error">{{ aiError }}</p>

        <template v-else>
            <div class="ai-insight-scroll">
                <div class="ai-insight-text markdown-body" v-html="renderMarkdown(aiResult)" />
            </div>
            <div class="ai-insight-actions">
                <NButton size="small" secondary @click="copyAiResult">
                    <template #icon>
                        <Icon :icon="aiCopied ? 'lucide:check' : 'lucide:copy'" />
                    </template>
                    {{ aiCopied ? 'Copied' : 'Copy' }}
                </NButton>
                <NButton size="small" type="primary" @click="continueInChat">
                    <template #icon><Icon icon="lucide:message-circle" /></template>
                    Continue in chat
                </NButton>
            </div>
        </template>
    </NModal>
</template>

<style scoped>
.ai-insight-loading {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    opacity: 0.8;
}

/* Result scrolls within the modal so long sermons/insights don't overflow. */
.ai-insight-scroll {
    max-height: 60vh;
    overflow-y: auto;
    padding-right: 6px;
    margin: -2px -2px 0;
}
.ai-insight-text {
    font-size: 14px;
    line-height: 1.55;
}

/* Rendered Markdown (mirrors the AI chat thread's .markdown-body). */
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4),
.markdown-body :deep(h5),
.markdown-body :deep(h6) {
    font-weight: 700;
    line-height: 1.3;
    margin: 14px 0 6px;
}
.markdown-body :deep(h2) { font-size: 18px; }
.markdown-body :deep(h3) { font-size: 16px; }
.markdown-body :deep(h4) { font-size: 14.5px; }
.markdown-body :deep(h5),
.markdown-body :deep(h6) { font-size: 13px; opacity: 0.9; }
.markdown-body :deep(p) { margin: 8px 0; line-height: 1.6; }
.markdown-body :deep(ul),
.markdown-body :deep(ol) { margin: 8px 0; padding-left: 22px; }
.markdown-body :deep(li) { margin: 3px 0; line-height: 1.5; }
.markdown-body :deep(strong) { font-weight: 700; }
.markdown-body :deep(em) { font-style: italic; }
.markdown-body :deep(code) {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 0.88em;
    padding: 1px 5px;
    border-radius: 5px;
    background: color-mix(in srgb, currentColor 10%, transparent);
}
.markdown-body :deep(blockquote) {
    margin: 8px 0;
    padding-left: 12px;
    border-left: 3px solid var(--primary-color);
    opacity: 0.9;
}
.markdown-body :deep(> :first-child) { margin-top: 0; }
.markdown-body :deep(> :last-child) { margin-bottom: 0; }

.ai-insight-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid var(--theme-border, rgba(127, 127, 127, 0.2));
}

/* ── Verse context menu layout ────────────────────────────────────────── */
.cm-root {
    width: 248px;
    padding: 8px;
    gap: 2px;
    /* Full height normally; only scrolls if the window is too short to fit. */
    max-height: calc(100vh - 20px);
    overflow-y: auto;
}

/* Small uppercase section heading ("Verse Actions" / "AI Tools"). */
.cm-section-label {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 8px 5px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    opacity: 0.5;
}
.cm-section-label--ai {
    margin-top: 6px;
    color: #8b5cf6;
    opacity: 1;
}
.cm-section-label--ai .iconify {
    font-size: 14px;
}

/* Primary action row — tinted icon tile, label, trailing chevron. */
.cm-action {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 8px 10px;
    border-radius: 11px;
    cursor: pointer;
    transition: background 0.13s ease;
}
.cm-action:hover {
    background: color-mix(in srgb, var(--primary-color) 14%, transparent);
}
.cm-action__icon {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    display: grid;
    place-items: center;
    border-radius: 9px;
}
.cm-action__label {
    flex: 1;
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
}
.cm-action__chev {
    flex-shrink: 0;
    font-size: 15px;
    opacity: 0.35;
}
.cm-action--danger:hover {
    background: rgba(239, 68, 68, 0.12);
}
.cm-action--danger .cm-action__label {
    color: #ef4444;
}

.cm-divider {
    height: 1px;
    margin: 6px 4px;
    background: color-mix(in srgb, currentColor 14%, transparent);
}

.cm-colors {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 8px 10px 10px;
}

/* AI actions in the verse context menu — premium blue→purple gradient cards. */
.ai-grad-card {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 9px 10px;
    margin-bottom: 4px;
    border-radius: 12px;
    cursor: pointer;
    background: linear-gradient(
        135deg,
        rgba(59, 130, 246, 0.12),
        rgba(139, 92, 246, 0.12)
    );
    border: 1px solid rgba(139, 92, 246, 0.30);
    transition: filter 0.15s ease;
}
.ai-grad-card:hover {
    filter: brightness(1.08);
}
.ai-grad-card__icon {
    flex-shrink: 0;
    width: 34px;
    height: 34px;
    display: grid;
    place-items: center;
    border-radius: 9px;
    color: #fff;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
}
.ai-grad-card__desc {
    opacity: 0.65;
    white-space: normal;
    line-height: 1.3;
}
.ai-grad-card__badge {
    flex-shrink: 0;
    align-self: flex-start;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.03em;
    color: #c4b5fd;
    background: rgba(139, 92, 246, 0.22);
}

.ai-insight-error {
    margin: 0;
    font-size: 13px;
    color: #f87171;
}

.ai-insight-upsell {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 8px;
    padding: 4px 4px 8px;
}

.ai-insight-upsell__glow {
    width: 64px;
    height: 64px;
    display: grid;
    place-items: center;
    border-radius: 18px;
    color: var(--primary-color);
    background: color-mix(in srgb, var(--primary-color) 16%, transparent);
}

.ai-insight-upsell__title {
    margin: 6px 0 0;
    font-weight: 700;
    font-size: 16px;
}

.ai-insight-upsell__text {
    margin: 0;
    font-size: 13px;
    line-height: 1.45;
    opacity: 0.85;
}

.ai-insight-upsell__features {
    list-style: none;
    margin: 4px 0 6px;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 7px;
    text-align: left;
    width: 100%;
    max-width: 360px;
}
.ai-insight-upsell__features li {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 13px;
    line-height: 1.35;
}
.ai-insight-upsell__features li .iconify {
    margin-top: 2px;
    color: #2e8b68;
    flex-shrink: 0;
}

.ai-insight-upsell__cta {
    margin-top: 6px;
    min-width: 180px;
}
</style>
