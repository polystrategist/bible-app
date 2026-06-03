<script setup lang="ts">
import { NIcon, NPopover, NModal, NSpin } from 'naive-ui';
import { Sparkle24Regular } from '@vicons/fluent';
import { onClickOutside } from '@vueuse/core';
import { ref, type PropType } from 'vue';
import { ContextMenuOptions } from './ContextMenuOptions';
import { useBookmarkStore } from '../../../../store/bookmark';
import { useBibleStore } from '../../../../store/BibleStore';
import { useAiStore, AiError } from '../../../../store/aiStore';
import { useAuthStore } from '../../../../store/authStore';
import { debouncedRunSync } from '../../../../util/Sync/sync';
import { colors } from '../../../../util/highlighter';

const bibleStore = useBibleStore();
const aiStore = useAiStore();
const authStore = useAuthStore();
const contextMenuRef = ref(null);
const emits = defineEmits(['close', 'create-clip-note']);
const bookmarkStore = useBookmarkStore();
const showColorPicker = ref(false);

// ─── AI Insight ──────────────────────────────────────────────────────────────
const showAiModal = ref(false);
const aiReference = ref('');
const aiLoading = ref(false);
const aiResult = ref('');
const aiError = ref('');
const aiUpgrade = ref(false);

function stripVerseMarkup(text: string): string {
    return (text ?? '')
        .replace(/<[^>]*>/g, ' ') // tags (<S>, <J>, <f>…)
        .replace(/\s+/g, ' ')
        .trim();
}

async function runAiInsight() {
    const d: any = props.data;
    aiReference.value = `${bibleStore.selectedBook.title} ${d.chapter}:${d.verse}`;
    aiResult.value = '';
    aiError.value = '';
    aiUpgrade.value = false;
    showAiModal.value = true;

    // AI is a Pro feature — surface the upgrade prompt without a failed request.
    if (!authStore.isAiEnabled) {
        aiUpgrade.value = true;
        return;
    }

    aiLoading.value = true;
    try {
        const res = await aiStore.verseInsight(
            aiReference.value,
            stripVerseMarkup(d.text),
        );
        aiResult.value = res.text;
    } catch (e) {
        if (e instanceof AiError && e.isPaywall) {
            aiUpgrade.value = true;
        } else {
            aiError.value =
                e instanceof AiError ? e.message : 'Could not load insight. Please try again.';
        }
    } finally {
        aiLoading.value = false;
    }
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
            class="w-200px max-h-250px overflow-y-auto overflowing-div flex flex-col select-none p-5px"
        >
            <div
                v-for="option in ContextMenuOptions"
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

    <!-- AI Insight modal -->
    <NModal
        v-model:show="showAiModal"
        preset="card"
        :title="`AI Insight · ${aiReference}`"
        :bordered="false"
        style="max-width: 560px; width: 92vw;"
    >
        <div v-if="aiLoading" class="ai-insight-loading">
            <NSpin size="small" /> <span>Generating insight…</span>
        </div>

        <div v-else-if="aiUpgrade" class="ai-insight-upsell">
            <NIcon size="22" :component="Sparkle24Regular" />
            <p class="ai-insight-upsell__title">AI Insight is part of Pro</p>
            <p class="ai-insight-upsell__text">
                Upgrade to Believers Sword Pro to get verse explanations, original-language
                words, and pronunciation.
            </p>
        </div>

        <p v-else-if="aiError" class="ai-insight-error">{{ aiError }}</p>

        <div v-else class="ai-insight-text">{{ aiResult }}</div>
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
    gap: 6px;
    padding: 8px 4px;
    color: #d8a23a;
}

.ai-insight-upsell__title {
    margin: 4px 0 0;
    font-weight: 700;
    font-size: 15px;
}

.ai-insight-upsell__text {
    margin: 0;
    font-size: 13px;
    line-height: 1.45;
    opacity: 0.85;
}
</style>
