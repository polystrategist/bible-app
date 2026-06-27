<script lang="ts" setup>
interface StrongsEntry {
    strong_number: string;
    language?: string | null;
    lemma?: string | null;
    translit?: string | null;
    pronunciation?: string | null;
    derivation?: string | null;
    strongs_def?: string | null;
    kjv_def?: string | null;
}

interface Props {
    show: boolean;
    x: number;
    y: number;
    below?: boolean;
    loading?: boolean;
    entry: StrongsEntry | null;
    fontSize: number;
}

defineProps<Props>();
</script>

<template>
    <Teleport to="body">
        <Transition name="strongs-fade">
            <div
                v-if="show"
                class="strongs-tooltip"
                :class="{ 'strongs-below': below }"
                :style="{ top: `${y}px`, left: `${x}px`, fontSize: `${fontSize}px` }"
            >
                <div class="strongs-tooltip-body">
                    <div v-if="loading" class="strongs-loading">…</div>

                    <template v-else-if="entry">
                        <div class="strongs-header">
                            <span class="strongs-number">{{ entry.strong_number }}</span>
                            <span v-if="entry.lemma" class="strongs-lemma">{{ entry.lemma }}</span>
                        </div>

                        <div v-if="entry.translit || entry.pronunciation" class="strongs-translit">
                            <span v-if="entry.translit">{{ entry.translit }}</span>
                            <span v-if="entry.pronunciation" class="strongs-pron">
                                ({{ entry.pronunciation }})
                            </span>
                        </div>

                        <div v-if="entry.derivation" class="strongs-section">
                            <span class="strongs-label">{{ $t('strongs-derivation') }}:</span>
                            {{ entry.derivation }}
                        </div>

                        <div v-if="entry.strongs_def" class="strongs-section">
                            <span class="strongs-label">{{ $t('strongs-definition') }}:</span>
                            {{ entry.strongs_def }}
                        </div>

                        <div v-if="entry.kjv_def" class="strongs-section strongs-kjv">
                            <span class="strongs-label">{{ $t('strongs-kjv-usage') }}:</span>
                            {{ entry.kjv_def }}
                        </div>
                    </template>

                    <div v-else class="strongs-empty">{{ $t('strongs-not-found') }}</div>
                </div>
                <div class="strongs-tooltip-arrow"></div>
            </div>
        </Transition>
    </Teleport>
</template>

<style scoped>
.strongs-tooltip {
    position: fixed;
    transform: translate(-50%, -100%);
    max-width: 320px;
    min-width: 180px;
    /* App theme vars (defined on :root) resolve here even though the popover is
       teleported to <body> — naive-ui's --n-* vars would not. */
    background: var(--theme-bg-elevated, #1c1c1e);
    border: 1px solid var(--theme-border, rgba(255, 255, 255, 0.12));
    border-radius: 8px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
    padding: 10px 12px;
    line-height: 1.5;
    color: var(--theme-text, #e0e0e0);
    z-index: 9999;
}

/* Flipped placement: popover sits below the badge with the arrow on top. */
.strongs-tooltip.strongs-below {
    transform: translate(-50%, 0);
}

.strongs-tooltip-body {
    max-height: 320px;
    overflow-y: auto;
}

.strongs-header {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 4px;
}

.strongs-number {
    font-weight: 700;
    color: var(--primary-color);
    font-size: 0.85em;
}

.strongs-lemma {
    font-size: 1.15em;
    font-weight: 600;
}

.strongs-translit {
    font-style: italic;
    opacity: 0.85;
    margin-bottom: 6px;
}

.strongs-pron {
    opacity: 0.7;
}

.strongs-section {
    margin-top: 4px;
    font-size: 0.92em;
}

.strongs-label {
    font-weight: 600;
    opacity: 0.7;
    margin-right: 3px;
}

.strongs-kjv {
    opacity: 0.85;
}

.strongs-empty,
.strongs-loading {
    opacity: 0.6;
    font-style: italic;
}

.strongs-tooltip-arrow {
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid var(--theme-border, rgba(255, 255, 255, 0.12));
}

.strongs-tooltip-arrow::after {
    content: '';
    position: absolute;
    top: -6px;
    left: -4px;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 4px solid var(--theme-bg-elevated, #1c1c1e);
}

/* Arrow flips to the top edge, pointing up, in below placement. */
.strongs-below .strongs-tooltip-arrow {
    bottom: auto;
    top: -5px;
    transform: translateX(-50%) rotate(180deg);
}

.strongs-fade-enter-active,
.strongs-fade-leave-active {
    transition: opacity 0.12s ease, transform 0.12s ease;
}

.strongs-fade-enter-from,
.strongs-fade-leave-to {
    opacity: 0;
    transform: translate(-50%, calc(-100% + 4px));
}

.strongs-below.strongs-fade-enter-from,
.strongs-below.strongs-fade-leave-to {
    opacity: 0;
    transform: translate(-50%, -4px);
}
</style>
