import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import correctSoundUrl from '../assets/sounds/correct.mp3';
import wrongSoundUrl from '../assets/sounds/wrong.mp3';

export type GameType = 'qa' | 'tf' | 'fp';
export type GameState = 'idle' | 'playing' | 'answered' | 'gameOver' | 'completed';

interface GroupProgress {
    group_id: number;
    is_completed: number;
    high_score_percentage: number;
    times_played: number;
    completed_at: string | null;
    updated_at: string;
}

interface QAQuestion {
    id: number;
    group_id: number;
    question: string;
    options: string[];
    answer: number;
    proof: string;
    explanation: string | null;
}

interface TFStatement {
    id: number;
    group_id: number;
    statement: string;
    answer: number; // 1 = True, 0 = False
    proof: string;
    explanation: string | null;
}

interface FPLevel {
    id: number;
    level_order: number;
    word: string;
    image1: string;
    image2: string;
    image3: string;
    image4: string;
}

function playSound(url: string) {
    try {
        const audio = new Audio(url);
        void audio.play();
    } catch (_) {
        /* best effort — never let a sound failure break gameplay */
    }
}

export const useGamesStore = defineStore('useGamesStore', () => {
    // ── Lives ──────────────────────────────────────────────────────────────
    const lives = ref(7);
    const nextRecoveryAt = ref<string | null>(null);
    const isLoading = ref(false);
    let recoveryTimer: ReturnType<typeof setTimeout> | null = null;

    // ── Catalog + progress ───────────────────────────────────────────────────
    const qaGroups = ref<Array<{ id: number; name: string; display_order: number; required_completed: number; passing_score: number }>>([]);
    const qaGroupProgress = ref<Record<number, GroupProgress>>({});
    const tfGroups = ref<Array<{ id: number; name: string; display_order: number; required_completed: number; passing_score: number }>>([]);
    const tfGroupProgress = ref<Record<number, GroupProgress>>({});
    const fpLevels = ref<FPLevel[]>([]);
    const fpSolvedIds = ref<Set<number>>(new Set());
    const fpImagesBasePath = ref('');

    // ── Active game state ──────────────────────────────────────────────────
    const activeGameType = ref<GameType | null>(null);
    const currentGroupId = ref<number | null>(null);
    const gameState = ref<GameState>('idle');
    const currentItems = ref<Array<QAQuestion | TFStatement>>([]);
    const currentIndex = ref(0);
    const score = ref(0);
    const streak = ref(0);
    const bestStreak = ref(0);
    const lastAnswerCorrect = ref<boolean | null>(null);
    const selectedAnswerIndex = ref<number | null>(null);
    const shuffledOptions = ref<string[]>([]);
    const shuffledCorrectIndex = ref(0);
    const newlyPassed = ref(false);

    // ── FP active state ──────────────────────────────────────────────────────
    const currentFpLevelIndex = ref(0);
    const fpGuessedLetters = ref<string[]>([]);
    const fpScrambledLetters = ref<string[]>([]);
    // Whether each tray tile has been consumed (one letter per tile).
    const fpTrayUsed = ref<boolean[]>([]);
    // For each answer slot, which tray tile filled it (so clearing frees the tile).
    const fpSlotTray = ref<(number | null)[]>([]);

    // ── Computed ─────────────────────────────────────────────────────────────
    const qaProgressSummary = computed(() => ({
        completed: Object.values(qaGroupProgress.value).filter((p) => p.is_completed).length,
        total: qaGroups.value.length,
    }));
    const tfProgressSummary = computed(() => ({
        completed: Object.values(tfGroupProgress.value).filter((p) => p.is_completed).length,
        total: tfGroups.value.length,
    }));
    const fpProgressSummary = computed(() => ({
        completed: fpSolvedIds.value.size,
        total: fpLevels.value.length,
    }));
    const currentQuestion = computed((): QAQuestion | TFStatement | null =>
        currentIndex.value < currentItems.value.length ? currentItems.value[currentIndex.value] : null,
    );
    const totalItems = computed(() => currentItems.value.length);
    const canPlay = computed(() => lives.value > 0);
    const scorePercentage = computed(() =>
        totalItems.value === 0 ? 0 : Math.round((score.value / totalItems.value) * 100),
    );
    const currentFpLevel = computed((): FPLevel | null => {
        const unsolved = fpLevels.value.filter((l) => !fpSolvedIds.value.has(l.id));
        return unsolved[currentFpLevelIndex.value] ?? null;
    });

    function qaIsGroupUnlocked(groupId: number) {
        const group = qaGroups.value.find((g) => g.id === groupId);
        if (!group || group.required_completed === 0) return true;
        return Object.values(qaGroupProgress.value).filter((p) => p.is_completed).length >= group.required_completed;
    }
    function tfIsGroupUnlocked(groupId: number) {
        const group = tfGroups.value.find((g) => g.id === groupId);
        if (!group || group.required_completed === 0) return true;
        return Object.values(tfGroupProgress.value).filter((p) => p.is_completed).length >= group.required_completed;
    }

    // ── Lives helpers ──────────────────────────────────────────────────────
    function scheduleRecoveryTimer() {
        if (recoveryTimer) clearTimeout(recoveryTimer);
        if (!nextRecoveryAt.value) return;
        const delay = new Date(nextRecoveryAt.value).getTime() - Date.now();
        if (delay <= 0) {
            void refreshLives();
            return;
        }
        // Cap the timer so a far-future recovery still re-checks periodically.
        recoveryTimer = setTimeout(() => void refreshLives(), Math.min(delay + 500, 2_147_483_000));
    }

    async function refreshLives() {
        if (!window.isElectron) return;
        lives.value = await window.browserWindow.gameGetLives();
        nextRecoveryAt.value = await window.browserWindow.gameNextRecoveryAt();
        scheduleRecoveryTimer();
    }

    async function loseLife() {
        if (!window.isElectron) return;
        lives.value = await window.browserWindow.gameLoseLife();
        nextRecoveryAt.value = await window.browserWindow.gameNextRecoveryAt();
        scheduleRecoveryTimer();
    }

    // ── Data loading ───────────────────────────────────────────────────────
    async function loadQAData() {
        const [groups, progress] = await Promise.all([
            window.browserWindow.qaGetGroups(),
            window.browserWindow.qaGetAllGroupProgress(),
        ]);
        qaGroups.value = groups;
        qaGroupProgress.value = Object.fromEntries(progress.map((p) => [p.group_id, p]));
    }
    async function loadTFData() {
        const [groups, progress] = await Promise.all([
            window.browserWindow.tfGetGroups(),
            window.browserWindow.tfGetAllGroupProgress(),
        ]);
        tfGroups.value = groups;
        tfGroupProgress.value = Object.fromEntries(progress.map((p) => [p.group_id, p]));
    }
    async function loadFPData() {
        const [levels, solvedIds, basePath] = await Promise.all([
            window.browserWindow.fpGetLevels(),
            window.browserWindow.fpGetSolvedLevelIds(),
            window.browserWindow.fpGetImagesBasePath(),
        ]);
        fpLevels.value = levels;
        fpSolvedIds.value = new Set(solvedIds);
        fpImagesBasePath.value = basePath;
    }

    async function init() {
        if (!window.isElectron) return;
        isLoading.value = true;
        try {
            await Promise.all([refreshLives(), loadQAData(), loadTFData(), loadFPData()]);
        } finally {
            isLoading.value = false;
        }
    }

    // Refresh lives + synced progress after a pull sync, without touching an
    // in-progress game. FP is local-only, so it never changes from a pull.
    async function refreshAfterSync() {
        if (!window.isElectron) return;
        await Promise.all([refreshLives(), loadQAData(), loadTFData()]);
    }

    // ── Q&A flow ───────────────────────────────────────────────────────────
    function shuffleQAOptions(q: QAQuestion) {
        const indexed = q.options.map((opt, i) => ({ i, opt }));
        for (let j = indexed.length - 1; j > 0; j--) {
            const k = Math.floor(Math.random() * (j + 1));
            [indexed[j], indexed[k]] = [indexed[k], indexed[j]];
        }
        shuffledOptions.value = indexed.map((x) => x.opt);
        shuffledCorrectIndex.value = indexed.findIndex((x) => x.i === q.answer);
    }

    function resetRoundState() {
        currentIndex.value = 0;
        score.value = 0;
        streak.value = 0;
        bestStreak.value = 0;
        lastAnswerCorrect.value = null;
        selectedAnswerIndex.value = null;
        newlyPassed.value = false;
    }

    async function startQAGame(groupId: number) {
        if (!canPlay.value) return;
        activeGameType.value = 'qa';
        currentGroupId.value = groupId;
        const questions = await window.browserWindow.qaGetQuestionsForGroup(groupId);
        currentItems.value = questions;
        resetRoundState();
        if (questions.length) shuffleQAOptions(questions[0] as QAQuestion);
        gameState.value = 'playing';
    }

    async function submitQAAnswer(answerIndex: number) {
        if (gameState.value !== 'playing') return;
        const correct = answerIndex === shuffledCorrectIndex.value;
        selectedAnswerIndex.value = answerIndex;
        lastAnswerCorrect.value = correct;
        if (correct) {
            score.value++;
            streak.value++;
            if (streak.value > bestStreak.value) bestStreak.value = streak.value;
            playSound(correctSoundUrl);
        } else {
            streak.value = 0;
            playSound(wrongSoundUrl);
            await loseLife();
        }
        gameState.value = 'answered';
    }

    async function finalizeQAGame() {
        if (currentGroupId.value == null) return;
        const group = qaGroups.value.find((g) => g.id === currentGroupId.value);
        if (!group) return;
        const result = await window.browserWindow.qaSaveGroupProgress({
            groupId: currentGroupId.value,
            correctCount: score.value,
            totalCount: totalItems.value,
            passingScore: group.passing_score,
        });
        newlyPassed.value = result.newlyPassed;
        await loadQAData();
    }

    async function nextQAQuestion() {
        if (gameState.value !== 'answered') return;
        selectedAnswerIndex.value = null;
        lastAnswerCorrect.value = null;
        if (lives.value <= 0) {
            await finalizeQAGame();
            gameState.value = 'gameOver';
            return;
        }
        currentIndex.value++;
        if (currentIndex.value >= currentItems.value.length) {
            await finalizeQAGame();
            gameState.value = 'completed';
        } else {
            shuffleQAOptions(currentItems.value[currentIndex.value] as QAQuestion);
            gameState.value = 'playing';
        }
    }

    // ── True/False flow ──────────────────────────────────────────────────────
    async function startTFGame(groupId: number) {
        if (!canPlay.value) return;
        activeGameType.value = 'tf';
        currentGroupId.value = groupId;
        const statements = await window.browserWindow.tfGetStatementsForGroup(groupId);
        currentItems.value = statements;
        resetRoundState();
        gameState.value = 'playing';
    }

    async function submitTFAnswer(isTrue: boolean) {
        if (gameState.value !== 'playing') return;
        const stmt = currentItems.value[currentIndex.value] as TFStatement;
        const correct = (isTrue ? 1 : 0) === stmt.answer;
        selectedAnswerIndex.value = isTrue ? 1 : 0;
        lastAnswerCorrect.value = correct;
        if (correct) {
            score.value++;
            streak.value++;
            if (streak.value > bestStreak.value) bestStreak.value = streak.value;
            playSound(correctSoundUrl);
        } else {
            streak.value = 0;
            playSound(wrongSoundUrl);
            await loseLife();
        }
        gameState.value = 'answered';
    }

    async function finalizeTFGame() {
        if (currentGroupId.value == null) return;
        const group = tfGroups.value.find((g) => g.id === currentGroupId.value);
        if (!group) return;
        const result = await window.browserWindow.tfSaveGroupProgress({
            groupId: currentGroupId.value,
            correctCount: score.value,
            totalCount: totalItems.value,
            passingScore: group.passing_score,
        });
        newlyPassed.value = result.newlyPassed;
        await loadTFData();
    }

    async function nextTFQuestion() {
        if (gameState.value !== 'answered') return;
        selectedAnswerIndex.value = null;
        lastAnswerCorrect.value = null;
        if (lives.value <= 0) {
            await finalizeTFGame();
            gameState.value = 'gameOver';
            return;
        }
        currentIndex.value++;
        if (currentIndex.value >= currentItems.value.length) {
            await finalizeTFGame();
            gameState.value = 'completed';
        } else {
            gameState.value = 'playing';
        }
    }

    // ── Four Pictures flow ─────────────────────────────────────────────────
    function buildFPScramble(word: string): string[] {
        const letters = word.toUpperCase().split('');
        const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const target = Math.max(12, letters.length);
        while (letters.length < target) {
            letters.push(alphabet[Math.floor(Math.random() * 26)]);
        }
        for (let j = letters.length - 1; j > 0; j--) {
            const k = Math.floor(Math.random() * (j + 1));
            [letters[j], letters[k]] = [letters[k], letters[j]];
        }
        return letters;
    }

    function loadFpLevelIntoState() {
        const level = currentFpLevel.value;
        if (!level) return;
        fpGuessedLetters.value = new Array(level.word.length).fill('');
        fpScrambledLetters.value = buildFPScramble(level.word);
        fpTrayUsed.value = new Array(fpScrambledLetters.value.length).fill(false);
        fpSlotTray.value = new Array(level.word.length).fill(null);
    }

    // Clear all placed letters, freeing every tray tile (used when a guess is wrong).
    function clearFpGuess() {
        fpGuessedLetters.value = fpGuessedLetters.value.map(() => '');
        fpSlotTray.value = fpSlotTray.value.map(() => null);
        fpTrayUsed.value = fpTrayUsed.value.map(() => false);
    }

    function startFPGame() {
        if (!canPlay.value) return;
        activeGameType.value = 'fp';
        currentFpLevelIndex.value = 0;
        newlyPassed.value = false;
        const level = currentFpLevel.value;
        if (!level) {
            gameState.value = 'completed';
            return;
        }
        loadFpLevelIntoState();
        gameState.value = 'playing';
    }

    // Place a specific tray tile (by index) into the next empty answer slot and
    // mark that tile as consumed so it can't be used again.
    function fpTapTrayLetter(trayIndex: number) {
        if (gameState.value !== 'playing') return;
        if (fpTrayUsed.value[trayIndex]) return;
        const emptyIndex = fpGuessedLetters.value.findIndex((l) => l === '');
        if (emptyIndex === -1) return;

        const nextGuess = [...fpGuessedLetters.value];
        nextGuess[emptyIndex] = fpScrambledLetters.value[trayIndex];
        fpGuessedLetters.value = nextGuess;

        const nextSlotTray = [...fpSlotTray.value];
        nextSlotTray[emptyIndex] = trayIndex;
        fpSlotTray.value = nextSlotTray;

        const nextUsed = [...fpTrayUsed.value];
        nextUsed[trayIndex] = true;
        fpTrayUsed.value = nextUsed;

        void checkFPAnswer();
    }

    // Keyboard entry: consume the first unused tray tile matching the letter.
    function fpTapLetter(letter: string) {
        if (gameState.value !== 'playing') return;
        const trayIndex = fpScrambledLetters.value.findIndex(
            (l, i) => l === letter && !fpTrayUsed.value[i],
        );
        if (trayIndex === -1) return;
        fpTapTrayLetter(trayIndex);
    }

    function fpRemoveLetter(index: number) {
        if (gameState.value !== 'playing') return;
        if (fpGuessedLetters.value[index] === '') return;

        const trayIndex = fpSlotTray.value[index];
        if (trayIndex != null) {
            const nextUsed = [...fpTrayUsed.value];
            nextUsed[trayIndex] = false;
            fpTrayUsed.value = nextUsed;
        }

        const nextGuess = [...fpGuessedLetters.value];
        nextGuess[index] = '';
        fpGuessedLetters.value = nextGuess;

        const nextSlotTray = [...fpSlotTray.value];
        nextSlotTray[index] = null;
        fpSlotTray.value = nextSlotTray;
    }

    async function checkFPAnswer() {
        const level = currentFpLevel.value;
        if (!level) return;
        const guessed = fpGuessedLetters.value.join('').toUpperCase();
        if (guessed.length < level.word.length || fpGuessedLetters.value.some((l) => l === '')) return;

        if (guessed === level.word.toUpperCase()) {
            playSound(correctSoundUrl);
            await window.browserWindow.fpMarkLevelSolved(level.id);
            fpSolvedIds.value = new Set([...fpSolvedIds.value, level.id]);
            const remaining = fpLevels.value.filter((l) => !fpSolvedIds.value.has(l.id));
            if (remaining.length === 0) {
                gameState.value = 'completed';
            } else {
                currentFpLevelIndex.value = 0;
                loadFpLevelIntoState();
            }
        } else {
            playSound(wrongSoundUrl);
            await loseLife();
            if (lives.value <= 0) {
                gameState.value = 'gameOver';
                return;
            }
            clearFpGuess();
        }
    }

    // ── Lifecycle ──────────────────────────────────────────────────────────
    function exitGame() {
        gameState.value = 'idle';
        activeGameType.value = null;
        currentGroupId.value = null;
        currentItems.value = [];
        resetRoundState();
        shuffledOptions.value = [];
        shuffledCorrectIndex.value = 0;
        fpGuessedLetters.value = [];
        fpScrambledLetters.value = [];
        fpTrayUsed.value = [];
        fpSlotTray.value = [];
    }

    function dispose() {
        if (recoveryTimer) clearTimeout(recoveryTimer);
        recoveryTimer = null;
    }

    // Debug: wipe all progress + refill lives, then reload the catalog.
    async function resetAllProgress() {
        if (!window.isElectron) return;
        exitGame();
        await window.browserWindow.gameResetProgress();
        await init();
    }

    return {
        // Lives
        lives, nextRecoveryAt, isLoading, refreshLives, loseLife,
        // Q&A
        qaGroups, qaGroupProgress, qaProgressSummary, qaIsGroupUnlocked,
        startQAGame, submitQAAnswer, nextQAQuestion,
        // T/F
        tfGroups, tfGroupProgress, tfProgressSummary, tfIsGroupUnlocked,
        startTFGame, submitTFAnswer, nextTFQuestion,
        // FP
        fpLevels, fpSolvedIds, fpImagesBasePath, fpProgressSummary,
        currentFpLevel, fpGuessedLetters, fpScrambledLetters, fpTrayUsed,
        startFPGame, fpTapLetter, fpTapTrayLetter, fpRemoveLetter,
        // Shared game state
        activeGameType, currentGroupId, gameState, currentQuestion,
        totalItems, canPlay, scorePercentage, score, streak, bestStreak,
        lastAnswerCorrect, selectedAnswerIndex, shuffledOptions, shuffledCorrectIndex,
        currentIndex, newlyPassed, exitGame,
        // Lifecycle
        init, refreshAfterSync, dispose, resetAllProgress,
    };
});
