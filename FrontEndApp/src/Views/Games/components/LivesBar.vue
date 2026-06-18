<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps<{
    lives: number;
    nextRecoveryAt: string | null;
}>();

const MAX_LIVES = 7;
const countdown = ref('');
let ticker: ReturnType<typeof setInterval> | null = null;

function updateCountdown() {
    if (!props.nextRecoveryAt) {
        countdown.value = '';
        return;
    }
    const diff = new Date(props.nextRecoveryAt).getTime() - Date.now();
    if (diff <= 0) {
        countdown.value = '';
        return;
    }
    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000).toString().padStart(2, '0');
    const s = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
    countdown.value = h > 0 ? `${h}h ${m}m ${s}s` : `${m}m ${s}s`;
}

watch(() => props.nextRecoveryAt, updateCountdown);

onMounted(() => {
    updateCountdown();
    ticker = setInterval(updateCountdown, 1000);
});
onUnmounted(() => {
    if (ticker) clearInterval(ticker);
});
</script>

<template>
    <div class="flex items-center justify-between p-4 rounded-xl border border-[var(--theme-border)] bg-[var(--theme-bg-elevated)]">
        <div>
            <p class="text-xs font-bold tracking-widest text-[var(--theme-text-soft)] uppercase mb-2">Lives</p>
            <div class="flex gap-1">
                <span v-for="i in MAX_LIVES" :key="i" class="text-xl leading-none">
                    <span v-if="i <= lives" class="text-red-500">&#10084;</span>
                    <span v-else class="text-[var(--theme-text-soft)]">&#10084;</span>
                </span>
            </div>
        </div>
        <div class="text-right">
            <span
                v-if="lives >= MAX_LIVES"
                class="px-3 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300"
            >Full</span>
            <template v-else-if="countdown">
                <p class="text-xs text-[var(--theme-text-soft)] mb-1">Next heart in</p>
                <span class="px-3 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300">{{ countdown }}</span>
            </template>
        </div>
    </div>
</template>
