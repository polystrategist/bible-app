<script lang="ts" setup>
import { computed, ref, watch, onBeforeUnmount } from 'vue';
import { Icon } from '@iconify/vue';
import { usePraySessionStore } from '../../store/praySessionStore';
import { usePrayerStreakStore } from '../../store/prayerStreakStore';
import { groupStyle, relativeTime } from './prayerGroupStyle';
import PrayerFinished from './PrayerFinished.vue';

const session = usePraySessionStore();
const streak = usePrayerStreakStore();

const index = ref(0);
const elapsed = ref(0);
const paused = ref(false);
const finished = ref(false);
let timer: ReturnType<typeof setInterval> | null = null;

const total = computed(() => session.prayers.length);
const current = computed(() => session.prayers[index.value]);
const style = computed(() => groupStyle(current.value?.group));
const isLast = computed(() => index.value >= total.value - 1);

const timeLabel = computed(() => {
    const m = String(Math.floor(elapsed.value / 60)).padStart(2, '0');
    const s = String(elapsed.value % 60).padStart(2, '0');
    return `${m}:${s}`;
});

function startTimer() {
    stopTimer();
    timer = setInterval(() => {
        if (!paused.value) elapsed.value++;
    }, 1000);
}
function stopTimer() {
    if (timer) clearInterval(timer);
    timer = null;
}

// Reset + start whenever the overlay opens.
watch(
    () => session.visible,
    (vis) => {
        if (vis) {
            index.value = session.startIndex;
            elapsed.value = 0;
            paused.value = false;
            finished.value = false;
            startTimer();
        } else {
            stopTimer();
        }
    }
);

onBeforeUnmount(stopTimer);

function next() {
    if (!isLast.value) index.value++;
}
function prev() {
    if (index.value > 0) index.value--;
}
async function finish() {
    stopTimer();
    await streak.recordTodayPrayed(elapsed.value);
    finished.value = true;
}
function done() {
    session.close();
}
</script>

<template>
    <Teleport to="body">
        <div v-if="session.visible" class="pray-overlay">
            <PrayerFinished v-if="finished" @done="done" />

            <template v-else>
                <button class="pray-close" @click="session.close()">
                    <Icon icon="lucide:x" />
                </button>

                <div class="pray-body">
                    <div class="pray-icon" :style="{ background: style.color + '24', color: style.color }">
                        <Icon :icon="style.icon" />
                    </div>
                    <div class="pray-tags">
                        <span
                            v-if="current?.group"
                            class="pray-group"
                            :style="{ background: style.color + '24', color: style.color }"
                        >{{ current.group }}</span>
                        <span class="pray-now">
                            <span class="pray-now__dot" /> Now praying
                        </span>
                    </div>
                    <h2 class="pray-title">{{ current?.title || 'Untitled prayer' }}</h2>

                    <div class="pray-progress">
                        <div class="pray-progress__track">
                            <div
                                class="pray-progress__fill"
                                :style="{ width: ((index + 1) / total) * 100 + '%' }"
                            />
                        </div>
                        <span class="pray-progress__label">{{ index + 1 }} of {{ total }}</span>
                    </div>

                    <div
                        v-if="current?.content"
                        class="pray-content prose-mirror-render-html"
                        v-html="current.content"
                    />
                    <div class="pray-when">
                        <Icon icon="lucide:clock" /> {{ relativeTime(current?.created_at) }}
                    </div>
                </div>

                <div class="pray-nav">
                    <button class="pray-next" :disabled="isLast" @click="next">
                        <span v-if="isLast">Last prayer</span>
                        <span v-else>Next <Icon icon="lucide:chevron-right" /></span>
                    </button>
                    <button class="pray-circle" :disabled="index === 0" @click="prev">
                        <Icon icon="lucide:chevron-left" />
                    </button>
                </div>

                <div class="pray-timer">
                    <button class="pray-circle" @click="paused = !paused">
                        <Icon :icon="paused ? 'lucide:play' : 'lucide:pause'" />
                    </button>
                    <div class="pray-timer__text">
                        <span class="pray-timer__label">Prayer time</span>
                        <span class="pray-timer__value">{{ timeLabel }}</span>
                    </div>
                    <button class="pray-finish" @click="finish">
                        <Icon icon="lucide:circle-check" /> Finished
                    </button>
                </div>
            </template>
        </div>
    </Teleport>
</template>

<style scoped>
.pray-overlay {
    position: fixed;
    inset: 0;
    z-index: 4000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 18px;
    padding: 24px;
    background: var(--theme-bg-main);
    color: var(--theme-text);
    overflow-y: auto;
}
.pray-close {
    position: absolute;
    top: 18px;
    right: 18px;
    width: 40px;
    height: 40px;
    display: grid;
    place-items: center;
    border: none;
    background: transparent;
    color: var(--theme-text);
    cursor: pointer;
    border-radius: 10px;
    font-size: 20px;
}
.pray-close:hover { background: var(--theme-bg-elevated); }

.pray-body {
    width: min(560px, 92vw);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}
.pray-icon {
    width: 64px;
    height: 64px;
    display: grid;
    place-items: center;
    border-radius: 18px;
    font-size: 30px;
    margin-bottom: 16px;
}
.pray-tags { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }
.pray-group { font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 999px; }
.pray-now {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 12px;
    font-weight: 700;
    color: var(--primary-color);
    padding: 4px 12px;
    border: 1px solid var(--theme-border);
    border-radius: 999px;
    background: var(--theme-bg-soft);
}
.pray-now__dot { width: 8px; height: 8px; border-radius: 50%; background: var(--primary-color); }
.pray-title { font-size: 28px; font-weight: 800; margin: 0 0 18px; }

.pray-progress { width: 100%; display: flex; align-items: center; gap: 12px; margin-bottom: 18px; }
.pray-progress__track {
    flex: 1;
    height: 6px;
    border-radius: 999px;
    background: var(--theme-bg-elevated);
    overflow: hidden;
}
.pray-progress__fill { height: 100%; background: var(--primary-color); transition: width 0.25s; }
.pray-progress__label { font-size: 13px; font-weight: 600; opacity: 0.7; }

.pray-content { font-size: 17px; line-height: 1.6; opacity: 0.85; }
.pray-when {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    opacity: 0.6;
    margin-top: 16px;
}

.pray-nav { width: min(560px, 92vw); display: flex; gap: 12px; }
.pray-next {
    flex: 1;
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
.pray-next:disabled { background: var(--theme-bg-elevated); color: var(--theme-text-soft); cursor: default; }
.pray-circle {
    width: 52px;
    height: 52px;
    flex-shrink: 0;
    display: grid;
    place-items: center;
    border: none;
    border-radius: 50%;
    background: color-mix(in srgb, var(--primary-color) 12%, transparent);
    color: var(--primary-color);
    cursor: pointer;
    font-size: 20px;
}
.pray-circle:disabled { background: var(--theme-bg-elevated); color: var(--theme-text-soft); cursor: default; }

.pray-timer {
    width: min(560px, 92vw);
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    border: 1px solid var(--theme-border);
    border-radius: 18px;
    background: var(--theme-bg-soft);
}
.pray-timer__text { display: flex; flex-direction: column; }
.pray-timer__label { font-size: 11px; opacity: 0.6; }
.pray-timer__value { font-size: 20px; font-weight: 800; }
.pray-finish {
    margin-left: auto;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 14px 20px;
    border: none;
    border-radius: 999px;
    background: var(--primary-color);
    color: #fff;
    font-size: 14px;
    font-weight: 700;
    cursor: pointer;
}
</style>
