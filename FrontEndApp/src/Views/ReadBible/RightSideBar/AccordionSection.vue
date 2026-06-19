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
        <div
            role="button"
            tabindex="0"
            class="accordion-header h-8 min-h-8 w-full select-none flex items-center gap-1.5 px-2 cursor-pointer transition-colors duration-150 focus:outline-none"
            :aria-expanded="expanded"
            @click="emit('toggle')"
            @keydown.enter="emit('toggle')"
            @keydown.space.prevent="emit('toggle')"
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
        </div>
        <div class="flex-1 min-h-0 overflow-hidden">
            <slot />
        </div>
    </div>
</template>

<style scoped>
.accordion-animate {
    transition: height 220ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* VS Code Explorer-style section header: a faint translucent bar over the
   panel surface. Neutral + low-alpha so it adapts to any theme (lightens on
   dark, darkens on light), reads as a subtle bar, and has no hard border line.
   The explicit value also overrides the native <button> grey background. */
.accordion-header {
    background-color: rgba(128, 128, 128, 0.1);
    color: var(--theme-text, #333333);
}

.accordion-header:hover,
.accordion-header:focus-visible {
    background-color: rgba(128, 128, 128, 0.16);
}
</style>
