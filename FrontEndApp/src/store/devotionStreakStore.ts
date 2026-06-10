import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { debouncedRunSync } from '../util/Sync/sync';

/** A single day in the current week's strip on the completed-devotion view. */
export interface DevotionStreakDay {
    date: Date;
    completed: boolean;
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
 * Devotion day-streak — the set of local calendar dates the user completed the
 * Daily Devotion. Days are persisted/synced via the bridge (table `devotion_days`,
 * created-only, union-merged); the streak itself is computed here so two devices
 * always converge on the union of their days. Mirrors the mobile
 * DevotionStreakProvider and the prayer streak store.
 */
export const useDevotionStreakStore = defineStore('devotionStreakStoreId', () => {
    const days = ref<Set<string>>(new Set());

    const completedToday = computed(() => days.value.has(dayKey()));

    /** Consecutive-day streak ending today (or yesterday if today isn't done). */
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

    /** Current week's Mon→Sun strip with completed/today flags. */
    const weekDays = computed<DevotionStreakDay[]>(() => {
        const today = dateOnly(new Date());
        // JS getDay(): 0=Sun..6=Sat → offset so Monday starts the week.
        const offset = (today.getDay() + 6) % 7;
        const monday = new Date(today.getTime() - offset * 86400000);
        return Array.from({ length: 7 }, (_, i) => {
            const date = new Date(monday.getTime() + i * 86400000);
            return {
                date,
                completed: days.value.has(dayKey(date)),
                isToday: dayKey(date) === dayKey(today),
            };
        });
    });

    async function loadDays() {
        const rows = await window.browserWindow.getDevotionDays();
        days.value = new Set((rows ?? []).map((r) => r.day));
    }

    /** Record today as completed (idempotent) and trigger a sync. */
    async function recordTodayCompleted() {
        const day = await window.browserWindow.markDevotionToday();
        if (day && !days.value.has(day)) {
            days.value = new Set([...days.value, day]);
            debouncedRunSync();
        }
    }

    return { days, completedToday, currentStreak, weekDays, loadDays, recordTodayCompleted };
});
