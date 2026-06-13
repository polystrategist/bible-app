<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
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

onMounted(() => store.init());
onUnmounted(() => store.dispose());

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
    <div class="h-full overflow-y-auto p-4 max-w-2xl mx-auto">
        <!-- Hub -->
        <div v-if="activeScreen === 'hub'" class="space-y-3">
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
        </div>

        <QAGroupsList
            v-else-if="activeScreen === 'qa-groups'"
            @back="goHub"
            @select="onQAGroupSelected"
        />
        <QAGameplay
            v-else-if="activeScreen === 'qa-play'"
            @back="activeScreen = 'qa-groups'"
            @exit="goHub"
        />
        <TFGroupsList
            v-else-if="activeScreen === 'tf-groups'"
            @back="goHub"
            @select="onTFGroupSelected"
        />
        <TFGameplay
            v-else-if="activeScreen === 'tf-play'"
            @back="activeScreen = 'tf-groups'"
            @exit="goHub"
        />
        <FPGameplay
            v-else-if="activeScreen === 'fp-play'"
            @exit="goHub"
        />
    </div>
</template>
