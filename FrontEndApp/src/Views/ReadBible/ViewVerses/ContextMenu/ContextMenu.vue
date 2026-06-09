<script setup lang="ts">
import { NIcon, NPopover, NModal, NSpin, NButton } from 'naive-ui';
import { Sparkle24Regular } from '@vicons/fluent';
import { Icon } from '@iconify/vue';
import { onClickOutside } from '@vueuse/core';
import { ref, computed, type PropType } from 'vue';
import { AiContextMenuOptions, ContextMenuOptions } from './ContextMenuOptions';
import { useBookmarkStore } from '../../../../store/bookmark';
import { useBibleStore } from '../../../../store/BibleStore';
import { useAiStore, AiError } from '../../../../store/aiStore';
import { useAuthStore } from '../../../../store/authStore';
import { usePlanModalStore } from '../../../../store/planModalStore';
import { useConversationStore } from '../../../../store/conversationStore';
import { useMenuStore } from '../../../../store/menu';
import { debouncedRunSync } from '../../../../util/Sync/sync';
import { colors } from '../../../../util/highlighter';

const bibleStore = useBibleStore();
const aiStore = useAiStore();
const authStore = useAuthStore();
const planModal = usePlanModalStore();
const convo = useConversationStore();
const menuStore = useMenuStore();
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

function stripVerseMarkup(text: string): string {
    return (text ?? '')
        .replace(/<[^>]*>/g, ' ') // tags (<S>, <J>, <f>…)
        .replace(/\s+/g, ' ')
        .trim();
}

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
    aiVerseText.value = stripVerseMarkup(d.text ?? '');
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
        for (const verseData of verses) {
            bookmarkStore.bookmarks = await window.browserWindow.saveBookMark(
                JSON.stringify(verseData),
            );
        }
        debouncedRunSync();
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
        :x="x"
        :y="y"
        trigger="manual"
        content-style="padding: 0 !important;"
        class="!p-0 !rounded-md"
    >
        <div
            ref="contextMenuRef"
            class="w-220px max-h-300px overflow-y-auto overflowing-div flex flex-col select-none p-5px"
        >
            <!-- AI actions, grouped + accented at the top so they're easy to find -->
            <div class="flex items-center gap-5px px-7px pt-3px pb-2px">
                <NIcon size="12" :component="Sparkle24Regular" class="ai-group-label__icon" />
                <span class="text-size-10px font-700 uppercase tracking-wide ai-group-label">AI Tools</span>
            </div>
            <div
                v-for="option in AiContextMenuOptions"
                :key="option.key"
                class="ai-menu-item flex items-start pt-4px pb-2px pl-7px pr-1 cursor-pointer rounded-sm"
                @click="clickContextMenu(option.key)"
            >
                <div class="w-25px pt-2px">
                    <NIcon size="15" :component="option.icon" class="ai-menu-item__icon" />
                </div>
                <div class="flex flex-col leading-tight">
                    <span class="text-size-15px whitespace-nowrap">{{ $t(option.label) }}</span>
                    <span v-if="option.description" class="text-size-11px opacity-60">
                        {{ option.description }}
                    </span>
                </div>
            </div>

            <div class="h-1px bg-gray-500 bg-opacity-20 my-4px mx-2px"></div>

            <div
                v-for="option in ContextMenuOptions"
                :key="option.key"
                class="flex items-start pt-4px pb-2px pl-7px pr-1 cursor-pointer hover:bg-[var(--primary-color)] hover:text-dark-500 rounded-sm"
                @click="clickContextMenu(option.key)"
            >
                <div class="w-25px pt-2px">
                    <NIcon size="15" :component="option.icon" />
                </div>
                <div class="flex flex-col leading-tight">
                    <span class="text-size-15px whitespace-nowrap">{{ $t(option.label) }}</span>
                    <span v-if="option.description" class="text-size-11px opacity-60">
                        {{ option.description }}
                    </span>
                </div>
            </div>
            <!-- Color picker for highlight -->
            <div v-if="showColorPicker" class="flex flex-wrap gap-5px px-7px py-6px border-t border-gray-500 border-opacity-30 mt-4px">
                <button
                    v-for="c in colors"
                    :key="c.color"
                    :style="`background: ${c.color}`"
                    class="h-24px w-24px rounded-full cursor-pointer border-2 border-transparent hover:border-white transition-all hover:scale-110"
                    :title="c.name"
                    @click="highlightVerse(c.color)"
                ></button>
            </div>
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
            <div class="ai-insight-text">{{ aiResult }}</div>
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

.ai-insight-text {
    white-space: pre-wrap;
    line-height: 1.55;
    font-size: 14px;
}

.ai-insight-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid var(--theme-border, rgba(127, 127, 127, 0.2));
}

/* AI group in the verse context menu — accented so it stands out / is findable. */
.ai-group-label {
    color: var(--primary-color);
    opacity: 0.9;
}
.ai-group-label__icon {
    color: var(--primary-color);
}
.ai-menu-item__icon {
    color: var(--primary-color);
}
.ai-menu-item:hover {
    background: color-mix(in srgb, var(--primary-color) 16%, transparent);
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
