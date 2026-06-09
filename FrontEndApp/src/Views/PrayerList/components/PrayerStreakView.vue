<script lang="ts" setup>
import { computed } from 'vue';
import { Icon } from '@iconify/vue';
import { usePrayerStreakStore } from '../../../store/prayerStreakStore';

const streak = usePrayerStreakStore();

const weekLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
];

/** Local calendar date (YYYY-MM-DD), matching the store's day keys. */
function dayKey(date: Date): string {
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const dd = String(date.getDate()).padStart(2, '0');
    return `${date.getFullYear()}-${mm}-${dd}`;
}

interface DayCell {
    day: number;
    prayed: boolean;
    isToday: boolean;
}

/** Current month grid: leading blanks (Monday-based) then each day, padded to
 * whole weeks. Recomputes if the prayed-days set changes. */
const calendar = computed(() => {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    const todayKey = dayKey(new Date(year, month, now.getDate()));
    const first = new Date(year, month, 1);
    // JS getDay(): 0=Sun..6=Sat → offset so Monday starts the week.
    const offset = (first.getDay() + 6) % 7;
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const cells: (DayCell | null)[] = [];
    for (let i = 0; i < offset; i++) cells.push(null);
    let prayedThisMonth = 0;
    for (let d = 1; d <= daysInMonth; d++) {
        const k = dayKey(new Date(year, month, d));
        const prayed = streak.days.has(k);
        if (prayed) prayedThisMonth++;
        cells.push({ day: d, prayed, isToday: k === todayKey });
    }
    while (cells.length % 7 !== 0) cells.push(null);

    return {
        label: `${monthNames[month]} ${year}`,
        cells,
        prayedThisMonth,
        daysInMonth,
    };
});
</script>

<template>
    <div class="streak-view">
        <!-- Summary: big consecutive-day count + this week's strip -->
        <div class="streak">
            <div class="streak__head">
                <Icon icon="lucide:flame" class="streak__flame" />
                <div class="streak__num">{{ streak.currentStreak }}</div>
            </div>
            <div class="streak__label">day streak</div>
            <div class="streak__hint">
                {{ streak.prayedToday
                    ? 'You prayed today — keep it going!'
                    : 'Pray today to keep your streak alive.' }}
            </div>
            <div class="streak__week">
                <div v-for="(d, i) in streak.weekDays" :key="i" class="pip">
                    <span class="pip__label">{{ weekLabels[i] }}</span>
                    <span
                        class="pip__dot"
                        :class="{ 'pip__dot--filled': d.prayed, 'pip__dot--today': d.isToday }"
                    >
                        <Icon v-if="d.prayed" icon="lucide:check" />
                        <template v-else>{{ d.date.getDate() }}</template>
                    </span>
                </div>
            </div>
        </div>

        <!-- Current month calendar -->
        <div class="cal">
            <div class="cal__head">
                <h3 class="cal__title">{{ calendar.label }}</h3>
                <span class="cal__count">
                    {{ calendar.prayedThisMonth }} / {{ calendar.daysInMonth }} days
                </span>
            </div>
            <div class="cal__grid cal__grid--labels">
                <span v-for="l in weekLabels" :key="l" class="cal__wd">{{ l }}</span>
            </div>
            <div class="cal__grid">
                <template v-for="(c, i) in calendar.cells" :key="i">
                    <span v-if="!c" class="cal__cell cal__cell--blank" />
                    <span v-else class="cal__cell">
                        <span
                            class="cal__day"
                            :class="{ 'cal__day--filled': c.prayed, 'cal__day--today': c.isToday }"
                        >
                            <Icon v-if="c.prayed" icon="lucide:check" />
                            <template v-else>{{ c.day }}</template>
                        </span>
                    </span>
                </template>
            </div>
        </div>
    </div>
</template>

<style scoped>
.streak-view { display: flex; flex-direction: column; gap: 14px; }

/* Summary card (mirrors PrayerFinished's streak card) */
.streak {
    width: 100%;
    padding: 20px 16px;
    border: 1px solid var(--theme-border);
    border-radius: 20px;
    background: var(--theme-bg-soft);
    text-align: center;
}
.streak__head { display: flex; align-items: center; justify-content: center; gap: 8px; }
.streak__flame { color: var(--primary-color); font-size: 30px; }
.streak__num { font-size: 52px; font-weight: 900; color: var(--primary-color); line-height: 1; }
.streak__label { font-size: 16px; font-weight: 700; color: var(--primary-color); }
.streak__hint { font-size: 12px; opacity: 0.65; margin: 2px 0 16px; }
.streak__week { display: flex; justify-content: space-between; }
.pip { display: flex; flex-direction: column; align-items: center; gap: 5px; }
.pip__label { font-size: 11px; opacity: 0.6; }
.pip__dot {
    width: 34px;
    height: 34px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    border: 1px solid var(--theme-border);
    font-size: 12px;
    opacity: 0.9;
}
.pip__dot--filled { background: var(--primary-color); border-color: var(--primary-color); color: #fff; }
.pip__dot--today { border-width: 2px; border-color: var(--primary-color); color: var(--primary-color); }
.pip__dot--today.pip__dot--filled { color: #fff; }

/* Month calendar card */
.cal {
    width: 100%;
    padding: 16px;
    border: 1px solid var(--theme-border);
    border-radius: 20px;
    background: var(--theme-bg-soft);
}
.cal__head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.cal__title { font-size: 16px; font-weight: 800; margin: 0; }
.cal__count { font-size: 12px; font-weight: 600; color: var(--primary-color); }
.cal__grid { display: grid; grid-template-columns: repeat(7, 1fr); }
.cal__grid--labels { margin-bottom: 8px; }
.cal__wd { text-align: center; font-size: 11px; font-weight: 600; opacity: 0.6; }
.cal__cell { display: grid; place-items: center; aspect-ratio: 1; }
.cal__cell--blank { visibility: hidden; }
.cal__day {
    width: 36px;
    height: 36px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    border: 1px solid transparent;
    font-size: 13px;
    font-weight: 500;
}
.cal__day--filled { background: var(--primary-color); border-color: var(--primary-color); color: #fff; }
.cal__day--today { border-color: var(--primary-color); border-width: 2px; color: var(--primary-color); font-weight: 800; }
.cal__day--today.cal__day--filled { color: #fff; }
</style>
