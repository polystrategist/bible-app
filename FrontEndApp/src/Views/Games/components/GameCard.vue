<script setup lang="ts">
defineProps<{
    title: string;
    description: string;
    color: string;
    emoji: string;
    progress: { completed: number; total: number };
    disabled?: boolean;
}>();

const emit = defineEmits<{ play: [] }>();
</script>

<template>
    <div
        class="rounded-xl border border-[var(--theme-border)] bg-[var(--theme-bg-elevated)] p-4 transition-shadow"
        :class="disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:shadow-md'"
        @click="!disabled && emit('play')"
    >
        <div class="flex items-start gap-4">
            <div
                class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shrink-0"
                :style="{ background: color + '22' }"
            >
                {{ emoji }}
            </div>
            <div class="flex-1 min-w-0">
                <p class="font-semibold text-sm text-[var(--theme-text)]">{{ title }}</p>
                <p class="text-xs text-[var(--theme-text-soft)] mt-0.5 line-clamp-2">{{ description }}</p>
                <div class="mt-3">
                    <div class="h-1.5 rounded-full bg-[var(--theme-bg-soft)] overflow-hidden">
                        <div
                            class="h-full rounded-full transition-all"
                            :style="{ width: (progress.total ? (progress.completed / progress.total) * 100 : 0) + '%', background: color }"
                        />
                    </div>
                    <p class="text-xs text-[var(--theme-text-soft)] mt-1.5 font-medium">
                        {{ progress.completed }} / {{ progress.total }} complete
                    </p>
                </div>
            </div>
            <span class="text-[var(--theme-text-soft)] text-lg">&rsaquo;</span>
        </div>
    </div>
</template>
