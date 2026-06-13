<script setup lang="ts">
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ back: []; select: [groupId: number] }>();
const store = useGamesStore();
</script>

<template>
    <div class="space-y-3">
        <div class="flex items-center gap-2">
            <button
                class="px-2 py-1 rounded-lg text-sm text-neutral-500 hover:bg-neutral-100 dark:hover:bg-dark-600"
                @click="emit('back')"
            >&larr; Back</button>
            <h2 class="text-lg font-bold text-neutral-900 dark:text-neutral-100">Question &amp; Answer</h2>
        </div>

        <div
            v-for="group in store.qaGroups"
            :key="group.id"
            class="flex items-center justify-between p-4 rounded-xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-dark-600"
        >
            <div class="flex-1 min-w-0">
                <p class="font-medium text-sm text-neutral-900 dark:text-neutral-100">{{ group.name }}</p>
                <p v-if="store.qaGroupProgress[group.id]" class="text-xs text-neutral-400 mt-0.5">
                    Best: {{ store.qaGroupProgress[group.id].high_score_percentage }}%
                    · Played {{ store.qaGroupProgress[group.id].times_played }}&times;
                </p>
                <p v-if="store.qaGroupProgress[group.id] && store.qaGroupProgress[group.id].is_completed" class="text-xs text-green-600 dark:text-green-400 mt-0.5 font-medium">&check; Passed</p>
            </div>
            <button
                v-if="store.qaIsGroupUnlocked(group.id)"
                class="px-4 py-1.5 rounded-lg text-sm font-semibold text-white shrink-0 ml-3"
                :class="store.canPlay ? 'bg-blue-500 hover:bg-blue-600' : 'bg-neutral-300 dark:bg-neutral-600 cursor-not-allowed'"
                :disabled="!store.canPlay"
                @click="store.canPlay && emit('select', group.id)"
            >Play</button>
            <span v-else class="text-neutral-300 dark:text-neutral-600 text-lg ml-3" title="Complete earlier groups to unlock">🔒</span>
        </div>

        <p v-if="!store.canPlay" class="text-xs text-center text-red-500 pt-1">
            You're out of lives — wait for a heart to recover before playing.
        </p>
    </div>
</template>
