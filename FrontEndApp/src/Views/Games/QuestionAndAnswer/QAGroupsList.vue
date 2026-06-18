<script setup lang="ts">
import { NButton } from 'naive-ui';
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ back: []; select: [groupId: number] }>();
const store = useGamesStore();

const ACCENT = '#3b82f6';
</script>

<template>
    <div class="flex flex-col h-full">
        <div class="flex items-center gap-2 shrink-0 pb-3">
            <NButton quaternary size="small" :focusable="false" @click="emit('back')">
                <span class="text-base leading-none mr-1">&larr;</span> Back
            </NButton>
            <h2 class="text-lg font-bold text-[var(--theme-text)]">Question &amp; Answer</h2>
        </div>

        <div class="flex-1 min-h-0 overflow-y-auto space-y-3 pr-1">
            <div
                v-for="group in store.qaGroups"
                :key="group.id"
                class="flex items-center justify-between p-4 rounded-xl border border-[var(--theme-border)] bg-[var(--theme-bg-elevated)]"
            >
                <div class="flex-1 min-w-0">
                    <p class="font-medium text-sm text-[var(--theme-text)]">{{ group.name }}</p>
                    <p v-if="store.qaGroupProgress[group.id]" class="text-xs text-[var(--theme-text-soft)] mt-0.5">
                        Best: {{ store.qaGroupProgress[group.id].high_score_percentage }}%
                        · Played {{ store.qaGroupProgress[group.id].times_played }}&times;
                    </p>
                    <p v-if="store.qaGroupProgress[group.id] && store.qaGroupProgress[group.id].is_completed" class="text-xs text-green-600 dark:text-green-400 mt-0.5 font-medium">&check; Passed</p>
                </div>
                <NButton
                    v-if="store.qaIsGroupUnlocked(group.id)"
                    class="shrink-0 ml-3"
                    size="small"
                    :color="ACCENT"
                    :disabled="!store.canPlay"
                    :focusable="false"
                    @click="emit('select', group.id)"
                >Play</NButton>
                <span v-else class="text-[var(--theme-text-soft)] text-lg ml-3" title="Complete earlier groups to unlock">🔒</span>
            </div>

            <p v-if="!store.canPlay" class="text-xs text-center text-red-500 pt-1">
                You're out of lives — wait for a heart to recover before playing.
            </p>
        </div>
    </div>
</template>
