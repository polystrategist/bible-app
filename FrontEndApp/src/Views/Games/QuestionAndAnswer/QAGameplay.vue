<script setup lang="ts">
import { computed } from 'vue';
import { NButton } from 'naive-ui';
import { useGamesStore } from '../../../store/useGamesStore';
import { formatProofReference } from '../../../util/books';

const emit = defineEmits<{ back: []; exit: [] }>();
const store = useGamesStore();

const ACCENT = '#3b82f6';

const question = computed(() => store.currentQuestion as any);

function answerProps(i: number) {
    if (store.gameState !== 'answered') {
        return { secondary: true };
    }
    if (i === store.shuffledCorrectIndex) {
        return { type: 'success' as const };
    }
    if (i === store.selectedAnswerIndex && !store.lastAnswerCorrect) {
        return { type: 'error' as const };
    }
    return { secondary: true, disabled: true };
}
</script>

<template>
    <div class="space-y-4">
        <div class="flex items-center justify-between">
            <NButton quaternary size="small" :focusable="false" @click="emit('back')">
                <span class="text-base leading-none mr-1">&larr;</span> Groups
            </NButton>
            <div class="flex items-center gap-3 text-sm text-neutral-500">
                <span class="text-red-500">&#10084; {{ store.lives }}</span>
                <span>Score: {{ store.score }}/{{ store.totalItems }}</span>
            </div>
        </div>

        <!-- Game over / completed -->
        <div
            v-if="store.gameState === 'gameOver' || store.gameState === 'completed'"
            class="max-w-sm mx-auto mt-2 p-8 rounded-3xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-dark-500 text-center space-y-5 shadow-xl shadow-black/5 dark:shadow-black/40"
        >
            <div
                class="mx-auto w-20 h-20 rounded-full flex items-center justify-center text-4xl"
                :class="store.gameState === 'completed' ? 'bg-blue-100 dark:bg-blue-500/15' : 'bg-red-100 dark:bg-red-500/15'"
            >{{ store.gameState === 'completed' ? '🎉' : '💔' }}</div>

            <div class="space-y-1">
                <p class="text-2xl font-bold text-neutral-900 dark:text-neutral-100">
                    {{ store.gameState === 'completed' ? (store.newlyPassed ? 'Passed!' : 'Completed!') : 'Out of lives' }}
                </p>
                <p class="text-sm text-neutral-500">
                    {{ store.gameState === 'gameOver' ? 'Better luck next time' : store.newlyPassed ? 'Great job — you cleared this group!' : 'Keep practicing to pass' }}
                </p>
            </div>

            <div class="grid grid-cols-2 gap-3">
                <div class="p-3 rounded-2xl bg-neutral-50 dark:bg-dark-900 border border-neutral-200/70 dark:border-white/5">
                    <p class="text-2xl font-extrabold text-blue-600 dark:text-blue-400">{{ store.score }}<span class="text-base font-bold text-neutral-400">/{{ store.totalItems }}</span></p>
                    <p class="text-xs text-neutral-400 mt-0.5">Score · {{ store.scorePercentage }}%</p>
                </div>
                <div class="p-3 rounded-2xl bg-neutral-50 dark:bg-dark-900 border border-neutral-200/70 dark:border-white/5">
                    <p class="text-2xl font-extrabold text-blue-600 dark:text-blue-400">{{ store.bestStreak }}</p>
                    <p class="text-xs text-neutral-400 mt-0.5">Best streak</p>
                </div>
            </div>

            <div class="flex gap-3 pt-1">
                <NButton class="flex-1" size="large" :color="ACCENT" :focusable="false" @click="emit('back')">Back to Groups</NButton>
                <NButton class="flex-1" size="large" :focusable="false" @click="emit('exit')">Exit</NButton>
            </div>
        </div>

        <!-- Playing / answered -->
        <template v-else-if="question">
            <div class="p-5 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-dark-600">
                <p class="text-xs text-neutral-400 mb-2 font-medium">Question {{ store.currentIndex + 1 }} of {{ store.totalItems }}</p>
                <p class="text-base font-medium text-neutral-900 dark:text-neutral-100 leading-relaxed">{{ question.question }}</p>
            </div>

            <div class="space-y-2">
                <NButton
                    v-for="(opt, i) in store.shuffledOptions"
                    :key="i"
                    block
                    size="large"
                    class="game-answer-btn"
                    :focusable="false"
                    v-bind="answerProps(i)"
                    @click="store.submitQAAnswer(i)"
                >{{ opt }}</NButton>
            </div>

            <template v-if="store.gameState === 'answered'">
                <div v-if="question.proof || question.explanation" class="text-sm text-neutral-600 dark:text-neutral-300 bg-neutral-50 dark:bg-dark-700 p-3 rounded-xl border border-neutral-200 dark:border-neutral-700 space-y-1">
                    <p v-if="question.proof" class="font-medium text-neutral-500 dark:text-neutral-400">{{ formatProofReference(question.proof) }}</p>
                    <p v-if="question.explanation">{{ question.explanation }}</p>
                </div>
                <NButton block size="large" :color="ACCENT" :focusable="false" @click="store.nextQAQuestion()">
                    {{ store.currentIndex + 1 >= store.totalItems ? 'Finish' : 'Next' }}
                </NButton>
            </template>
        </template>
    </div>
</template>

<style scoped>
/* Let answer options grow and left-align their (possibly long) text. */
.game-answer-btn {
    justify-content: flex-start;
    height: auto;
    min-height: 2.75rem;
    padding-top: 0.6rem;
    padding-bottom: 0.6rem;
    text-align: left;
}
.game-answer-btn :deep(.n-button__content) {
    white-space: normal;
}
</style>
