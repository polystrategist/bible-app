<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue';
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ exit: [] }>();
const store = useGamesStore();

const level = computed(() => store.currentFpLevel);
const images = computed(() => {
    if (!level.value) return [];
    // Served by the gameimg:// custom protocol (Electron main → userData/Games/fp_images).
    return [level.value.image1, level.value.image2, level.value.image3, level.value.image4]
        .filter(Boolean)
        .map((name) => `gameimg://img/${name}`);
});

function onImgError(e: Event) {
    const el = e.target as HTMLImageElement;
    el.style.visibility = 'hidden';
}

function onKeyDown(e: KeyboardEvent) {
    if (store.gameState !== 'playing') return;
    const letter = e.key.toUpperCase();
    if (/^[A-Z]$/.test(letter)) {
        store.fpTapLetter(letter);
    } else if (e.key === 'Backspace') {
        const guessed = store.fpGuessedLetters;
        for (let i = guessed.length - 1; i >= 0; i--) {
            if (guessed[i] !== '') {
                store.fpRemoveLetter(i);
                break;
            }
        }
    }
}

onMounted(() => window.addEventListener('keydown', onKeyDown));
onUnmounted(() => window.removeEventListener('keydown', onKeyDown));
</script>

<template>
    <div class="space-y-4">
        <div class="flex items-center justify-between">
            <h2 class="text-lg font-bold text-neutral-900 dark:text-neutral-100">4 Pictures 1 Word</h2>
            <div class="flex items-center gap-3 text-sm text-neutral-500">
                <span class="text-red-500">&#10084; {{ store.lives }}</span>
                <span>{{ store.fpProgressSummary.completed }}/{{ store.fpProgressSummary.total }}</span>
            </div>
        </div>

        <!-- Completed -->
        <div
            v-if="store.gameState === 'completed'"
            class="p-6 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-dark-600 text-center space-y-4"
        >
            <p class="text-4xl">🏆</p>
            <p class="text-xl font-bold text-neutral-900 dark:text-neutral-100">All levels complete!</p>
            <p class="text-neutral-500">You solved all {{ store.fpProgressSummary.total }} levels.</p>
            <button class="px-5 py-2 rounded-xl bg-amber-500 text-white font-semibold hover:bg-amber-600" @click="emit('exit')">Back to Hub</button>
        </div>

        <!-- Game over -->
        <div
            v-else-if="store.gameState === 'gameOver'"
            class="p-6 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-dark-600 text-center space-y-4"
        >
            <p class="text-3xl">💔</p>
            <p class="text-xl font-bold text-neutral-900 dark:text-neutral-100">Out of lives</p>
            <div class="flex gap-3 justify-center pt-1">
                <button
                    class="px-5 py-2 rounded-xl text-white font-semibold"
                    :class="store.canPlay ? 'bg-amber-500 hover:bg-amber-600' : 'bg-neutral-300 dark:bg-neutral-600 cursor-not-allowed'"
                    :disabled="!store.canPlay"
                    @click="store.canPlay && store.startFPGame()"
                >Try Again</button>
                <button class="px-5 py-2 rounded-xl border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-dark-700" @click="emit('exit')">Exit</button>
            </div>
        </div>

        <!-- Playing -->
        <template v-else-if="level">
            <div class="grid grid-cols-2 gap-2">
                <div
                    v-for="(src, i) in images"
                    :key="i"
                    class="aspect-square rounded-xl overflow-hidden bg-neutral-100 dark:bg-dark-700"
                >
                    <img :src="src" class="w-full h-full object-cover" :alt="`clue ${i + 1}`" @error="onImgError" />
                </div>
            </div>

            <!-- Answer slots -->
            <div class="flex gap-2 justify-center flex-wrap">
                <div
                    v-for="(letter, i) in store.fpGuessedLetters"
                    :key="i"
                    class="w-10 h-10 rounded-lg border-2 flex items-center justify-center text-lg font-bold select-none transition-colors"
                    :class="letter ? 'border-amber-400 bg-amber-50 dark:bg-amber-900 text-amber-700 dark:text-amber-200 cursor-pointer' : 'border-neutral-300 dark:border-neutral-600'"
                    @click="letter && store.fpRemoveLetter(i)"
                >{{ letter }}</div>
            </div>

            <!-- Letter tray -->
            <div class="flex gap-2 justify-center flex-wrap">
                <button
                    v-for="(letter, i) in store.fpScrambledLetters"
                    :key="i"
                    class="w-10 h-10 rounded-lg bg-neutral-100 dark:bg-dark-700 hover:bg-neutral-200 dark:hover:bg-neutral-600 flex items-center justify-center text-sm font-bold text-neutral-700 dark:text-neutral-200 transition-colors"
                    @click="store.fpTapLetter(letter)"
                >{{ letter }}</button>
            </div>

            <p class="text-xs text-neutral-400 text-center">Type or click letters to guess · click a filled slot to clear it</p>
        </template>
    </div>
</template>
