<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { NIcon, useMessage, useDialog } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { PrayingHands } from '@vicons/fa';
import { useI18n } from 'vue-i18n';
import { usePrayerListStore } from '../../store/prayerListStore';
import { usePrayerStreakStore } from '../../store/prayerStreakStore';
import { usePraySessionStore } from '../../store/praySessionStore';
import EditPrayerItem from './EditPrayerItem.vue';
import NewPrayerItem from './CreateNewPrayerItem.vue';
import PrayerStatsStrip from './components/PrayerStatsStrip.vue';
import PrayerCard from './components/PrayerCard.vue';
import PraySession from './PraySession.vue';

const message = useMessage();
const dialog = useDialog();
const { t } = useI18n();

const prayerListStore = usePrayerListStore();
const streak = usePrayerStreakStore();
const session = usePraySessionStore();

const editPrayerModal = ref<any>(null);
const newPrayerModal = ref<any>(null);
const tab = ref<'ongoing' | 'done'>('ongoing');
const search = ref('');
const groupFilter = ref<string | null>(null);

onMounted(() => streak.loadDays());

const ongoing = computed(() => prayerListStore.prayerList);
const answered = computed(() => prayerListStore.donePrayerList);

const groups = computed(() => {
    const set = new Set<string>();
    for (const p of [...ongoing.value, ...answered.value]) {
        const g = (p.group ?? '').trim();
        if (g) set.add(g);
    }
    return [...set].sort();
});

const thisWeek = computed(() => {
    const cutoff = Date.now() - 7 * 86400000;
    return [...ongoing.value, ...answered.value].filter((p) => {
        const t = p.created_at ? new Date(p.created_at).getTime() : NaN;
        return !Number.isNaN(t) && t >= cutoff;
    }).length;
});

const visible = computed(() => {
    const list = tab.value === 'ongoing' ? ongoing.value : answered.value;
    const q = search.value.trim().toLowerCase();
    return list.filter((p) => {
        if (groupFilter.value && (p.group ?? '') !== groupFilter.value) return false;
        if (!q) return true;
        return (
            (p.title ?? '').toLowerCase().includes(q) ||
            (p.content ?? '').toLowerCase().includes(q) ||
            (p.group ?? '').toLowerCase().includes(q)
        );
    });
});

function editPrayer(item: any) {
    editPrayerModal.value?.modalTrigger(item);
}

async function toggle(item: any) {
    try {
        await prayerListStore.toggleStatus(item);
    } catch (e) {
        if (e instanceof Error) message.error(e.message);
    }
}

function remove(item: any) {
    dialog.warning({
        title: t('Confirm'),
        content: t('Are You Sure You want to remove?'),
        positiveText: t('Yes'),
        negativeText: t('No'),
        onPositiveClick: () => {
            try {
                prayerListStore.removePrayerItem(item.key);
            } catch (e) {
                if (e instanceof Error) message.error(e.message);
            }
        },
    });
}

function startPray(startIndex = 0) {
    session.open(ongoing.value as any[], startIndex);
}

function prayThis(item: any) {
    const idx = ongoing.value.findIndex((p) => p.key === item.key);
    startPray(idx < 0 ? 0 : idx);
}
</script>

