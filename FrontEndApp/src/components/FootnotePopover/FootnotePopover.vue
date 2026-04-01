<script lang="ts" setup>
interface Props {
    show: boolean;
    x: number;
    y: number;
    marker: string;
    text: string;
    fontSize: number;
}

defineProps<Props>();
defineEmits<{ close: [] }>();
</script>

<template>
    <Teleport to="body">
        <Transition name="footnote-fade">
            <div
                v-if="show"
                class="footnote-tooltip"
                :style="{ top: `${y}px`, left: `${x}px`, fontSize: `${fontSize}px` }"
            >
                <div class="footnote-tooltip-body" v-html="text"></div>
                <div class="footnote-tooltip-arrow"></div>
            </div>
        </Transition>
    </Teleport>
</template>

<style scoped>
.footnote-tooltip {
    position: fixed;
    transform: translate(-50%, -100%);
    max-width: 280px;
    min-width: 120px;
    background: var(--n-color, #2a2a2a);
    border: 1px solid var(--n-border-color, rgba(255,255,255,0.1));
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    padding: 7px 10px;
    line-height: 1.5;
    color: var(--n-text-color, #e0e0e0);
    pointer-events: none;
    z-index: 9999;
}

.footnote-tooltip-body :deep(em),
.footnote-tooltip-body :deep(i) {
    font-style: italic;
}

.footnote-tooltip-body :deep(span.tl),
.footnote-tooltip-body :deep(span.it) {
    font-style: italic;
}

.footnote-tooltip-arrow {
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid var(--n-border-color, rgba(255,255,255,0.1));
}

.footnote-tooltip-arrow::after {
    content: '';
    position: absolute;
    top: -6px;
    left: -4px;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 4px solid var(--n-color, #2a2a2a);
}

.footnote-fade-enter-active,
.footnote-fade-leave-active {
    transition: opacity 0.12s ease, transform 0.12s ease;
}

.footnote-fade-enter-from,
.footnote-fade-leave-to {
    opacity: 0;
    transform: translate(-50%, calc(-100% + 4px));
}
</style>
