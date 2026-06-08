import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { debouncedRunSync } from '../util/Sync/sync';

/** A single day in the current week's strip on the Finished screen. */
export interface StreakDay {
    date: Date;
    prayed: boolean;
    isToday: boolean;
}

/** Local calendar date (YYYY-MM-DD) for a Date (defaults to now). */
function dayKey(date = new Date()): string {
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const dd = String(date.getDate()).padStart(2, '0');
    return `${date.getFullYear()}-${mm}-${dd}`;
}

function dateOnly(d: Date): Date {
    return new Date(d.getFullYear(), d.getMonth(), d.getDate());
}

/**
 * Prayer day-streak — the set of local calendar dates the user finished a
 * prayer session. Days are persisted/synced via the bridge (table `prayer_days`,
 * created-only, union-merged); the streak itself is computed here so two devices
 * always converge on the union of their days. Mirrors the mobile
 * PrayerStreakProvider.
 */
export const usePrayerStreakStore = defineStore('prayerStreakStoreId', () => {
    const days = ref<Set<string>>(new Set());
    // Per-day total prayer time in seconds, keyed by day (YYYY-MM-DD).
    const durations = ref<Map<string, number>>(new Map());

    const prayedToday = computed(() => days.value.has(dayKey()));

    /** Total prayer time (seconds) for a day (defaults to today). */
    function durationForDay(day = dayKey()): number {
        return durations.value.get(day) ?? 0;
    }
    const todayDuration = computed(() => durationForDay());

    /** Consecutive-day streak ending today (or yesterday if today isn't prayed). */
    const currentStreak = computed(() => {
        let anchor = dateOnly(new Date());
        if (!days.value.has(dayKey())) {
            anchor = new Date(anchor.getTime() - 86400000);
            if (!days.value.has(dayKey(anchor))) return 0;
        }
        let streak = 0;
        let d = anchor;
        while (days.value.has(dayKey(d))) {
            streak++;
            d = new Date(d.getTime() - 86400000);
        }
        return streak;
    });

    /** Current week's Mon→Sun strip with prayed/today flags. */
    const weekDays = computed<StreakDay[]>(() => {
        const today = dateOnly(new Date());
        // JS getDay(): 0=Sun..6=Sat → offset so Monday starts the week.
        const offset = (today.getDay() + 6) % 7;
        const monday = new Date(today.getTime() - offset * 86400000);
        return Array.from({ length: 7 }, (_, i) => {
            const date = new Date(monday.getTime() + i * 86400000);
            return {
                date,
                prayed: days.value.has(dayKey(date)),
                isToday: dayKey(date) === dayKey(today),
            };
        });
    });

    async function loadDays() {
        const rows = await window.browserWindow.getPrayerDays();
        days.value = new Set((rows ?? []).map((r) => r.day));
        durations.value = new Map((rows ?? []).map((r) => [r.day, r.duration ?? 0]));
    }

    /**
     * Record today as prayed and add `durationSeconds` to today's prayer-time
     * total, then trigger a sync.
     */
    async function recordTodayPrayed(durationSeconds = 0) {
        const day = await window.browserWindow.markPrayedToday(durationSeconds);
        if (!day) return;
        days.value = new Set([...days.value, day]);
        if (durationSeconds > 0) {
            durations.value = new Map(durations.value).set(day, durationForDay(day) + durationSeconds);
        }
        debouncedRunSync();
    }

    return { days, durations, prayedToday, todayDuration, durationForDay, currentStreak, weekDays, loadDays, recordTodayPrayed };
});