<template>
    <div class="prayer-page scroll-bar-sm">
        <div class="prayer-page__inner">
            <!-- Header -->
            <div class="prayer-head">
                <NIcon class="prayer-head__leaf"><PrayingHands /></NIcon>
                <h1 class="prayer-head__title">Pray</h1>
                <p class="prayer-head__sub">Bring your requests before God</p>
            </div>

            <PrayerStatsStrip
                :ongoing="ongoing.length"
                :answered="answered.length"
                :this-week="thisWeek"
            />

            <!-- Ongoing / Answered toggle -->
            <div class="seg">
                <button
                    class="seg__btn"
                    :class="{ 'seg__btn--active': tab === 'ongoing' }"
                    @click="tab = 'ongoing'"
                >
                    <Icon icon="lucide:clock" />
                    <span>Ongoing</span>
                    <span class="seg__count">{{ ongoing.length }}</span>
                </button>
                <button
                    class="seg__btn"
                    :class="{ 'seg__btn--active': tab === 'done' }"
                    @click="tab = 'done'"
                >
                    <Icon icon="lucide:circle-check" />
                    <span>Answered</span>
                    <span class="seg__count">{{ answered.length }}</span>
                </button>
            </div>

            <!-- Search + filter -->
            <div class="prayer-tools">
                <div class="prayer-search">
                    <Icon icon="lucide:search" />
                    <input v-model="search" type="text" placeholder="Search prayers…" />
                </div>
                <select v-model="groupFilter" class="prayer-filter">
                    <option :value="null">All groups</option>
                    <option v-for="g in groups" :key="g" :value="g">{{ g }}</option>
                </select>
            </div>

            <!-- List -->
            <div class="prayer-list">
                <PrayerCard
                    v-for="p in visible"
                    :key="p.key"
                    :prayer="p"
                    :answered="tab === 'done'"
                    @edit="editPrayer(p)"
                    @remove="remove(p)"
                    @toggle="toggle(p)"
                    @pray="prayThis(p)"
                />
                <div v-if="visible.length === 0" class="prayer-empty">
                    <Icon :icon="search || groupFilter ? 'lucide:search-x' : 'lucide:hand-heart'" />
                    <p v-if="search || groupFilter">No prayers match your search</p>
                    <p v-else-if="tab === 'ongoing'">No ongoing prayers yet</p>
                    <p v-else>No answered prayers yet</p>
                </div>
            </div>
        </div>

        <!-- Floating controls -->
        <div class="prayer-fabs">
            <button v-if="ongoing.length" class="prayer-start" @click="startPray(0)">
                <NIcon class="prayer-start__icon"><PrayingHands /></NIcon>
                Start Pray
            </button>
            <button class="prayer-add" title="New prayer" @click="newPrayerModal?.open()">
                <Icon icon="lucide:plus" />
            </button>
            <NewPrayerItem ref="newPrayerModal" :show-trigger="false" />
        </div>

        <EditPrayerItem ref="editPrayerModal" />
        <PraySession />
    </div>
</template>

<style scoped>
.prayer-page {
    position: relative;
    height: 100%;
    overflow-y: auto;
    background: var(--theme-bg-main);
    color: var(--theme-text);
}
.prayer-page__inner {
    max-width: 720px;
    margin: 0 auto;
    padding: 16px 20px 120px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.prayer-head { display: flex; flex-direction: column; align-items: center; text-align: center; }
.prayer-head__leaf { color: var(--primary-color); font-size: 24px; }
.prayer-head__title { font-size: 30px; font-weight: 800; margin: 2px 0 0; }
.prayer-head__sub { font-size: 13px; opacity: 0.65; margin: 2px 0 0; }

.seg {
    display: flex;
    gap: 4px;
    padding: 4px;
    border-radius: 999px;
    background: var(--theme-bg-elevated);
}
.seg__btn {
    flex: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    padding: 9px;
    border: none;
    border-radius: 999px;
    background: transparent;
    color: var(--theme-text-soft);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}
.seg__btn--active { background: var(--theme-bg-main); color: var(--theme-text); box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08); }
.seg__count {
    min-width: 20px;
    padding: 1px 6px;
    border-radius: 999px;
    background: color-mix(in srgb, var(--primary-color) 14%, transparent);
    color: var(--primary-color);
    font-size: 11px;
    font-weight: 700;
}

.prayer-tools { display: flex; gap: 8px; }
.prayer-search {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 12px;
    height: 42px;
    border: 1px solid var(--theme-border);
    border-radius: 12px;
    background: var(--theme-bg-soft);
    opacity: 0.9;
}
.prayer-search input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    color: var(--theme-text);
    font-size: 13px;
}
.prayer-filter {
    height: 42px;
    padding: 0 12px;
    border: 1px solid var(--theme-border);
    border-radius: 12px;
    background: var(--theme-bg-soft);
    color: var(--theme-text);
    font-size: 13px;
    cursor: pointer;
}

.prayer-list { display: flex; flex-direction: column; }
.prayer-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 48px 0;
    opacity: 0.55;
    font-size: 30px;
}
.prayer-empty p { font-size: 14px; margin: 0; }

.prayer-fabs {
    position: absolute;
    bottom: 20px;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
}
.prayer-start {
    height: 48px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 0 24px;
    border: none;
    border-radius: 999px;
    background: var(--primary-color);
    color: #fff;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
}
.prayer-start:hover { filter: brightness(1.05); }
.prayer-start__icon { font-size: 18px; }

.prayer-add {
    width: 48px;
    height: 48px;
    flex-shrink: 0;
    display: grid;
    place-items: center;
    border: 1px solid var(--theme-border);
    border-radius: 50%;
    background: var(--theme-bg-soft);
    color: var(--theme-text);
    font-size: 22px;
    cursor: pointer;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
}
.prayer-add:hover { background: var(--theme-bg-elevated); }
</style>
