<script setup lang="ts">
import type { Component } from 'vue';
import { NIcon } from 'naive-ui';
import { ChevronRight24Regular } from '@vicons/fluent';

defineProps<{
    title: string;
    expanded: boolean;
    icon?: Component;
    /** Animate height changes (toggle). Disabled while a divider is being dragged. */
    animate?: boolean;
}>();

const emit = defineEmits<{ (e: 'toggle'): void }>();
</script>

<template>
    <div
        class="flex flex-col min-h-0 overflow-hidden"
        :class="{ 'accordion-animate': animate !== false }"
    >
        <button
            type="button"
            class="accordion-header h-8 min-h-8 w-full select-none flex items-center gap-1.5 px-2 cursor-pointer transition-colors duration-150 focus:outline-none"
            :aria-expanded="expanded"
            @click="emit('toggle')"
        >
            <NIcon
                size="14"
                class="flex-shrink-0 opacity-60 transition-transform duration-200 ease-out"
                :class="expanded ? 'rotate-90' : ''"
            >
                <ChevronRight24Regular />
            </NIcon>
            <NIcon v-if="icon" :component="icon" size="16" class="flex-shrink-0 opacity-60" />
            <span class="text-[11px] font-700 uppercase tracking-widest opacity-60">
                {{ title }}
            </span>
            <span class="ml-auto flex items-center" @click.stop>
                <slot name="actions" />
            </span>
        </button>
        <div class="flex-1 min-h-0 overflow-hidden">
            <slot />
        </div>
    </div>
</template>

<style scoped>
.accordion-animate {
    transition: height 220ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Use the panel's own themed surface so the theme colour reaches the header
   AND it stays seamless with the content (same colour = no fill-edge / border).
   The explicit value also overrides the native <button> grey background, which
   is what made the bars look light/un-themed. */
.accordion-header {
    background-color: var(--theme-bg-elevated, #ffffff);
    color: var(--theme-text, #333333);
}

/* Hover/focus: a gentle step to the soft surface for affordance. */
.accordion-header:hover,
.accordion-header:focus-visible {
    background-color: var(--theme-bg-soft, #ebebeb);
}
</style>
