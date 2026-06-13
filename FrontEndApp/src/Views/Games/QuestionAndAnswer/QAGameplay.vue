<script setup lang="ts">
import { computed } from 'vue';
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ back: []; exit: [] }>();
const store = useGamesStore();

const question = computed(() => store.currentQuestion as any);

function answerClass(i: number) {
    if (store.gameState !== 'answered') {
        return 'bg-white dark:bg-dark-600 border-neutral-200 dark:border-neutral-700 hover:border-blue-400';
    }
    if (i === store.shuffledCorrectIndex) {
        return 'bg-green-50 dark:bg-green-900 border-green-500 text-green-700 dark:text-green-300';
    }
    if (i === store.selectedAnswerIndex && !store.lastAnswerCorrect) {
        return 'bg-red-50 dark:bg-red-900 border-red-500 text-red-700 dark:text-red-300';
    }
    return 'bg-white dark:bg-dark-600 border-neutral-200 dark:border-neutral-700 opacity-50';
}
</script>

<template>
    <div class="space-y-4">
        <div class="flex items-center justify-between">
            <button
                class="px-2 py-1 rounded-lg text-sm text-neutral-500 hover:bg-neutral-100 dark:hover:bg-dark-600"
                @click="emit('back')"
            >&larr; Groups</button>
            <div class="flex items-center gap-3 text-sm text-neutral-500">
                <span class="text-red-500">&#10084; {{ store.lives }}</span>
                <span>Score: {{ store.score }}/{{ store.totalItems }}</span>
            </div>
        </div>

        <!-- Game over / completed -->
        <div
            v-if="store.gameState === 'gameOver' || store.gameState === 'completed'"
            class="p-6 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-dark-600 text-center space-y-4"
        >
            <p class="text-3xl">{{ store.gameState === 'completed' ? '🎉' : '💔' }}</p>
            <p class="text-xl font-bold text-neutral-900 dark:text-neutral-100">
                {{ store.gameState === 'completed' ? (store.newlyPassed ? 'Passed!' : 'Completed!') : 'Out of lives' }}
            </p>
            <p class="text-neutral-500">Score: {{ store.score }} / {{ store.totalItems }} ({{ store.scorePercentage }}%)</p>
            <p class="text-neutral-500">Best streak: {{ store.bestStreak }}</p>
            <div class="flex gap-3 justify-center pt-1">
                <button class="px-5 py-2 rounded-xl bg-blue-500 text-white font-semibold hover:bg-blue-600" @click="emit('back')">Back to Groups</button>
                <button class="px-5 py-2 rounded-xl border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-dark-700" @click="emit('exit')">Exit</button>
            </div>
        </div>

        <!-- Playing / answered -->
        <template v-else-if="question">
            <div class="p-5 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-dark-600">
                <p class="text-xs text-neutral-400 mb-2 font-medium">Question {{ store.currentIndex + 1 }} of {{ store.totalItems }}</p>
                <p class="text-base font-medium text-neutral-900 dark:text-neutral-100 leading-relaxed">{{ question.question }}</p>
            </div>

            <div class="space-y-2">
                <button
                    v-for="(opt, i) in store.shuffledOptions"
                    :key="i"
                    :disabled="store.gameState === 'answered'"
                    class="w-full text-left px-4 py-3 rounded-xl border text-sm font-medium transition-colors text-neutral-800 dark:text-neutral-100"
                    :class="answerClass(i)"
                    @click="store.submitQAAnswer(i)"
                >{{ opt }}</button>
            </div>

            <template v-if="store.gameState === 'answered'">
                <div v-if="question.proof || question.explanation" class="text-sm text-neutral-600 dark:text-neutral-300 bg-neutral-50 dark:bg-dark-700 p-3 rounded-xl border border-neutral-200 dark:border-neutral-700 space-y-1">
                    <p v-if="question.proof" class="font-medium text-neutral-500 dark:text-neutral-400">{{ question.proof }}</p>
                    <p v-if="question.explanation">{{ question.explanation }}</p>
                </div>
                <button
                    class="w-full py-3 rounded-xl bg-blue-500 text-white font-semibold hover:bg-blue-600"
                    @click="store.nextQAQuestion()"
                >{{ store.currentIndex + 1 >= store.totalItems ? 'Finish' : 'Next' }}</button>
            </template>
        </template>
    </div>
</template>
