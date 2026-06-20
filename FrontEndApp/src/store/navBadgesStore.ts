import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import session from '../util/session';

/**
 * Sidebar nav-badge state.
 *
 * - Games hub "attention dot": shows when the hub hasn't been visited in the
 *   last 10 hours, clears on visit (mirrors mobile ReaderBottomNavigation).
 * - Prayer "visited today" flag: visiting the Prayer page clears its nav dot
 *   for the rest of the day (the dot's base condition — "haven't prayed today" —
 *   lives in the streak store and is combined by the consumer, App.vue).
 *
 * Local-only (not synced). Devotion's dot is still derived purely from its
 * streak store by the consumer.
 */
const GAMES_LAST_VISITED_KEY = 'games_hub_last_visited_at';
const GAMES_ATTENTION_DELAY_MS = 10 * 60 * 60 * 1000; // 10 hours
const TICK_MS = 60 * 1000; // re-evaluate the boundaries every minute (mirrors mobile's timer)
const PRAYER_VISITED_DAY_KEY = 'prayer_dot_last_visited_day';

/** Local calendar date (YYYY-MM-DD) for a timestamp. */
function dayKeyOf(ts: number): string {
    const d = new Date(ts);
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${d.getFullYear()}-${mm}-${dd}`;
}

export const useNavBadgesStore = defineStore('navBadgesStoreId', () => {
    const gamesLastVisited = ref<string | null>(session.get(GAMES_LAST_VISITED_KEY) ?? null);
    // Day (YYYY-MM-DD) the Prayer page was last opened.
    const prayerVisitedDay = ref<string | null>(session.get(PRAYER_VISITED_DAY_KEY) ?? null);
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

    // True once the Prayer page has been opened today; re-derives daily via the
    // ticker (`now`) so the dot can reappear the next day if still unprayed.
    const prayerVisitedToday = computed(
        () => prayerVisitedDay.value !== null && prayerVisitedDay.value === dayKeyOf(now.value)
    );

    /** Record a Prayer-page visit now, clearing the prayer dot until tomorrow. */
    function markPrayerVisited() {
        const key = dayKeyOf(Date.now());
        session.set(PRAYER_VISITED_DAY_KEY, key);
        prayerVisitedDay.value = key;
    }

    return { showGamesDot, markGamesVisited, prayerVisitedToday, markPrayerVisited };
});
