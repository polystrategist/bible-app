<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { NButton } from 'naive-ui';
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ exit: [] }>();
const store = useGamesStore();

const ACCENT = '#f59e0b';

const lightboxSrc = ref<string | null>(null);
function openLightbox(src: string) {
    lightboxSrc.value = src;
}
function closeLightbox() {
    lightboxSrc.value = null;
}

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
    if (lightboxSrc.value) {
        if (e.key === 'Escape') closeLightbox();
        return;
    }
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
            <div class="flex items-center gap-2">
                <NButton
                    quaternary
                    size="small"
                    :focusable="false"
                    title="Back to games"
                    @click="emit('exit')"
                ><span class="text-base leading-none mr-1">&larr;</span> Back</NButton>
                <h2 class="text-lg font-bold text-neutral-900 dark:text-neutral-100">4 Pictures 1 Word</h2>
            </div>
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
            <NButton size="large" :color="ACCENT" :focusable="false" @click="emit('exit')">Back to Hub</NButton>
        </div>

        <!-- Game over -->
        <div
            v-else-if="store.gameState === 'gameOver'"
            class="p-6 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-dark-600 text-center space-y-4"
        >
            <p class="text-3xl">💔</p>
            <p class="text-xl font-bold text-neutral-900 dark:text-neutral-100">Out of lives</p>
            <div class="flex gap-3 justify-center pt-1">
                <NButton
                    size="large"
                    :color="ACCENT"
                    :disabled="!store.canPlay"
                    :focusable="false"
                    @click="store.startFPGame()"
                >Try Again</NButton>
                <NButton size="large" :focusable="false" @click="emit('exit')">Exit</NButton>
            </div>
        </div>

        <!-- Playing -->
        <template v-else-if="level">
            <div class="grid grid-cols-2 gap-2 max-w-md mx-auto">
                <button
                    v-for="(src, i) in images"
                    :key="i"
                    type="button"
                    class="block p-0 border-0 aspect-square w-full rounded-xl overflow-hidden bg-neutral-100 dark:bg-dark-700 cursor-zoom-in"
                    @click="openLightbox(src)"
                >
                    <img :src="src" class="w-full h-full object-cover" :alt="`clue ${i + 1}`" @error="onImgError" />
                </button>
            </div>

            <!-- Answer slots -->
            <div class="flex gap-2 justify-center flex-wrap pt-1">
                <div
                    v-for="(letter, i) in store.fpGuessedLetters"
                    :key="i"
                    class="w-11 h-12 rounded-xl flex items-center justify-center text-xl font-extrabold select-none transition-all"
                    :class="letter
                        ? 'bg-amber-500 text-white shadow-md shadow-amber-500/30 cursor-pointer hover:bg-amber-600'
                        : 'bg-neutral-200/70 dark:bg-dark-700'"
                    @click="letter && store.fpRemoveLetter(i)"
                >{{ letter }}</div>
            </div>

            <!-- Letter tray (one letter per tile — used tiles are hidden) -->
            <div class="flex gap-2 justify-center flex-wrap pt-2">
                <template v-for="(letter, i) in store.fpScrambledLetters" :key="i">
                    <NButton
                        v-if="!store.fpTrayUsed[i]"
                        secondary
                        strong
                        size="large"
                        :focusable="false"
                        :style="{ width: '2.75rem', height: '3rem', fontWeight: 700 }"
                        @click="store.fpTapTrayLetter(i)"
                    >{{ letter }}</NButton>
                    <div
                        v-else
                        class="rounded-xl bg-neutral-100/60 dark:bg-dark-700/40"
                        :style="{ width: '2.75rem', height: '3rem' }"
                    />
                </template>
            </div>

            <p class="text-xs text-neutral-400 text-center pt-1">Type or click letters to guess · tap a filled slot to clear it</p>
        </template>

        <!-- Image lightbox -->
        <Teleport to="body">
            <div
                v-if="lightboxSrc"
                class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4"
                @click="closeLightbox"
            >
                <NButton
                    circle
                    size="large"
                    class="!absolute top-4 right-4"
                    color="rgba(255,255,255,0.14)"
                    text-color="#ffffff"
                    title="Close"
                    :focusable="false"
                    @click.stop="closeLightbox"
                >&times;</NButton>
                <img
                    :src="lightboxSrc"
                    class="max-w-full max-h-full rounded-xl object-contain shadow-2xl"
                    alt="clue full view"
                    @click.stop
                />
            </div>
        </Teleport>
    </div>
</template>
