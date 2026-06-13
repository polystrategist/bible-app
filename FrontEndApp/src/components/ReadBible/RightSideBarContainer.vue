<script setup lang="ts">
defineProps({
    title: {
        type: String,
    },
});
</script>
<template>
    <div class="w-full h-full flex flex-col">
        <div
            class="h-8 min-h-8 select-none flex items-center justify-between px-2 border-b border-gray-200 dark:border-dark-600"
        >
            <span class="text-[11px] font-700 uppercase tracking-widest opacity-60">
                {{ $props.title }}
            </span>
            <slot name="rightSide">
                <div></div>
            </slot>
        </div>
        <div class="flex-1 min-h-0 overflow-hidden">
            <slot />
        </div>
    </div>
</template>
