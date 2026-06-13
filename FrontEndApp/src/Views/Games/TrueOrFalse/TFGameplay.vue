<script setup lang="ts">
import { computed } from 'vue';
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ back: []; exit: [] }>();
const store = useGamesStore();

const statement = computed(() => store.currentQuestion as any);

function btnClass(isTrue: boolean) {
    const selected = store.selectedAnswerIndex === (isTrue ? 1 : 0);
    const correct = statement.value?.answer === (isTrue ? 1 : 0);
    if (store.gameState !== 'answered') {
        return isTrue
            ? 'bg-emerald-500 hover:bg-emerald-600 text-white'
            : 'bg-red-500 hover:bg-red-600 text-white';
    }
    if (correct) return 'bg-green-100 dark:bg-green-900 border-2 border-green-500 text-green-700 dark:text-green-300';
    if (selected) return 'bg-red-100 dark:bg-red-900 border-2 border-red-500 text-red-700 dark:text-red-300';
    return 'opacity-40 ' + (isTrue ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white');
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
                <button class="px-5 py-2 rounded-xl bg-emerald-500 text-white font-semibold hover:bg-emerald-600" @click="emit('back')">Back to Groups</button>
                <button class="px-5 py-2 rounded-xl border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-dark-700" @click="emit('exit')">Exit</button>
            </div>
        </div>

        <template v-else-if="statement">
            <div class="p-5 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-dark-600">
                <p class="text-xs text-neutral-400 mb-2 font-medium">Statement {{ store.currentIndex + 1 }} of {{ store.totalItems }}</p>
                <p class="text-base font-medium text-neutral-900 dark:text-neutral-100 leading-relaxed">{{ statement.statement }}</p>
            </div>

            <div class="grid grid-cols-2 gap-3">
                <button
                    :disabled="store.gameState === 'answered'"
                    class="py-4 rounded-xl text-lg font-bold transition-all"
                    :class="btnClass(true)"
                    @click="store.submitTFAnswer(true)"
                >&check; True</button>
                <button
                    :disabled="store.gameState === 'answered'"
                    class="py-4 rounded-xl text-lg font-bold transition-all"
                    :class="btnClass(false)"
                    @click="store.submitTFAnswer(false)"
                >&times; False</button>
            </div>

            <template v-if="store.gameState === 'answered'">
                <div v-if="statement.proof || statement.explanation" class="text-sm text-neutral-600 dark:text-neutral-300 bg-neutral-50 dark:bg-dark-700 p-3 rounded-xl border border-neutral-200 dark:border-neutral-700 space-y-1">
                    <p v-if="statement.proof" class="font-medium text-neutral-500 dark:text-neutral-400">{{ statement.proof }}</p>
                    <p v-if="statement.explanation">{{ statement.explanation }}</p>
                </div>
                <button
                    class="w-full py-3 rounded-xl bg-emerald-500 text-white font-semibold hover:bg-emerald-600"
                    @click="store.nextTFQuestion()"
                >{{ store.currentIndex + 1 >= store.totalItems ? 'Finish' : 'Next' }}</button>
            </template>
        </template>
    </div>
</template>
