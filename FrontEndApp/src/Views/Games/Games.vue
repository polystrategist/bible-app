<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import { NButton } from 'naive-ui';
import { useGamesStore } from '../../store/useGamesStore';
import LivesBar from './components/LivesBar.vue';
import GameCard from './components/GameCard.vue';
import QAGroupsList from './QuestionAndAnswer/QAGroupsList.vue';
import QAGameplay from './QuestionAndAnswer/QAGameplay.vue';
import TFGroupsList from './TrueOrFalse/TFGroupsList.vue';
import TFGameplay from './TrueOrFalse/TFGameplay.vue';
import FPGameplay from './FourPictures/FPGameplay.vue';

type Screen = 'hub' | 'qa-groups' | 'qa-play' | 'tf-groups' | 'tf-play' | 'fp-play';

const store = useGamesStore();
const activeScreen = ref<Screen>('hub');
const isDev = import.meta.env.DEV;
const isResetting = ref(false);

onMounted(() => store.init());
onUnmounted(() => store.dispose());

async function onDebugReset() {
    if (isResetting.value) return;
    if (!window.confirm('Reset ALL game progress and refill lives? (debug)')) return;
    isResetting.value = true;
    try {
        await store.resetAllProgress();
    } finally {
        isResetting.value = false;
    }
}

function goHub() {
    store.exitGame();
    activeScreen.value = 'hub';
}
function openQA() { activeScreen.value = 'qa-groups'; }
function openTF() { activeScreen.value = 'tf-groups'; }
function openFP() {
    store.startFPGame();
    activeScreen.value = 'fp-play';
}
function onQAGroupSelected(groupId: number) {
    store.startQAGame(groupId);
    activeScreen.value = 'qa-play';
}
function onTFGroupSelected(groupId: number) {
    store.startTFGame(groupId);
    activeScreen.value = 'tf-play';
}
</script>

<template>
    <div class="h-full overflow-hidden p-4 max-w-2xl mx-auto flex flex-col">
        <!-- Hub -->
        <div v-if="activeScreen === 'hub'" class="flex-1 min-h-0 overflow-y-auto space-y-3 pr-1">
            <h1 class="text-xl font-bold text-neutral-900 dark:text-neutral-100 pt-1">Bible Games</h1>
            <LivesBar :lives="store.lives" :next-recovery-at="store.nextRecoveryAt" />
            <div v-if="store.isLoading" class="space-y-3">
                <div v-for="i in 3" :key="i" class="h-28 rounded-xl bg-neutral-100 dark:bg-dark-600 animate-pulse" />
            </div>
            <template v-else>
                <GameCard
                    title="Question & Answer"
                    description="Answer multiple-choice Bible questions and unlock new groups."
                    color="#3b82f6"
                    emoji="📖"
                    :progress="store.qaProgressSummary"
                    @play="openQA"
                />
                <GameCard
                    title="True or False"
                    description="Decide whether each Bible statement is true or false."
                    color="#10b981"
                    emoji="✅"
                    :progress="store.tfProgressSummary"
                    @play="openTF"
                />
                <GameCard
                    title="4 Pictures 1 Word"
                    description="Guess the Bible word from four picture clues."
                    color="#f59e0b"
                    emoji="🖼️"
                    :progress="store.fpProgressSummary"
                    :disabled="!store.canPlay"
                    @play="openFP"
                />
            </template>

            <!-- Debug-only: reset all progress + lives (dev builds only) -->
            <NButton
                v-if="isDev"
                block
                dashed
                type="error"
                class="mt-2"
                :loading="isResetting"
                :focusable="false"
                @click="onDebugReset"
            >{{ isResetting ? 'Resetting…' : '⟳ Reset progress (debug)' }}</NButton>
        </div>

        <QAGroupsList
            v-else-if="activeScreen === 'qa-groups'"
            class="flex-1 min-h-0"
            @back="goHub"
            @select="onQAGroupSelected"
        />
        <QAGameplay
            v-else-if="activeScreen === 'qa-play'"
            class="flex-1 min-h-0 overflow-y-auto pr-1"
            @back="activeScreen = 'qa-groups'"
            @exit="goHub"
        />
        <TFGroupsList
            v-else-if="activeScreen === 'tf-groups'"
            class="flex-1 min-h-0"
            @back="goHub"
            @select="onTFGroupSelected"
        />
        <TFGameplay
            v-else-if="activeScreen === 'tf-play'"
            class="flex-1 min-h-0 overflow-y-auto pr-1"
            @back="activeScreen = 'tf-groups'"
            @exit="goHub"
        />
        <FPGameplay
            v-else-if="activeScreen === 'fp-play'"
            class="flex-1 min-h-0 overflow-y-auto pr-1"
            @exit="goHub"
        />
    </div>
</template>
