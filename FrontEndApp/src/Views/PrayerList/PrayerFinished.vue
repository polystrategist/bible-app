<script lang="ts" setup>
import { computed } from 'vue';
import { Icon } from '@iconify/vue';
import { usePrayerStreakStore } from '../../store/prayerStreakStore';

const emit = defineEmits<{ (e: 'done'): void }>();
const streak = usePrayerStreakStore();

const VERSES = [
    { text: 'Keep drawing near to God, one prayer at a time.', ref: 'James 4:8' },
    { text: 'The prayer of a righteous person is powerful and effective.', ref: 'James 5:16' },
    { text: 'Pray continually, give thanks in all circumstances.', ref: '1 Thessalonians 5:17' },
    { text: 'Cast all your anxiety on him because he cares for you.', ref: '1 Peter 5:7' },
];
const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const verse = computed(() => VERSES[streak.currentStreak % VERSES.length]);
</script>

<template>
    <div class="finished">
        <div class="finished__check">
            <Icon icon="lucide:hand-heart" />
            <span class="finished__badge"><Icon icon="lucide:check" /></span>
        </div>
        <h2 class="finished__title">Prayer finished</h2>
        <p class="finished__sub">Well done. You spent time with God today. 💙</p>

        <div class="streak">
            <div class="streak__num">{{ streak.currentStreak }}</div>
            <div class="streak__label">day streak</div>
            <div class="streak__week">
                <div v-for="(d, i) in streak.weekDays" :key="i" class="pip">
                    <span class="pip__label">{{ labels[i] }}</span>
                    <span
                        class="pip__dot"
                        :class="{ 'pip__dot--filled': d.prayed, 'pip__dot--today': d.isToday }"
                    >
                        <Icon v-if="d.prayed" icon="lucide:check" />
                        <template v-else>{{ d.date.getDate() }}</template>
                    </span>
                    <span class="pip__today">{{ d.isToday ? 'Today' : '' }}</span>
                </div>
            </div>
        </div>

        <div class="verse">
            <Icon icon="lucide:quote" class="verse__icon" />
            <div>
                <div class="verse__text">{{ verse.text }}</div>
                <div class="verse__ref">{{ verse.ref }}</div>
            </div>
        </div>

        <button class="finished__amen" @click="emit('done')">
            Amen <Icon icon="lucide:chevron-right" />
        </button>
    </div>
</template>

<style scoped>
.finished {
    width: min(440px, 92vw);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}
.finished__check {
    position: relative;
    width: 96px;
    height: 96px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    background: color-mix(in srgb, var(--primary-color) 10%, transparent);
    border: 2px solid color-mix(in srgb, var(--primary-color) 25%, transparent);
    color: var(--primary-color);
    font-size: 44px;
}
.finished__badge {
    position: absolute;
    right: -2px;
    bottom: -2px;
    width: 28px;
    height: 28px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    background: var(--primary-color);
    color: #fff;
    font-size: 15px;
    border: 2px solid var(--theme-bg-main);
}
.finished__title { font-size: 28px; font-weight: 800; margin: 18px 0 6px; }
.finished__sub { opacity: 0.7; margin: 0 0 22px; }

.streak {
    width: 100%;
    padding: 20px 16px;
    border: 1px solid var(--theme-border);
    border-radius: 20px;
    background: var(--theme-bg-soft);
}
.streak__num { font-size: 52px; font-weight: 900; color: var(--primary-color); line-height: 1; }
.streak__label { font-size: 16px; font-weight: 700; color: var(--primary-color); margin-bottom: 16px; }
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
.pip__dot--filled {
    background: var(--primary-color);
    border-color: var(--primary-color);
    color: #fff;
}
.pip__dot--today { border-width: 2px; border-color: var(--primary-color); color: var(--primary-color); }
.pip__dot--today.pip__dot--filled { color: #fff; }
.pip__today { font-size: 9px; color: var(--primary-color); min-height: 12px; }

.verse {
    display: flex;
    gap: 10px;
    text-align: left;
    width: 100%;
    padding: 16px;
    margin: 16px 0;
    border-radius: 16px;
    background: color-mix(in srgb, var(--primary-color) 6%, transparent);
    border: 1px solid color-mix(in srgb, var(--primary-color) 18%, transparent);
}
.verse__icon { color: var(--primary-color); font-size: 22px; flex-shrink: 0; }
.verse__text { font-size: 14px; line-height: 1.4; }
.verse__ref { font-size: 13px; font-weight: 700; color: var(--primary-color); margin-top: 6px; }

.finished__amen {
    width: 100%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 16px;
    border: none;
    border-radius: 999px;
    background: var(--primary-color);
    color: #fff;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
}
.finished__amen:hover { filter: brightness(1.05); }
</style>
