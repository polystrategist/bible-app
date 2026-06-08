<script lang="ts" setup>
import { computed, h } from 'vue';
import { NDropdown, NIcon } from 'naive-ui';
import { Icon } from '@iconify/vue';
import { groupStyle, relativeTime } from '../prayerGroupStyle';

const props = defineProps<{
    prayer: {
        key: string;
        title?: string | null;
        content?: string;
        group?: string | null;
        status?: string | null;
        created_at?: string;
    };
    answered: boolean;
}>();

const emit = defineEmits<{
    (e: 'edit'): void;
    (e: 'remove'): void;
    (e: 'toggle'): void;
    (e: 'pray'): void;
}>();

const style = computed(() => groupStyle(props.prayer.group));
const when = computed(() => relativeTime(props.prayer.created_at));

// Strip the rich-text markup to a single flowing line; the template clamps it
// to two lines with an ellipsis.
const preview = computed(() => {
    const div = document.createElement('div');
    div.innerHTML = props.prayer.content ?? '';
    return (div.textContent || '').replace(/\s+/g, ' ').trim();
});

const renderIcon = (icon: string) => () => h(NIcon, null, { default: () => h(Icon, { icon }) });

const menuOptions = computed(() => [
    ...(!props.answered
        ? [{ label: 'Pray this', key: 'pray', icon: renderIcon('lucide:hand-heart') }]
        : []),
    {
        label: props.answered ? 'Mark ongoing' : 'Mark answered',
        key: 'toggle',
        icon: renderIcon('lucide:circle-check'),
    },
    { label: 'Edit', key: 'edit', icon: renderIcon('lucide:pencil') },
    { label: 'Remove', key: 'remove', icon: renderIcon('lucide:trash-2') },
]);

function onSelect(key: string) {
    if (key === 'edit') emit('edit');
    else if (key === 'remove') emit('remove');
    else if (key === 'toggle') emit('toggle');
    else if (key === 'pray') emit('pray');
}
</script>

<template>
    <div class="pcard">
        <div class="pcard__icon" :style="{ background: style.color + '24', color: style.color }">
            <Icon :icon="style.icon" />
        </div>
        <div class="pcard__body">
            <span
                v-if="prayer.group"
                class="pcard__group"
                :style="{ background: style.color + '24', color: style.color }"
            >{{ prayer.group }}</span>
            <div class="pcard__title">{{ prayer.title || 'Untitled prayer' }}</div>
            <div v-if="preview" class="pcard__content">{{ preview }}</div>
            <div class="pcard__footer">
                <span class="pcard__time">
                    <Icon icon="lucide:clock" /> {{ when }}
                </span>
                <button
                    class="pcard__toggle"
                    :style="{
                        color: answered ? 'var(--theme-text-soft)' : '#16a34a',
                        background: (answered ? '#9ca3af' : '#16a34a') + '20',
                    }"
                    @click="emit('toggle')"
                >
                    <Icon :icon="answered ? 'lucide:undo-2' : 'lucide:circle-check'" />
                    {{ answered ? 'Mark Ongoing' : 'Mark Answered' }}
                </button>
            </div>
        </div>
        <NDropdown trigger="click" :options="menuOptions" @select="onSelect">
            <button class="pcard__menu"><Icon icon="lucide:ellipsis-vertical" /></button>
        </NDropdown>
    </div>
</template>

<style scoped>
.pcard {
    display: flex;
    gap: 12px;
    padding: 14px;
    margin-bottom: 12px;
    border: 1px solid var(--theme-border);
    border-radius: 16px;
    background: var(--theme-bg-soft);
}
.pcard__icon {
    width: 44px;
    height: 44px;
    flex-shrink: 0;
    display: grid;
    place-items: center;
    border-radius: 12px;
    font-size: 20px;
}
.pcard__body { flex: 1; min-width: 0; }
.pcard__group {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 9px;
    border-radius: 999px;
    margin-bottom: 6px;
}
.pcard__title { font-weight: 700; font-size: 15px; margin-bottom: 4px; }
.pcard__content {
    font-size: 13px;
    opacity: 0.7;
    line-height: 1.35;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.pcard__footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 10px;
}
.pcard__time {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    opacity: 0.6;
}
.pcard__toggle {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 12px;
    font-weight: 700;
    padding: 7px 12px;
    border: none;
    border-radius: 999px;
    cursor: pointer;
}
.pcard__menu {
    flex-shrink: 0;
    width: 30px;
    height: 30px;
    display: grid;
    place-items: center;
    border: none;
    background: transparent;
    color: var(--theme-text-soft);
    cursor: pointer;
    border-radius: 8px;
    font-size: 18px;
}
.pcard__menu:hover { background: var(--theme-bg-elevated); }
</style>
