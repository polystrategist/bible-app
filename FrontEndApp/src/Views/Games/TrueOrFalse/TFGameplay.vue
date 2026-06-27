<script setup lang="ts">
import { computed } from 'vue';
import { NButton } from 'naive-ui';
import { useGamesStore } from '../../../store/useGamesStore';
import { formatProofReference } from '../../../util/books';
import { stripVerseHtml } from '../../../util/helper';

const emit = defineEmits<{ back: []; exit: [] }>();
const store = useGamesStore();

const ACCENT = '#10b981';

const statement = computed(() => store.currentQuestion as any);

function tfBtnProps(isTrue: boolean) {
    const selected = store.selectedAnswerIndex === (isTrue ? 1 : 0);
    const correct = statement.value?.answer === (isTrue ? 1 : 0);
    if (store.gameState !== 'answered') {
        return { type: (isTrue ? 'success' : 'error') as 'success' | 'error' };
    }
    if (correct) return { type: 'success' as const };
    if (selected) return { type: 'error' as const };
    return { type: (isTrue ? 'success' : 'error') as 'success' | 'error', class: 'opacity-40' };
}
</script>

<template>
    <div class="space-y-4">
        <div class="flex items-center justify-between">
            <NButton quaternary size="small" :focusable="false" @click="emit('back')">
                <span class="text-base leading-none mr-1">&larr;</span> Groups
            </NButton>
            <div class="flex items-center gap-3 text-sm text-[var(--theme-text-soft)]">
                <span class="text-red-500">&#10084; {{ store.lives }}</span>
                <span>Score: {{ store.score }}/{{ store.totalItems }}</span>
            </div>
        </div>

        <div
            v-if="store.gameState === 'gameOver' || store.gameState === 'completed'"
            class="max-w-sm mx-auto mt-2 p-8 rounded-3xl border border-[var(--theme-border)] bg-[var(--theme-bg-elevated)] text-center space-y-5 shadow-xl shadow-black/5 dark:shadow-black/40"
        >
            <div
                class="mx-auto w-20 h-20 rounded-full flex items-center justify-center text-4xl"
                :class="store.gameState === 'completed' ? 'bg-emerald-100 dark:bg-emerald-500/15' : 'bg-red-100 dark:bg-red-500/15'"
            >{{ store.gameState === 'completed' ? '🎉' : '💔' }}</div>

            <div class="space-y-1">
                <p class="text-2xl font-bold text-[var(--theme-text)]">
                    {{ store.gameState === 'completed' ? (store.newlyPassed ? 'Passed!' : 'Completed!') : 'Out of lives' }}
                </p>
                <p class="text-sm text-[var(--theme-text-soft)]">
                    {{ store.gameState === 'gameOver' ? 'Better luck next time' : store.newlyPassed ? 'Great job — you cleared this group!' : 'Keep practicing to pass' }}
                </p>
            </div>

            <div class="grid grid-cols-2 gap-3">
                <div class="p-3 rounded-2xl bg-[var(--theme-bg-soft)] border border-[var(--theme-border)]">
                    <p class="text-2xl font-extrabold text-emerald-600 dark:text-emerald-400">{{ store.score }}<span class="text-base font-bold text-[var(--theme-text-soft)]">/{{ store.totalItems }}</span></p>
                    <p class="text-xs text-[var(--theme-text-soft)] mt-0.5">Score · {{ store.scorePercentage }}%</p>
                </div>
                <div class="p-3 rounded-2xl bg-[var(--theme-bg-soft)] border border-[var(--theme-border)]">
                    <p class="text-2xl font-extrabold text-emerald-600 dark:text-emerald-400">{{ store.bestStreak }}</p>
                    <p class="text-xs text-[var(--theme-text-soft)] mt-0.5">Best streak</p>
                </div>
            </div>

            <div class="flex gap-3 pt-1">
                <NButton class="flex-1" size="large" :color="ACCENT" :focusable="false" @click="emit('back')">Back to Groups</NButton>
                <NButton class="flex-1" size="large" :focusable="false" @click="emit('exit')">Exit</NButton>
            </div>
        </div>

        <template v-else-if="statement">
            <div class="p-5 rounded-2xl border border-[var(--theme-border)] bg-[var(--theme-bg-elevated)]">
                <p class="text-xs text-[var(--theme-text-soft)] mb-2 font-medium">Statement {{ store.currentIndex + 1 }} of {{ store.totalItems }}</p>
                <p class="text-base font-medium text-[var(--theme-text)] leading-relaxed">{{ statement.statement }}</p>
            </div>

            <div class="grid grid-cols-2 gap-3">
                <NButton
                    block
                    size="large"
                    class="tf-choice-btn"
                    :focusable="false"
                    v-bind="tfBtnProps(true)"
                    @click="store.submitTFAnswer(true)"
                >&check; True</NButton>
                <NButton
                    block
                    size="large"
                    class="tf-choice-btn"
                    :focusable="false"
                    v-bind="tfBtnProps(false)"
                    @click="store.submitTFAnswer(false)"
                >&times; False</NButton>
            </div>

            <template v-if="store.gameState === 'answered'">
                <div v-if="statement.proof || statement.explanation" class="text-sm text-[var(--theme-text)] bg-[var(--theme-bg-soft)] p-3 rounded-xl border border-[var(--theme-border)] space-y-1">
                    <p v-if="statement.proof" class="font-medium text-[var(--theme-text-soft)]">{{ formatProofReference(statement.proof) }}</p>
                    <p v-if="statement.explanation">{{ stripVerseHtml(statement.explanation) }}</p>
                </div>
                <NButton block size="large" :color="ACCENT" :focusable="false" @click="store.nextTFQuestion()">
                    {{ store.currentIndex + 1 >= store.totalItems ? 'Finish' : 'Next' }}
                </NButton>
            </template>
        </template>
    </div>
</template>

<style scoped>
/* Keep the True/False buttons tall and bold like the original. */
.tf-choice-btn {
    height: 3.25rem;
    font-size: 1.05rem;
    font-weight: 700;
}
</style>
