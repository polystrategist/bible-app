<script lang="ts" setup>
import { Icon } from '@iconify/vue';

defineProps<{ ongoing: number; answered: number; thisWeek: number }>();
</script>

<template>
    <div class="stats">
        <div class="stats__cell">
            <Icon icon="lucide:clock" class="stats__icon" style="color: var(--primary-color)" />
            <span class="stats__label">Ongoing</span>
            <span class="stats__value">{{ ongoing }}</span>
            <span class="stats__caption">Keep praying</span>
        </div>
        <div class="stats__divider" />
        <div class="stats__cell">
            <Icon icon="lucide:circle-check" class="stats__icon" style="color: #16a34a" />
            <span class="stats__label">Answered</span>
            <span class="stats__value">{{ answered }}</span>
            <span class="stats__caption">God is faithful</span>
        </div>
        <div class="stats__divider" />
        <div class="stats__cell">
            <Icon icon="lucide:calendar-days" class="stats__icon" style="color: #8b5cf6" />
            <span class="stats__label">This week</span>
            <span class="stats__value">{{ thisWeek }}</span>
            <span class="stats__caption">New requests</span>
        </div>
    </div>
</template>

<style scoped>
.stats {
    display: flex;
    align-items: stretch;
    padding: 14px 0;
    border: 1px solid var(--theme-border);
    border-radius: 16px;
    background: var(--theme-bg-soft);
}
.stats__cell {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
}
.stats__icon { font-size: 20px; }
.stats__label { font-size: 11px; opacity: 0.7; }
.stats__value { font-size: 22px; font-weight: 800; }
.stats__caption { font-size: 10px; opacity: 0.55; }
.stats__divider { width: 1px; background: var(--theme-border); }
</style>
