import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import session from '../util/session';

/**
 * Sidebar nav-badge state. Currently owns the Games hub "attention dot",
 * mirroring the mobile ReaderBottomNavigation games dot: the dot shows when the
 * game hub hasn't been visited in the last 10 hours, and clears on visit.
 *
 * Local-only (not synced) — mirrors mobile, which stores the timestamp in
 * SharedPreferences (key `games_hub_last_visited_at`). Prayer/Devotion dots are
 * derived directly from their streak stores by the consumer (App.vue), so they
 * are not duplicated here.
 */
const GAMES_LAST_VISITED_KEY = 'games_hub_last_visited_at';
const GAMES_ATTENTION_DELAY_MS = 10 * 60 * 60 * 1000; // 10 hours
const TICK_MS = 60 * 1000; // re-evaluate the 10h boundary every minute (mirrors mobile's timer)

export const useNavBadgesStore = defineStore('navBadgesStoreId', () => {
    const gamesLastVisited = ref<string | null>(session.get(GAMES_LAST_VISITED_KEY) ?? null);
    const now = ref<number>(Date.now());

    // Single app-lifetime ticker (the store is a singleton), so the dot
    // reappears within ~1 minute of crossing the 10h boundary.
    setInterval(() => {
        now.value = Date.now();
    }, TICK_MS);

    const showGamesDot = computed(() => {
        if (!gamesLastVisited.value) return true;
        const last = new Date(gamesLastVisited.value).getTime();
        if (Number.isNaN(last)) return true;
        return now.value - last >= GAMES_ATTENTION_DELAY_MS;
    });

    /** Record a game-hub visit now, clearing the dot for the next 10 hours. */
    function markGamesVisited() {
        const iso = new Date().toISOString();
        session.set(GAMES_LAST_VISITED_KEY, iso);
        gamesLastVisited.value = iso;
    }

    return { showGamesDot, markGamesVisited };
});
